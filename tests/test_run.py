import sys
ip = sys.argv[2]

from nose.tools import *

def run(name):

  import urllib
  test = urllib.urlopen("http://%s/%s?test"%(ip,name)).read()

  import re
  res = re.search( ", (\d*) wrong", test )

  return (res.groups(),test)

def check_res( name ):
  
  res = run( name )
  eq_( int(res[0][0]), 0, res[1])

def test_run():

  tests = [ 
     "LabTests.RunAgents", 
     "LabTests.MountSqlDb", 
     "LabTests.AdFix.CreateUsers",
     "LabTests.InfoPortal.InstallIp",
  ] 

  for t in tests:
    yield check_res, t

def test_wait_setup():

  import time
  
  for i in range(0,10):

    time.sleep( 5 )
    res = run("LabTests.InfoPortal.IsInstalled")

    if int(res[0][0]) == 0: 
      return

  ok_( False )
    
def test_fix_ip(): 

  check_res( "LabTests.InfoPortal.FixIp" )
