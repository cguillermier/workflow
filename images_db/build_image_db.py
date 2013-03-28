#!/usr/bin/python

import fnmatch
import os
import hashlib
import time
import sqlite3 as lite
import sys

#
# READ THIS!
# This script assumes several things:
# - db file is in this directory
# - db allready has a table Images generated with:
# CREATE TABLE Images( id INTEGER PRIMARY KEY, fname TEXT, path TEXT, size INTEGER, mtime TEXT, own INTEGER, perm TEXT, hash TEXT );
# - need to set the search root 'start'
# - need to set image extensions
# - as of now there is no check to see if file is in db
#
# has been run against:
#

start = "/nrims/home3/cpoczatek/Pictures/"
extensions = ('.png','.jpg')
con = lite.connect('test.db')
cur = con.cursor()

for root, dirnames, filenames in os.walk(start):
  for filename in filenames:
    if filename.endswith(extensions):
      # get full path
      fullpath = os.path.join(root, filename)

      cur.execute("SELECT fname FROM Images WHERE path=:path", {"path": fullpath})        
      con.commit()
      
      row = cur.fetchone()
      if row!=None:
        print ("skipping", fullpath)
        continue
      
      # computing the hash piece by piece is more memory efficient
      #This is too slow, commenting out
#      md5 = hashlib.md5()
#      f = open(fullpath, 'r')
#      while True:
#        data = f.read(2**14)
#        if not data:
#            break
#        md5.update(data)
#      psum = md5.hexdigest()

      # get file metadata
      info = os.stat(fullpath)
      # format modification time
      modtime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(info.st_mtime))
      # get owner/permissions
      owner = info.st_uid
      perm = oct(info.st_mode)[-3:]

      stats = (filename, fullpath, info.st_size, modtime, owner, perm)
      print stats
      
      #cur.select(UPDATE Cars SET Price=? WHERE Id=?", (uPrice, uId))
      cur.execute("INSERT INTO Images(fname, path, size, mtime, own, perm) VALUES(?,?,?,?,?,?)", stats )
      con.commit()



