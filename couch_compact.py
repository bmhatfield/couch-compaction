#!/usr/bin/env python
# http://docs.python-requests.org/en/latest/user/quickstart/
import requests
import datetime
import gzip
from optparse import OptionParser


def save_url(url, file_handle, size=(8 * 1024)):
    req = requests.get(url, prefetch=False)

    while True:
        chunk = req.raw.read(size)
        if chunk:
            file_handle.write(chunk)
        else:
            break

    return req.status_code


def put(url):
    req = requests.put(url)
    return req.json


def post(url, content=""):
    req = requests.post(url, data=content, headers={'content-type': 'application/json'})
    return req.json


def views(url):
    req = requests.get(views_URL)
    designs = req.json
    return [x['id'].split("/")[1] for x in designs['rows']]

parser = OptionParser()
parser.add_option("--couch-server", dest="server", default="192.168.33.11", help="Couch Database Server Hostname/IP")
parser.add_option("--couch-port", dest="port", default=5984, help="Couch Database Server Port")
parser.add_option("--database", dest="database", default='chef', help="Database to work with")

parser.add_option("--all", dest="all", action='store_true', default=False, help="Run all compaction and backup steps, except restore")
parser.add_option("--compact-views", dest="compact_views", action='store_true', default=False, help="Compact each view")
parser.add_option("--cleanup-views", dest="cleanup_views", action='store_true', default=False, help="Clean up previously-compacted view files")
parser.add_option("--compact-database", dest="compact_database", action='store_true', default=False, help="Compact database")

parser.add_option("--backup", dest="backup", action='store_true', default=False, help="Export database backup")
parser.add_option("--restore", dest="restore_file", default=None, help="Restore database from file")

parser.add_option("--s3-bucket", dest="s3_bucket", default=None, help="Save Backup to S3 Bucket specified")
(options, args) = parser.parse_args()

if options.restore_file:
    with gzip.open(options.restore_file) as handle:
        # need to modify the first line from:
        #   "total_rows":4879,"offset":0,"rows":
        # to:
        #   "docs":
        print "restore", post("http://%s:%s/%s/_bulk_docs" % (options.server, options.port, options.database), handle.read())

if options.compact_views or options.all:
    # Retrieve all the 'views', and then compact each one.
    views_URL = 'http://%s:%s/%s/_all_docs?startkey="_design/"&endkey="_design0"' % (options.server, options.port, options.database)
    for view in views(views_URL):
        print "Compacting:", view, post("http://%s:%s/%s/_compact/%s" % (options.server, options.port, options.database, view))

if options.cleanup_views or options.all:
    # Run a 'view cleanup' against all the views that have just been compacted.
    print "Running View Cleanup...", post("http://%s:%s/%s/_view_cleanup" % (options.server, options.port, options.database))

if options.compact_database or options.all:
    # Run a compaction against the whole database.
    print "Running Overall Compaction...", post("http://%s:%s/%s/_compact" % (options.server, options.port, options.database))

if options.backup:
    d = datetime.datetime.now()
    with gzip.open('backup-%s-%s.bak.gz' % (options.database, d.strftime("%Y-%m-%d_%H.%M.%S")), 'w') as handle:
        print "backup", save_url("http://%s:%s/%s/_all_docs?include_docs=true" % (options.server, options.port, options.database), handle)

        if options.s3_bucket:
            try:
                from boto.s3.connection import S3Connection
                from boto.s3.bucket import Bucket
            except:
                print "Unable to import boto, s3 upload skipped."
                exit(1)

            s3 = S3Connection()
            bucket = Bucket(s3, "couch-testbucket")
