import boto
import time

ec2 = boto.connect_ec2()
sns = boto.connect_sns()

def log(msg):
  sns.publish( 'arn:aws:sns:us-east-1:758139277749:SharePointLab', msg, 'Lab Start' )

def start_dc():

  dc = ec2.run_instances('ami-c5a675ac', 

    key_name = 'webserver',
    instance_type = 'm1.small',
    subnet_id = 'subnet-b58921dd',
    private_ip_address = '10.0.0.10',
    security_group_ids = ['sg-824d54ee']

  ).instances[0]

  while dc.state != 'running':

    dc.update()
    time.sleep(2)

  ip = ec2.allocate_address(domain='vpc')
  ec2.associate_address( dc.id,  allocation_id=ip.allocation_id )

  v = ec2.get_all_volumes( ['vol-1fb7d673'] )[0]
  ec2.attach_volume(  v.id, dc.id, 'xvdf' )

  log( 'velasekc-dc started' )


def start_spot( image_id ):

  return ec2.request_spot_instances( '0.2', image_id, count = 1,

    key_name = 'webserver',
    instance_type = 'm1.medium',
    subnet_id = 'subnet-b58921dd'

  )[0]

def start_wss(): 

  start_spot('ami-4be23222')
  log( 'wss4fe started' )

def start_sql():

  s_sql = start_spot( 'ami-7fe23216' )

  sql = lambda: ec2.get_all_spot_instance_requests([s_sql.id])[0]
  while sql().state != 'active': time.sleep(1)

  instance_id = sql().instance_id

  v = ec2.get_all_volumes( ['vol-3df85651'] )[0]
  ec2.attach_volume(  v.id, instance_id, 'xvdf' )

  ip = ec2.allocate_address(domain='vpc')
  ec2.associate_address( instance_id,  allocation_id=ip.allocation_id )

  log( 'sql1 started' )

