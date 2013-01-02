#!/usr/bin/python

import core

def start_sp():
  
  ami = core.get_image("SP2013 Demo")
  s = core.get_instance(core.start_spot( ami.id, "m1.large", placement="us-east-1c"))

  core.wait_running(s)
  core.set_name( s, "SP2013" )

  return s

def attach_fitnesse(s):  

  core.attach_volume('vol-1fb7d673',s) 
  core.log( "SP2013 Lab has been started!" )

if __name__ == "__main__":

  core.init()
  attach_fitnesse( start_sp() )

