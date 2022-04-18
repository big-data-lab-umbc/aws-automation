import json
import boto3
import time
import sys
import os

credentials = ["us-east-2","AKIAZXAV57U5QX4IPSEO","uthG04BZxsptY2ndbZzToCS0zuZBXHOIBWQ9aIQy"]   #region,access_key,secret_key
InstanceId = 'i-0aafdf08fb579c325'

def get_ec2_instances_id(region,access_key,secret_key):
    ec2_conn = boto3.resource('ec2',region_name=region,aws_access_key_id=access_key,aws_secret_access_key=secret_key)
    
    if ec2_conn:
        for instance in ec2_conn.instances.all():
            if instance.state['Name'] == 'running' and instance.security_groups[0]['GroupName'] == 'default':
                masterInstanceId = instance.instance_id
                print("Master Instance Id is ",masterInstanceId)
        return masterInstanceId
    else:
        print('Region failed', region)
        return None
    
    #return InstanceId

def send_command_to_master(InstanceId,command,ssm_client):
    print("Ssm run command: ",command)
    response = ssm_client.send_command(InstanceIds=[InstanceId],DocumentName="AWS-RunShellScript",Parameters={'commands': [command]})

    # command_id = response['Command']['CommandId']
    # waiter = ssm_client.get_waiter("command_executed")

    # while True:
    #     try:
    #         waiter.wait(CommandId=command_id,InstanceId=InstanceId)
    #         break
    #     except:
    #         print("SSM in progress")
    #         time.sleep(5)

    # output = ssm_client.get_command_invocation(CommandId=command_id,InstanceId=InstanceId)
    # if output['Status'] == 'Success':
    #     print('SSM success')
    # else:
    #     print('SSM failed')
        
        
def lambda_handler(event, context):
    #event is PAYLOAD
    masterInstanceId = get_ec2_instances_id(credentials[0],credentials[1],credentials[2])
    ssm_client = boto3.client('ssm',region_name=credentials[0],aws_access_key_id=credentials[1],aws_secret_access_key=credentials[2])
    
    send_command_to_master(masterInstanceId,\
        "docker run --rm -v /home/ubuntu/ML_based_Cloud_Retrieval_Use_Case:/root/ML_based_Cloud_Retrieval_Use_Case starlyxxx/dask-decision-tree-example:latest sh -c 'cd /root/ML_based_Cloud_Retrieval_Use_Case/Code && /usr/bin/python3.6 ml_based_cloud_retrieval_with_data_preprocessing.py >> result.txt'",\
        ssm_client)
    print(event)
    print(context)
    
    # uploadByteStream = bytes(json.dumps(transactionToUpload).encode('UTF-8'))
    # s3.put_object(Bucket=bucket_metadata, Key=fileName, Body=uploadByteStream)
    # print("Hybrid learning Lambda Metadata <%s> sends to <%s>"%(fileName, bucket_metadata))
        
    return {
        'statusCode': 200,
        'body': json.dumps('Action Completed!')
    }


# def s3_put_object(filename,path):
#     return "aws s3 cp /home/ubuntu/%s s3://%s"%(filename,path)
    
# # copy ensemble_result from VM to S3
# send_command_to_master(masterInstanceId,\
#     s3_put_object(event['Configurations']['output_result']["filename"],event['Configurations']['output_result']['bucketname']+"/"+event['Configurations']['output_result']['prefix']),\
#     ssm_client)
# result_version = s3_object_version(event['Configurations']['output_result']["bucketname"],event['Configurations']['output_result']["prefix"])