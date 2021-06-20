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
def installDeps(conn):
    conn.sudo('apt-get update')
    conn.sudo('apt install -y software-properties-common')
    conn.sudo('add-apt-repository -y ppa:deadsnakes/ppa')
    conn.sudo('apt-get update')
    conn.sudo('rm /usr/local/cuda')
    conn.sudo('ln -s /usr/local/cuda-10.1 /usr/local/cuda')
    conn.sudo('apt-get -y install python3.6')
    conn.run("echo alias python3='/usr/bin/python3.6' >> ~/.bashrc")
    conn.run('echo export CUDA_HOME=/usr/local/cuda >> ~/.bashrc')
    conn.run('echo export PATH=$PATH:/home/ubuntu/bin:/home/ubuntu/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/local/bin:/usr/local/cuda/bin >> ~/.bashrc')
    conn.run('echo export LD_LIBRARY_PATH=/usr/local/cuda/lib64:/home/ubuntu/cuda/lib64:/usr/local/cuda-10.1/lib64:/usr/local/cuda-10.1/targets/x86_64-linux/lib:/usr/local/cuda/extras/CUPTI/lib64:/usr/local/lib:/usr/local/cuda-10.2/targets/x86_64-linux/lib:/home/ubuntu/.local/lib:$LD_LIBRARY_PATH >> ~/.bashrc')
    conn.run('source ~/.bashrc')
    conn.sudo('apt-get -y install python3.6-gdbm')

    conn.sudo('apt-get -y install git')
    conn.sudo('apt-get -y install wget')
    conn.sudo('apt-get -y install python3-pip')
    conn.sudo('/usr/bin/python3.5 -m pip uninstall pip')
    conn.sudo('/usr/bin/python3 -m pip uninstall pip')
    conn.sudo('python3 -m pip install --upgrade pip setuptools')
    conn.run('pip3 install tensorflow==2.2.0')
    conn.run('pip3 install cmake')
    conn.run('pip3 install keras')
    conn.run('pip3 install pandas')
    conn.run('pip3 install captum')
    conn.run('pip3 install sklearn')
    conn.run('pip3 install awscliv2')

    conn.run('wget https://download.open-mpi.org/release/open-mpi/v4.0/openmpi-4.0.0.tar.gz')
    conn.run('tar -xzvf openmpi-4.0.0.tar.gz')
    with conn.cd('openmpi-4.0.0'):
        conn.run('./configure --prefix=/usr/local/')
        conn.sudo('make all install')
    conn.sudo('apt update')
    conn.sudo('apt-get update')
    conn.run('wget https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64/libnccl-dev_2.4.7-1+cuda10.1_amd64.deb')
    conn.run('wget https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64/libnccl2_2.4.7-1+cuda10.1_amd64.deb')
    conn.sudo('dpkg -i libnccl2_2.4.7-1+cuda10.1_amd64.deb')
    conn.sudo('dpkg -i libnccl-dev_2.4.7-1+cuda10.1_amd64.deb')
    conn.run('HOROVOD_GPU_OPERATIONS=NCCL HOROVOD_WITH_MPI=1 pip install --no-cache-dir horovod[tensorflow,keras]')

    conn.run('pip3 install torch==1.7.0 torchvision==0.8.1 -f https://download.pytorch.org/whl/cu101/torch_stable.html')
    
@task
def start(conn,git_link,access_key,secret_key):

    conn.run('mkdir .aws')
    conn.run('echo [default]\naws_access_key_id=%s\naws_secret_access_key=%s >> ~/.aws/credentials'%(access_key,secret_key))

    try:
        conn.sudo('rm -rf aws-automation')
    except:
        pass
    conn.run('git clone %s'%git_link)
        
    with conn.cd('aws-automation'):
        conn.run('aws s3 cp s3://kddworkshop/train10.npz ./')
        conn.run('aws s3 cp s3://kddworkshop/test_142_day.npz ./')
        conn.run('python3 DistributedDL.py cpu')
        conn.run('python3 DistributedDL.py gpu')