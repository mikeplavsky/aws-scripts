#!/usr/bin/python

import core
import os

if __name__ == "__main__":  

  core.init()

  img = core.get_image("selenium")
  spot = core.start_spot(img.id, 'm1.small')

  inst_id = core.get_instance( spot )
  core.wait_running( inst_id )

  inst = core.get_instance_by_id(inst_id) 

  os.system("cli53 rrcreate quest.com selenium A %s --replace" % inst.private_ip_address)
  core.log( 'selenium started at %s' % inst.public_dns_name )

