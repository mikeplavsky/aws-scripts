import time

ec2 = None
sns = None

def init():

  import boto
  
  res = globals()

  res["ec2"] = boto.connect_ec2()
  res["sns"] = boto.connect_sns()

set_name = lambda id, name: ec2.create_tags( [id], {'Name' : name } )

def wait_running(id):

  i = ec2.get_all_instances( [id] )[0].instances[0]

  while i.state != 'running':

    i.update()
    time.sleep(2)

def log(msg):

  try:
    
    sns.publish( 'arn:aws:sns:us-east-1:758139277749:SharePointLab', msg, 'Lab Start' )

  except Exception, e:

    print msg
    print e.message

def start_dc():

  dc = ec2.run_instances('ami-c5a675ac', 

    key_name = 'webserver',
    instance_type = 'm1.small',
    subnet_id = 'subnet-b58921dd',
    private_ip_address = '10.0.0.10',
    security_group_ids = ['sg-824d54ee']

  ).instances[0]

  wait_running(dc.id)

  ip = ec2.allocate_address(domain='vpc')
  ec2.associate_address( dc.id,  allocation_id=ip.allocation_id )

  v = ec2.get_all_volumes( ['vol-1fb7d673'] )[0]
  ec2.attach_volume(  v.id, dc.id, 'xvdf' )

  set_name( dc.id, 'velaskec-dc' )
  log( 'velaskec-dc started at %s' % ip.public_ip )


def start_spot( image_id ):

  return ec2.request_spot_instances( '0.2', image_id, count = 1,

    key_name = 'webserver',
    instance_type = 'm1.medium',
    subnet_id = 'subnet-b58921dd'

  )[0]

spots = []

def start_spots(): 

  [spots.append(start_spot(x)) for x  
    in [ 'ami-7fe23216','ami-4be23222']]

  log( 'spot requests have been created' )

def get_instance(spot_id):

  spot = lambda: ec2.get_all_spot_instance_requests([spot_id.id])[0]
  while spot().state != 'active': time.sleep(1)

  return spot().instance_id


def allocate_ip(id):

  ip = ec2.allocate_address(domain='vpc')
  ec2.associate_address( id,  allocation_id=ip.allocation_id )

  return ip


def tune_sql():

  instance_id = get_instance(spots[0])
  wait_running( instance_id )

  v = ec2.get_all_volumes( ['vol-3df85651'] )[0]
  ec2.attach_volume(  v.id, instance_id, 'xvdf' )

  ip = allocate_ip(instance_id)

  set_name( instance_id, 'sql1' )
  log( 'sql1 started at %s' % ip.public_ip )

def tune_wss():

  instance_id = get_instance(spots[1])
  wait_running( instance_id )

  ip = allocate_ip(instance_id)

  set_name( instance_id, 'wss4fe' )
  log( 'wss4fe started at %s' % ip.public_ip )
