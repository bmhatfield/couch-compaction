couch-compaction
================

A simple script to automatically perform the various CouchDB compaction tasks.

Usage
=====

    [bhatfield@bhatfield-mac couch-compaction]$ python couch_compact.py --help
    Usage: couch_compact.py [options]

    Options:
      -h, --help            show this help message and exit
      --couch-server=SERVER
                            Couch Database Server Hostname/IP
      --couch-port=PORT     Couch Database Server Port
      --database=DATABASE   Database to work with
      --all                 Run all compaction and backup steps, except restore
      --compact-views       Compact each view
      --cleanup-views       Clean up previously-compacted view files
      --compact-database    Compact database
      --backup              Export database backup
      --restore=RESTORE_FILE
                            Restore database from file
      --s3-bucket=S3_BUCKET
                            Save Backup to S3 Bucket specified
