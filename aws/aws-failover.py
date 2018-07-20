#!/usr/bin/env python2.7
__author__ = "Rohit Chormale"


"""
Description - AWS Failover script to migrate traffic from one instance to another.
Dependancies - python2.7, pip2.7, awscli
Installation - pip2.7 install awscli
Usage:
    # Configure aws using below command. Required details can be found in AWS IAM service
    aws configure

    # Make script executable
    chmod ugo+x aws-failover.py

    # Add main instance-id, fallback instance-id and floating-ip below.
     Optional - If both instances have elastic ips by default, mention them below (eip1 and eip2) to retain them back, once floating ip is re-assigned.
     Make sure these default ips are allowed to reassociate when attached. 
     This can be achieved by enabling 'Allow Elastic IP to be reassociated if already attached' option in Elastic IP Settings

    # for help
    ./aws-failover.py --help
    
    # To setup fallback instance
    ./aws-failover.py --fallback

    # To setup main instance
    ./aws-failover.py --main

Supporting OS: CentOS 7
"""


import os

# main instance id
instance1 = "" 

# fallback instance id
instance2 = ""

# floating ip - This  ip will float in between both instances
fip = ""

# Optional - If both instances have elastic ips by default, mentioned them here to retain them back, once floating ip is re-assigned.
# Make sure these default ips are allowed to reassociate when attached. 
# This can be achieved by enabling 'Allow Elastic IP to be reassociated if already attached' option in Elastic IP Settings
eip1 = ""
eip2 = ""


assign_eip1_instance1 = "aws ec2 associate-address --instance-id %s --public-ip %s --allow-reassociation" %(instance1, eip1)
assign_eip2_instance2 = "aws ec2 associate-address --instance-id %s --public-ip %s --allow-reassociation" %(instance2, eip2)
assign_fip_instance1 = "aws ec2 associate-address --instance-id %s --public-ip %s --allow-reassociation" %(instance1, fip)
assign_fip_instance2 = "aws ec2 associate-address --instance-id %s --public-ip %s --allow-reassociation" %(instance2, fip)


def setup_fallback_instance():
    """Move to fallback instance"""
    os.system(assign_fip_instance2)
    if eip1:
        os.system(assign_eip1_instance1)


def setup_main_instance():
    """Move to main instance"""
    os.system(assign_fip_instance1)
    if eip2:
        os.system(assign_eip2_instance2)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="AWS Failover Tool")
    ap.add_argument("--main", help="Move to main node", action="store_true", default=False)
    ap.add_argument("--fallback", help="Move to fallback node", action="store_true", default=False)
    args = vars(ap.parse_args())
    if args["fallback"]:
        setup_fallback_instance()
    if args["main"]:
        setup_main_instance()
