import boto3
from ddaptools.aws_classes.class_enhancement import *
from ddaptools.dda_constants import *
import uuid

sqs = boto3.client('sqs')

# Define the URL of your SQS queue
queue_url = 'https://sqs.us-east-1.amazonaws.com/796522278827/ProcessingQueue.fifo'

def test_enqueue_all():
    # Query all staging events guids
    

    credentials = {
        'USERNAME': "postgres",
        'PASSWORD': "dDueller123araM=!",
        "HOST": "test-ddanalytics-rds-v2.cpcwi20k2qgg.us-east-1.rds.amazonaws.com",
        "DB": "v1_2"
    }
    
    organizationDBProvider = PostgresqlOrganizationQuerier(credentials=credentials)
    all_staging_events_guids = organizationDBProvider.get_all_staging_events_guids(organization_guid='123e4567-e89b-12d3-a456-1231231')
    print(all_staging_events_guids)
    
    message_deduplication_id = str(uuid.uuid4())

    for staging_guid in all_staging_events_guids:
        print("Enqueue: ", staging_guid)
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=staging_guid,
            MessageGroupId=staging_guid,
            MessageDeduplicationId=message_deduplication_id,
        )
        print(response)


