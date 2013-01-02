#!/usr/bin/python
import core

if __name__ == "__main__":  

  core.init()

  def call(func):
    try:
      func()
    except Exception, e:
      core.log(str(e))

  filter = lambda(x): x.tags.get( "aws:autoscaling:groupName" ) != None

  [call(y.terminate) for x in core.ec2.get_all_instances() for y in x.instances if not filter(y)]

  [core.ec2.disassociate_address(association_id = x.association_id) 
    for x in core.ec2.get_all_addresses() if x.association_id]

  [core.ec2.release_address(allocation_id = x.allocation_id) 
    for x in core.ec2.get_all_addresses() if x.allocation_id]

  [v.delete() for v in core.ec2.get_all_volumes() if not v.tags and v.status != 'in-use']
  [call(x.delete) for x in core.ec2.get_all_snapshots(owner = 'self')]
