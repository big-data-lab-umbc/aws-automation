"""
Author: Xin Wang. Phd Student. University of Maryland, Baltimore County
Date: 08/24/2021
"""

import boto.ec2
import sys, os
import time
from subprocess import check_output, Popen, call, PIPE, STDOUT
import fcntl
import platform
import configparser
import json

configFile = "config/config.ini"
emrConfigFile = "config/emr-configuration-ecr-public.json"

def readsummary(): 
    config = configparser.ConfigParser()
    config.read(configFile)
    return (str(config['summary']['your_key_path']),str(config['summary']['your_key_name']),str(config['summary']['access_key']),str(config['summary']['secret_key']),str(config['summary']['git_link']),str(config['summary']['runtime_application']))

def readaws():
    config = configparser.ConfigParser() 
    config.read(configFile)
    return (int(config['aws']['TOTAL_INSTANCE']),str(config['aws']['SUBNET_ID']),str(config['aws']['INSTANCE_TYPE']),str(config['aws']['REGION']),str(config['aws']['SECURITY_GROUP_ID']),str(config['aws']['VPC_ID']))

your_key_path, your_key_name, access_key, secret_key, git_link, runtime_application = readsummary()  #str
TOTAL_INSTANCE, SUBNET_ID, INSTANCE_TYPE, REGION, SECURITY_GROUP_ID, VPC_ID = readaws() #int,str

if not boto.config.has_section('ec2'):
    boto.config.add_section('ec2')
    boto.config.setbool('ec2','use-sigv4',True)

secgroups = {
    REGION:SECURITY_GROUP_ID, 
}
subnets = {
    REGION:SUBNET_ID,
}
regions = sorted(secgroups.keys())[::-1]
NameFilter = 'AWS-Setup'
    
def get_ec2_instances_ip(region):
    ec2_conn = boto.ec2.connect_to_region(region,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key)
    if ec2_conn:
        result = []
        reservations = ec2_conn.get_all_reservations(filters={'tag:Name': NameFilter})
        for reservation in reservations:
            if reservation:       
                for ins in reservation.instances:
                    if ins.public_dns_name: 
                        currentIP = ins.public_dns_name.split('.')[0][4:].replace('-','.')
                        result.append(currentIP)
                        print(currentIP)
        return result
    else:
        print('Region failed.', region)
        return None

def get_ec2_instances_id(region):
    ec2_conn = boto.ec2.connect_to_region(region,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key)
    if ec2_conn:
        result = []
        reservations = ec2_conn.get_all_reservations(filters={'tag:Name': NameFilter})
        for reservation in reservations:    
            for ins in reservation.instances:
                print(ins.id)
                result.append(ins.id)
        return result
    else:
        print('Region failed.', region)
        return None

def terminate_all_instances(region):
    ec2_conn = boto.ec2.connect_to_region(region,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key)
    idList = []
    if ec2_conn:
        reservations = ec2_conn.get_all_reservations(filters={'tag:Name': NameFilter})
        for reservation in reservations:   
            if reservation:    
                for ins in reservation.instances:
                    idList.append(ins.id)
        ec2_conn.terminate_instances(instance_ids=idList)

def LaunchInstances():
    ec2_conn = boto.ec2.connect_to_region(REGION,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key)
    dev_sda1 = boto.ec2.blockdevicemapping.EBSBlockDeviceType(delete_on_termination=True)
    dev_sda1.size = 8 # size in Gigabytes
    dev_sda1.delete_on_termination = True
    bdm = boto.ec2.blockdevicemapping.BlockDeviceMapping()
    bdm['/dev/sda1'] = dev_sda1
    img = ec2_conn.get_all_images(filters={'name':'Deep Learning Base AMI (Ubuntu 16.04) Version 40.0'})[0].id
    #img = "ami-09b07024e0b31501d"
    reservation = ec2_conn.run_instances(image_id=img,
                                 min_count=TOTAL_INSTANCE,
                                 max_count=TOTAL_INSTANCE,
                                 key_name=your_key_name, 
                                 instance_type=INSTANCE_TYPE,
                                 security_group_ids = [secgroups[REGION], ],
                                 subnet_id = subnets[REGION])                          
    print (type(reservation.instances))
    for instance in reservation.instances:
        instance.add_tag("Name", NameFilter)
    return reservation

def ipAll():
    result = []
    for region in regions:
        result += get_ec2_instances_ip(region) or []
    open('public_ip','w').write('\n'.join(result))
    return result

def getIP():
    return [l for l in open('public_ip', 'r').read().split('\n') if l]

def idAll():
    result = []
    for region in regions:
        result += get_ec2_instances_id(region) or []
    return result

def join_get(l,sep):
    if isinstance(l,list):
        output = []
        for i in l:
            output.append('ubuntu@'+i)
        return sep.join(output)
    if isinstance(l,str):
        return 'ubuntu@'+l

def join_getlist(l):
    output = []
    if isinstance(l,list):
        for i in l:
            output.append('ubuntu@'+i)
    if isinstance(l,str):
        output.append('ubuntu@'+l)
    return output

def callFabFromIPList(l, work):
    print('fab -r %s -i %s -H %s %s' % ("./"+runtime_application+"/",your_key_path, join_get(l,','), work))
    call('fab -r %s -i %s -H %s %s' % ("./"+runtime_application+"/",your_key_path, join_get(l,','), work), shell=True)

c = callFabFromIPList

def RunSingleVMComputing():
    c(getIP()[0], 'start %s %s %s'%(git_link,access_key,secret_key))

def InstallDeps():
    result = []    
    for region in regions:
        result += get_ec2_instances_ip(region) or []
    open('public_ip','w').write('\n'.join(result))

    # bashfilename = "scripts/runInstallDeps.sh"
    # ips = join_getlist(getIP())
    # work = 'installDeps %s %s %s'%(git_link,access_key,secret_key)
    # f = open(bashfilename,"w")
    # f.write("#!/bin/bash\n\n")
    # for i in range(len(ips)):
    #     f.write('fab -r %s -i %s -H %s %s&\n' % ("./"+runtime_application+"/",your_key_path, ips[i], work))
    # f.close()

    # try:
    #     popen = Popen('./%s'%bashfilename)
    # except:
    #     popen = Popen(['bash',bashfilename])

    c(getIP(), 'installDeps %s %s %s'%(git_link,access_key,secret_key))

def TerminateAll():
    c(getIP(), 'addhoc')
    for region in regions:
        terminate_all_instances(region)
    return 'Terminate successfully.'



if  __name__ =='__main__':
  try: __IPYTHON__
  except NameError:

    import IPython
    IPython.embed()

