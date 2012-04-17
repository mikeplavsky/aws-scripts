#!/usr/bin/python

if __name__ == "__main__":  

  import core
  core.init()

  def terminate(image_id):

    i = core.ec2.get_all_instances(filters= { 'image-id': image_id })
    [y.terminate() for x in i for y in x.instances if y.state == 'running' ]

  selenium_id = core.get_image("selenium")

  [terminate(x) for x in ('ami-c5a675ac', 'ami-7fe23216', 'ami-4be23222', selenium_id)]

  [core.ec2.disassociate_address(association_id = x.association_id) 
    for x in core.ec2.get_all_addresses() if x.association_id]

  [core.ec2.release_address(allocation_id = x.allocation_id) 
    for x in core.ec2.get_all_addresses() if x.allocation_id]

