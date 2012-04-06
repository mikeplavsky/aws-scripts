#!/usr/bin/python

import core

if __name__ != "__main__":  

  try:

    core.init()

    core.start_dc()
    core.start_spots()

    core.tune_sql()
    core.tune_wss() 

  except Exception, e:

    print e.message
    core.log( e.message )







