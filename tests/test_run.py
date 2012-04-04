ip = "107.21.45.173"

from nose.tools import *

def run(name):

  import urllib
  test = urllib.urlopen("http://%s/%s?test"%(ip,name)).read()

  import re
  res = re.search( ", (\d*) wrong", test )

  return res.groups()

def check_res( name ):
  
  res = run( name )
  eq_( int(res[0]), 0)

def test_run():

  tests = [ 
     "LabTests.RunAgents", 
     "LabTests.MountSqlDb", 
     "LabTests.AdFix.CreateUsers",
     "LabTests.InfoPortal.InstallIp",
  ] 

  for t in tests:
    yield check_res, t
    
