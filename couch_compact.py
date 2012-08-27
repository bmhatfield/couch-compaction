import json
import urllib2

couch_server = "192.168.33.11"
couch_port = 5984
db = "chef"


def post(url):
    reqObj = urllib2.Request(url, data=" ", headers={'Content-type': 'application/json'})
    req = urllib2.urlopen(reqObj)
    return json.load(req)


def views(url):
    designs_request = urllib2.urlopen(views_URL)
    designs = json.load(designs_request)
    return [x['id'].split("/")[1] for x in designs['rows']]


# Retrieve all the 'views', and then compact each one.
views_URL = 'http://%s:%s/%s/_all_docs?startkey="_design/"&endkey="_design0"' % (couch_server, couch_port, db)
for view in views(views_URL):
    print view, post("http://%s:%s/%s/_compact/%s" % (couch_server, couch_port, db, view))

# Run a 'view cleanup' against all the views that have just been compacted.
print "view_cleanup", post("http://%s:%s/%s/_view_cleanup" % (couch_server, couch_port, db))

# Finally, run a compaction against the whole database.
print "compact", post("http://%s:%s/%s/_compact" % (couch_server, couch_port, db))
