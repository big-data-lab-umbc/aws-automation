# Web based Execution with Docker     
Web based


1. Launch instances on [EC2 console](https://us-west-2.console.aws.amazon.com/ec2/v2/home):   
<p align="center"><img src="../docs/launchvms.png"/></p><br/>

2. Choose an Amazon Machine Image (AMI)  
An AMI is a template that contains the software configuration (operating system, application server, and applications) required to launch your instance.
For GPU case, we use Deep Learning Base AMI (Ubuntu 16.04) Version 40.0.  
<p align="center"><img src="../docs/ami.png"/></p><br/>

3. Choose an Instance Type  
    Based on your purpose, AWS provides various instance types on [https://aws.amazon.com/ec2/instance-types/](https://aws.amazon.com/ec2/instance-types/). For GPU application, we recommand to use p3.2xlarge instance.

  

4. Configure Number of instances  
We use 2 instances for distributed computation.
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

- GPU example:
```bash
docker pull starlyxxx/horovod-pytorch-cuda10.1-cudnn7
```
- or, build from Dockerfile:
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
aws s3 cp s3://kddworkshop/MultiGpus-Domain-Adaptation-main.zip ./
aws s3 cp s3://kddworkshop/office31.tar.gz ./
```
​        or
```bash
wget https://kddworkshop.s3.us-west-2.amazonaws.com/MultiGpus-Domain-Adaptation-main.zip
wget https://kddworkshop.s3.us-west-2.amazonaws.com/office31.tar.gz
```
​        Extract the files:
```bash
unzip MultiGpus-Domain-Adaptation-main.zip
tar -xzvf office31.tar.gz
```
<br/>

12. Run docker containers for GPU applications

- Add primary worker’s public key to all secondary workers’ <~/.ssh/authorized_keys>
```bash
sudo mkdir -p /mnt/share/ssh && sudo cp ~/.ssh/* /mnt/share/ssh
```
- Primary worker VM:
```bash
nvidia-docker run -it --network=host -v /mnt/share/ssh:/root/.ssh -v /home/ubuntu/MultiGpus-Domain-Adaptation-main:/root/MultiGpus-Domain-Adaptation-main -v /home/ubuntu/office31:/root/office31 starlyxxx/horovod-pytorch-cuda10.1-cudnn7:latest /bin/bash
```
- Secondary workers VM:
```bash
nvidia-docker run -it --network=host -v /mnt/share/ssh:/root/.ssh -v /home/ubuntu/MultiGpus-Domain-Adaptation-main:/root/MultiGpus-Domain-Adaptation-main -v /home/ubuntu/office31:/root/office31 starlyxxx/horovod-pytorch-cuda10.1-cudnn7:latest bash -c "/usr/sbin/sshd -p 12345; sleep infinity"
```
<br/>  

13. Run ML GPU application

- Primary worker VM:
```bash
cd MultiGpus-Domain-Adaptation-main
```
```bash
horovodrun --verbose -np 2 -H <machine1-address>:1,<machine2-address>:1 -p 12345 /usr/bin/python3.6 main.py --config DeepCoral/DeepCoral.yaml --data_dir ../office31 --src_domain webcam --tgt_domain amazon
```
<br/>

14. Terminate all VMs on EC2 when finishing experiments.

<p align="center"><img src="../docs/terminate.png"/></p>
<br/>
