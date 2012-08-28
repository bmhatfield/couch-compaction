import json
import urllib2
import datetime
from optparse import OptionParser


def save_url(url, file_handle, size=4096):
    req = urllib2.urlopen(url)

    while True:
        chunk = req.read(size)
        if chunk:
            file_handle.write(chunk)
        else:
            break


def post(url):
    reqObj = urllib2.Request(url, data=" ", headers={'Content-type': 'application/json'})
    req = urllib2.urlopen(reqObj)
    return json.load(req)


def views(url):
    designs_request = urllib2.urlopen(views_URL)
    designs = json.load(designs_request)
    return [x['id'].split("/")[1] for x in designs['rows']]


parser = OptionParser()
parser.add_option("--couch-server", dest="server", default="192.168.33.11", help="Couch Database Server Hostname/IP")
parser.add_option("--couch-port", dest="port", default=5984, help="Couch Database Server Port")
parser.add_option("--database", dest="database", default='chef', help="Database to work with")

parser.add_option("--backup", dest="backup", action='store_true', default=False, help="Export database backup")
parser.add_option("--compact-views", dest="compact_views", action='store_true', default=False, help="Compact each view")
parser.add_option("--compact-database", dest="compact_database", action='store_true', default=False, help="Compact database")
parser.add_option("--cleanup-views", dest="cleanup_views", action='store_true', default=False, help="Clean up previously-compacted view files")
(options, args) = parser.parse_args()

if options.compact_views:
    # Retrieve all the 'views', and then compact each one.
    views_URL = 'http://%s:%s/%s/_all_docs?startkey="_design/"&endkey="_design0"' % (options.server, options.port, options.database)
    for view in views(views_URL):
        print view, post("http://%s:%s/%s/_compact/%s" % (options.server, options.port, options.database, view))

if options.cleanup_views:
    # Run a 'view cleanup' against all the views that have just been compacted.
    print "view_cleanup", post("http://%s:%s/%s/_view_cleanup" % (options.server, options.port, options.database))

if options.compact_database:
    # Run a compaction against the whole database.
    print "compact", post("http://%s:%s/%s/_compact" % (options.server, options.port, options.database))

if options.backup:
    d = datetime.datetime.now()
    with open('backup-%s-%s.bak' % (options.database, d.strftime("%Y-%m-%d_%H.%M.%S")), 'w') as handle:
        save_url("http://%s:%s/%s/_all_docs?include_docs=true" % (options.server, options.port, options.database), handle)
