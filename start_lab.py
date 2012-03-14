#!/usr/bin/python

import core

try:

  start_dc()
  start_wss()
  start_sql()

except Exception, e:

  core.log( e.message )







