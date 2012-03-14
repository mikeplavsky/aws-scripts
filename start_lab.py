#!/usr/bin/python

import core

try:

  core.start_dc()
  core.start_wss()
  core.start_sql()

except Exception, e:

  print e.message
  core.log( e.message )







