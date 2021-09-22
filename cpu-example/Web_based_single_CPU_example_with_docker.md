# Web based Execution with Docker     
Web based


1. Launch instances on [EC2 console](https://us-west-2.console.aws.amazon.com/ec2/v2/home):   
<p align="center"><img src="../docs/launchvms.png"/></p><br/>

2. Choose an Amazon Machine Image (AMI)  
An AMI is a template that contains the software configuration (operating system, application server, and applications) required to launch your instance.
For CPU applications, we use Ubuntu Server 16.04 LTS (HVM), SSD Volume Type.  



3. Choose an Instance Type  
Based on your purpose, AWS provides various instance types on [https://aws.amazon.com/ec2/instance-types/](https://aws.amazon.com/ec2/instance-types/). For CPU application, we recommand to use c5.2xlarge instance.
<p align="center"><img src="../docs/vmtype.png"/></p><br/>

4. Configure Number of instances  
We use 1 instance for single machine computation.
<p align="center"><img src="../docs/instancenumber.png"/></p><br/>

5. Configure Security Group
<p align="center"><img src="../docs/sg.png"/></p><br/>

6. Review, Create your SSH key pair, and Launch
<p align="center"><img src="../docs/keypair.png"/></p><br/>

7. View your Instance and wait for Initialing
<p align="center"><img src="../docs/status.png"/></p><br/>

8. SSH into your instance
<p align="center"><img src="../docs/ssh.png"/></p><br/>

9. Install [Docker](https://docs.docker.com/engine/install/ubuntu/)
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo service docker start
sudo usermod -a -G docker ubuntu
sudo chmod 666 /var/run/docker.sock
```
<br/>

10. Download [Docker images](https://hub.docker.com/u/starlyxxx) or build images by Dockerfile.

```bash
docker pull starlyxxx/dask-decision-tree-example
```
or, build from Dockerfile:

```bash
docker build -t <your-image-name>
```
<br/>

11. Download ML applications and data on AWS S3.
- For privacy, we store the application code and data on AWS S3. Install aws cli and [set aws credentials](https://console.aws.amazon.com/iam/home?#/security_credentials).
```bash
curl 'https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip' -o 'awscliv2.zip'
unzip awscliv2.zip
sudo ./aws/install
aws configure set aws_access_key_id your-access-key
aws configure set aws_secret_access_key your-secret-key
```
- Download ML applications and data on AWS S3.
  Download:

  ```bash
  aws s3 cp s3://kddworkshop/ML_based_Cloud_Retrieval_Use_Case.zip ./
  ```
  or
  ```bash
  (wget https://kddworkshop.s3.us-west-.amazonaws.com/ML_based_Cloud_Retrieval_Use_Case.zip)
  ```
  Extract the files:
  ```bash
  ML_based_Cloud_Retrieval_Use_Case.zip
  ```
  <br/>

12. Run docker containers for CPU applications.
- Single CPU:
```bash
docker run -it -v /home/ubuntu/ML_based_Cloud_Retrieval_Use_Case:/root/ML_based_Cloud_Retrieval_Use_Case starlyxxx/dask-decision-tree-example:latest /bin/bash
```
<br/>

13. Run ML CPU application:

```bash
cd ML_based_Cloud_Retrieval_Use_Case/Code && /usr/bin/python3.6 ml_based_cloud_retrieval_with_data_preprocessing.py
```
  <br/>

14. Terminate the virtual machine on EC2 when finishing experiments.

<p align="center"><img src="../docs/terminate.png"/></p>
<br/>

