# Web based Execution on a Single CPU with Script
The machine learning application in this page uses a decision tree based cloud property retrieval from remote sensing data.

1. Launch instances on [EC2 console](https://us-west-2.console.aws.amazon.com/ec2/v2/home):   
<p align="center"><img src="../docs/launchvms.png"/></p><br/>

2. Choose an Amazon Machine Image (AMI)  
  An AMI is a template that contains the software configuration (operating system, application server, and applications) required to launch your instance.
  For CPU applications, we use **Ubuntu Server 20.04 LTS (HVM), SSD Volume Type**.  



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

9. Copy [bootstrap.sh](bootstrap.sh) to your instance, and run the script
```bash
sudo bash bootstrap.sh
```

10. Run ML CPU application:

    ```bash
    cd ML_based_Cloud_Retrieval_Use_Case/Code && /usr/bin/python3.6 ml_based_cloud_retrieval_with_data_preprocessing.py
    ```

11. Run application via Jupyter Notebook (optional):

    ```bash
    pip3 install jupyterlab
    jupyter-lab --ip=*
    ```
    Now you can open your web browser to open JuypterLab based on it domain name and Jupyter token. Here is an example is http://ec2-54-186-96-63.us-west-2.compute.amazonaws.com:8888/?token=b9143e017355e42660cbed9f269793fba8837a6f0c0f03ef

12. Terminate the virtual machine on EC2 when finishing experiments.
<p align="center"><img src="../docs/terminate.png"/></p>
