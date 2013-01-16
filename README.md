couch-compaction
================

A simple script to automatically perform the various CouchDB compaction tasks.

Versioning Note
===============

As of Requests 1.0, some of the Requests APIs changed; resp.json went from at attribute to a method, etc.
I've updated couch_compact.py to support 1.0+ of Requests, but this means that previous versions are not supported anymore.

Usage Example
=============

    python couch_compact.py --couch-server ec2-INSTANCE.compute-1.amazonaws.com --all
    [wait a few moments]
    python couch_compact.py --couch-server ec2-INSTANCE.compute-1.amazonaws.com --backup

Full Usage
==========

    [bhatfield@bhatfield-mac couch-compaction]$ python couch_compact.py --help
    Usage: couch_compact.py [options]

    Options:
      -h, --help            show this help message and exit
      --couch-server=SERVER
                            Couch Database Server Hostname/IP
      --couch-port=PORT     Couch Database Server Port
      --database=DATABASE   Database to work with
      --all                 Run all compaction steps (--compact-views, --cleanup-
                              views, --compact-database)
      --compact-views       Compact each view
      --cleanup-views       Clean up previously-compacted view files
      --compact-database    Compact database
      --backup              Export database backup
      --restore=RESTORE_FILE
                            Restore database from file
