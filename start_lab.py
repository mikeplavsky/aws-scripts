#!/usr/bin/python

import core

try:

  core.start_dc()
  core.start_spots()

  core.tune_sql()
  core.tune_wss() 

except Exception, e:

  print e.message
  core.log( e.message )







