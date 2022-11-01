import json, boto3, time, sys, os
from datetime import datetime
from botocore.vendored import requests

credentials = ["us-west-2","your-access-key","your-secret-key"]   #region,access_key,secret_key
InstanceId = 'i-0b83239ada0a8ae1d' 

def get_ec2_instances_id(region,access_key,secret_key):
    ec2_conn = boto3.resource('ec2',region_name=region,aws_access_key_id=access_key,aws_secret_access_key=secret_key)
    
    if ec2_conn:
        for instance in ec2_conn.instances.all():
            if instance.state['Name'] == 'running' and instance.security_groups[0]['GroupName'] == 'your-security-group-name': ## i.e., default, distributed_dl
                masterInstanceId = instance.instance_id
        return masterInstanceId
    else:
        print('Region failed', region)
        return None

def copy_file_to_s3_with_unique_name(InstanceId,ssm_client):
    command = "aws s3 cp --acl public-read /home/ec2-user/cloud-phase-prediction-main/saved_model s3://ai-4-atmosphere-remote-sensing/cloud-phase-prediction_result' '$(date +'%Y-%m-%d_%H:%M:%S.%s')/ --recursive"
    response = ssm_client.send_command(InstanceIds=[InstanceId],DocumentName="AWS-RunShellScript",Parameters={'commands': [command]})
    command_id = response['Command']['CommandId']
    # waiter = ssm_client.get_waiter("command_executed")
    # waiter.wait(CommandId=command_id,InstanceId=InstanceId)

def send_command_to_master(masterInstanceId,command_id,ssm_client):
    output = ssm_client.get_command_invocation(CommandId=command_id,InstanceId=masterInstanceId)
    
    if output['Status'] == 'Success':
        copy_file_to_s3_with_unique_name(masterInstanceId,ssm_client)
        
        html = '''<!DOCTYPE html>
        <html>
                <head>
                    <meta http-equiv="refresh" content="0; url='https://s3.amazonaws.com/ai-4-atmosphere-remote-sensing/index.html'" />
                </head>
        
        </html>'''
    
        return {
            # 'statusCode': 200,
            'body': html,
                'headers': {'Content-Type': 'text/html'}
        }
        
    elif output['Status'] == 'Failed':
        message = '''the process was failed'''
        return {
            'body': message,
            'headers': {'Content-Type': 'text/html'}
        }
        
    elif output['Status'] == 'InProgress':
        message = '''the process is still running'''
        return {
            'body': message,
            'headers': { 'Content-Type': 'text/html'}
        }
    
def lambda_handler(event, context):
    # print("here is the event", event)
    # params = event['queryStringParameters']
    masterInstanceId = get_ec2_instances_id(credentials[0],credentials[1],credentials[2])
    ssm_client = boto3.client('ssm',region_name=credentials[0],aws_access_key_id=credentials[1],aws_secret_access_key=credentials[2])
    
    command_id = event['queryStringParameters']['command_id']
    return send_command_to_master(masterInstanceId, command_id, ssm_client)