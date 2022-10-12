import json
import urllib.parse
import boto3

s3 = boto3.client('s3')
sns = boto3.client('sns')

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    key = urllib.parse.unquote_plus(key, encoding='utf-8')
    eventname = event['Records'][0]['eventName']
    sns_message = str("Status of file has been changed in one of S3 Buckets \n\n BUCKET NAME: "+ bucket +"\n\n FILE NAME: " + key + "\n\n OPERATION: " + eventname + "\n\n")
    try:
        
        if eventname == "ObjectRemoved:Delete":
            sns_message += str("File Deleted")
    
        subject= "S3 Bucket[" + bucket + "] Event[" + eventname + "]"
        sns_response = sns.publish(
        TargetArn='arn:aws:sns:us-west-1:911226616125:S3_bucket_lambda_notification',
        Message= str(sns_message),
        Subject= str(subject)
        )
        
    except Exception as e:
        print('Error getting object {} from bucket {}'.format(key, bucket))
        raise e