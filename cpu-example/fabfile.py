"""
Author: Xin Wang. Phd Student. University of Maryland, Baltimore County
Date: 08/24/2021
"""

from __future__ import with_statement
from fabric import *
from invoke import task, Exit
from fabric import Connection
import time, sys, os
from io import BytesIO
from fabric import ThreadingGroup as Group


@task
def host_type(conn):
    conn.run('uname -s')

@task
def gettime(conn):
    conn.run('date +%s.%N')

@task
def ping(conn):
    conn.run('ping -c 5 google.com')
    conn.run('echo "synced transactions set"')
    conn.run('ping -c 100 google.com')
    
@task
def addhoc(conn):
    conn.sudo("pkill -9 python")

@task
def installDeps(conn,git_link,aws_access_key_id,aws_secret_access_key):
    conn.run("curl -fsSL https://get.docker.com -o get-docker.sh")
    conn.sudo("sh get-docker.sh")
    conn.sudo("service docker start")
    conn.sudo("usermod -a -G docker ubuntu")
    conn.sudo("chmod 666 /var/run/docker.sock")
    conn.run("docker pull starlyxxx/dask-decision-tree-example")

    conn.run("curl 'https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip' -o 'awscliv2.zip'")
    conn.run("unzip awscliv2.zip")
    conn.sudo("./aws/install")

    conn.run("aws configure set aws_access_key_id %s"%aws_access_key_id)
    conn.run("aws configure set aws_secret_access_key %s"%aws_secret_access_key)

    conn.run("aws s3 cp s3://kddworkshop/ML_based_Cloud_Retrieval_Use_Case.zip ./")
    conn.run("unzip ML_based_Cloud_Retrieval_Use_Case.zip")

@task
def start(conn,git_link,access_key,secret_key):
    conn.run("docker run -v /home/ubuntu/ML_based_Cloud_Retrieval_Use_Case:/root/ML_based_Cloud_Retrieval_Use_Case -d starlyxxx/dask-decision-tree-example:latest")
    conn.run('docker exec -it starlyxxx/dask-decision-tree-example:latest cd ML_based_Cloud_Retrieval_Use_Case/Code && /usr/bin/python3.6 ml_based_cloud_retrieval_with_data_preprocessing.py')
