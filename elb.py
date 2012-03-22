#!/usr/bin/python

import boto

elb = boto.connect_elb()
phabricator = elb.get_all_load_balancers()[0]

import sys
phabricator.register_instances( sys.argv[1] )
