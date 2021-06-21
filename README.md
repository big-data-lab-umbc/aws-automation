################  
### Distributed DL Automation on AWS  
################  
  
1. Get your own Access key and Secret key:   
    Go to account -> My security credentials -> Dashboard -> rotate your access key, create new access key, download the file (accessKeys.csv).  
  
2. Get your own key pair:  
    (https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#having-ec2-create-your-key-pair)  
	Go to EC2 -> Network security -> key pairs, create key pair, download the file (your_key_pair.pem).  
	Move to its path, and $chmod 400 your_key_pair.pem  
    Move file to .ssh folder: $mv path_to_key_pair .ssh  
  
3. Make a little change:  
    For run_interface.py, use your customized configuration. Replace default values in ./config/config.ini  
  
4. Start Distributed DL Step by Step:
    $python3 run_interface.py  
    $LaunchInstances()  
    $InstallDeps()  
    $RunDL()  
    $TerminateAll()  
