import json, boto3, time, sys, os

credentials = ["us-west-2","your-access-key","your-secret-key"]   #region,access_key,secret_key
InstanceId = 'i-0b83239ada0a8ae1d' ## EC2 instance ID

def get_ec2_instances_id(region,access_key,secret_key):
    ec2_conn = boto3.resource('ec2',region_name=region,aws_access_key_id=access_key,aws_secret_access_key=secret_key)
    
    if ec2_conn:
        for instance in ec2_conn.instances.all():
            if instance.state['Name'] == 'running' and instance.security_groups[0]['GroupName'] == 'your-security-group-name': ## i.e., default, distributed_dl
                masterInstanceId = instance.instance_id
                print("Master Instance Id is ",masterInstanceId)
        return masterInstanceId
    else:
        print('Region failed', region)
        return None

def send_command_to_master(InstanceId,command,ssm_client):
    response = ssm_client.send_command(InstanceIds=[InstanceId],DocumentName="AWS-RunShellScript",Parameters={'commands': [command]})
    
    cmdId = response['Command']['CommandId']
    return cmdId

def lambda_handler(event, context):
    masterInstanceId = InstanceId 
    ssm_client = boto3.client('ssm',region_name=credentials[0],aws_access_key_id=credentials[1],aws_secret_access_key=credentials[2])
    
    output = send_command_to_master(masterInstanceId,\
        "cd /home/ec2-user/DL_3d_cloud_retrieval-main && mkdir -p outputs && /usr/bin/python3.8 COT_retrieval/test_example.py --cot_file_name=example/training_data/data_cot.h5 --path_1d_retrieval=example/retrieved_COT/ --path_model=saved_model/lstm/model1.h5 --path_predictions=outputs/ --radiance_test=example/testing_data/X_test_1.npy --cot_test=example/testing_data/y_test_1.npy --path_plots=outputs/",\
        ssm_client)
        
    return 'https://jldgsfljne.execute-api.us-west-2.amazonaws.com/default/seraj_call_url_long_services?command_id='+output ## the https//...is the service2 API called by this service1 API