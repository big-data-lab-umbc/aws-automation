import boto3
# import base64

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    data = s3.get_object(Bucket='apigateway-call-test', Key='result.txt')
    # data = s3.get_object(Bucket='apigateway-call-test', Key='tags.png')
    # print(data)
    # contents = data['Body'].read().decode('utf-8').splitlines()
    contents = data['Body'].read()
    # print(contents)
    
    # return {
    #     # 'statusCode': 200,
    #     "headers":{"Content-Type": "application/pdf"},
    #     'body': base64.b64encode(contents),
    #     'isBase64Encoded': True
    #     # 'body': json.dumps('downloaded!')    }
    
    return contents