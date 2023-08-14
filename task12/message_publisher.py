import boto3
import random
import time

# Create SQS client
sqs = boto3.client('sqs')

# creating sqs queue

# Create SQS client
# sqs = boto3.client('sqs')

# Create a SQS queue
response = sqs.create_queue(
    QueueName='video-queue',
    Attributes={
        'DelaySeconds': '60',
        'MessageRetentionPeriod': '86400'
    }
)

# print("quque url : ", response['QueueUrl'])

# get Queue URL

queue_url = response['QueueUrl'] 
queue_url = "https://sqs.us-east-1.amazonaws.com/031901161230/video-queue" 

count = 0 
while count < 10 :
    msg = f"testing {random.randint(10, 100)}"
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageAttributes={
            'Title': {
                'DataType': 'String',
                'StringValue': 'The Whistler'
            },
            'Author': {
                'DataType': 'String',
                'StringValue': 'Vishwajeet Thakur'
            },
        },
        MessageBody=(
            msg
        )
    )

    count += 1

    print(msg)
    time.sleep(15)
    # break





