# Distributed ML on AWS Cloud: Computing with CPUs and GPUs     

## Introduction
Instead of buying, owning, and maintaining physical data centers and servers, you can access technology services (such as computing power, storage, and databases) from a cloud provider like Amazon Web Services (AWS), Microsoft Azure, Google Cloud, ...

This git help you achieve single machine computation and distributed (multiple) machine computation on AWS, with both CPU and GPU execution.

## Web based

1. Launch instances on [EC2 console](https://us-west-2.console.aws.amazon.com/ec2/v2/home):   
<p align="center"><img src="docs/launchvms.png"/></p>

2. Choose an Amazon Machine Image (AMI)  
An AMI is a template that contains the software configuration (operating system, application server, and applications) required to launch your instance.
For CPU applications, we use Ubuntu Server 16.04 LTS (HVM), SSD Volume Type; for GPU case, we use Deep Learning Base AMI (Ubuntu 16.04) Version 40.0.  
<p align="center"><img src="docs/ami.png"/></p>

3. Choose an Instance Type  
Based on your purpose, AWS provides various instance types on [https://aws.amazon.com/ec2/instance-types/](https://aws.amazon.com/ec2/instance-types/). For CPU application, we recommand to use c5.2xlarge instance; For GPU application, we recommand to use p3.2xlarge instance.
<p align="center"><img src="docs/vmtype.png"/></p>

4. Configure Number of instances  
We use 1 instance for single machine computation, and 2 instances for distributed computation.
<p align="center"><img src="docs/instancenumber.png"/></p>

5. Configure Security Group
<p align="center"><img src="docs/sg.png"/></p>

6. Review, Create your SSH key pair, and Launch
<p align="center"><img src="docs/keypair.png"/></p>

7. View your Instance and wait for Initialing
<p align="center"><img src="docs/status.png"/></p>

8. SSH into your instance
<p align="center"><img src="docs/ssh.png"/></p>

9. Install Docker and download Docker images
CPU example:
```bash
docker pull starlyxxx/dask-decision-tree-example
```

GPU example:
```bash
docker pull starlyxxx/horovod-pytorch-cuda10.1-cudnn7
```

10. Download source data and code on AWS S3
CPU example:
```bash
aws s3 cp s3://kddworkshop/ML_based_Cloud_Retrieval_Use_Case.zip ./
```

GPU example:
```bash
aws s3 cp s3://kddworkshop/MultiGpus-Domain-Adaptation-main.zip ./
aws s3 cp s3://kddworkshop/office31.tar.gz ./
```

11. Run programs on docker containers

For a closer look, please refer to our [presentation](https://github.com/AI-4-atmosphere-remote-sensing/aws-automation/blob/main/docs/NASA%20ACCESS%20AWS%20Cloud%20Presentation.pptx.pdf).

## Command line automation via Boto
Follow steps below for automating single machine computation. For distributed machine computation, see README on each example's sub-folder.  

### Prerequisites:  
```bash
pip install boto fabric2 scanf IPython invoke
pip install Werkzeug --upgrade
```

1. Configuration

Use your customized configurations. Replace default values in ./config/config.ini  
   
2. Start IPython   
```bash
python3 run_interface.py 
```

3. Launch VMs on EC2
```bash
LaunchInstances()
```
4. Install required packages on VMs
```bash
InstallDeps() 
```

5. Automatically run Single VM ML Computing 
```bash
RunSingleVMComputing() 
```
  
6. Terminate all VMs on EC2
```bash
TerminateAll() 
```    
