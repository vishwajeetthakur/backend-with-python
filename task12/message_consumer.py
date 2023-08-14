import boto3 
sqs = boto3.client('sqs')

queue_url = "https://sqs.us-east-1.amazonaws.com/031901161230/video-queue"


def process_message(message_body):
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ")
    print(f"Processing Message : {message_body}")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ")


while True:
    response = sqs.receive_message(
        QueueUrl=queue_url,
        WaitTimeSeconds=20,
        MaxNumberOfMessages=1
    )

    # print(response)
    if "Messages" in response:
        process_message(response['Messages'][0]['Body'])
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=response['Messages'][0]['ReceiptHandle'])
    else:
        print("XXXXXXXXXXXX No response from SQS XXXXXXXXXXXX ")
    
    # break
    
