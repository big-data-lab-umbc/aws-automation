# Web based Execution on a Single CPU with Script
The application in this page explains how to collocate remote sensing data from multiple satellites. We mainly use the [satellite_collocation library](https://github.com/AI-4-atmosphere-remote-sensing/satellite_collocation).

1. (Optional) Upload raw data and code to be collocated to S3 if they have not been uploaded to S3 yet:
    ```bash   
    aws s3 cp --recursive CALIPSO-L2-01km-CLayer s3://ai-4-atmosphere-remote-sensing/CALIPSO-L2-01km-CLayer
    aws s3 cp --recursive VNP02MOD-VIIRS-Attributes s3://ai-4-atmosphere-remote-sensing/VNP02MOD-VIIRS-Attributes
    aws s3 cp --recursive VNP03MOD-VIIRS-Coordinates s3://ai-4-atmosphere-remote-sensing/VNP03MOD-VIIRS-Coordinates
    aws s3 cp /Users/jianwu/Downloads/satellite_collocation-main.zip s3://ai-4-atmosphere-remote-sensing
    aws s3 cp /Users/jianwu/Data/satellite_collocation_sample_data.zip s3://ai-4-atmosphere-remote-sensing
    ```

1. Launch instances on [EC2 console](https://us-west-2.console.aws.amazon.com/ec2/v2/home):   
<p align="center"><img src="../../docs/launchvms.png"/></p><br/>

2. Choose an Amazon Machine Image (AMI)  
  An AMI is a template that contains the software configuration (operating system, application server, and applications) required to launch your instance.
  For CPU applications, we use **Ubuntu Server 20.04 LTS (HVM), SSD Volume Type**.  



3. Choose an Instance Type  
Based on your purpose, AWS provides various instance types on [https://aws.amazon.com/ec2/instance-types/](https://aws.amazon.com/ec2/instance-types/). For CPU application, we recommand to use c5.2xlarge instance.
<p align="center"><img src="../../docs/vmtype.png"/></p><br/>

4. Configure Number of instances  
We use 1 instance for single machine computation.
<p align="center"><img src="../../docs/instancenumber.png"/></p><br/>

5. Configure Security Group
<p align="center"><img src="../../docs/sg.png"/></p><br/>

6. Review, Create your SSH key pair, and Launch
<p align="center"><img src="../../docs/keypair.png"/></p><br/>

7. View your Instance and wait for Initialing
<p align="center"><img src="../../docs/status.png"/></p><br/>

8. SSH into your instance
<p align="center"><img src="../../docs/ssh.png"/></p><br/>

9. Copy [bootstrap.sh](bootstrap.sh) to your instance, and run the script
```bash
sudo bash bootstrap.sh
```

10. Run ML CPU application:

    ```bash
    cd /home/ubuntu/satellite_collocation-main && python3 examples/collocate_viirs_calipso_dask_cluster/collocation_dask_local.py -tp ../satellite_collocation_sample_data/CALIPSO-L2-01km-CLayer/ -sgp ../satellite_collocation_sample_data/VNP03MOD-VIIRS-Coordinates/ -sdp ../satellite_collocation_sample_data/VNP02MOD-VIIRS-Attributes/ -sp ../satellite_collocation_sample_data/collocation-output-2/
    ```

12. Terminate the virtual machine on EC2 when finishing experiments.
<p align="center"><img src="../../docs/terminate.png"/></p>
