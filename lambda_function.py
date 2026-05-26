import boto3
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

SOURCE_BUCKET = 'manish-incoming-files'
DESTINATION_BUCKET = 'manish-processed-files'

def lambda_handler(event, context):
    try:
        record = event['Records'][0]
        file_name = record['s3']['object']['key']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        logger.info(f"File received: {file_name} at {timestamp}")
        
        copy_source = {
            'Bucket': SOURCE_BUCKET,
            'Key': file_name
        }
        
        s3.copy_object(
            CopySource=copy_source,
            Bucket=DESTINATION_BUCKET,
            Key=file_name
        )
        
        logger.info(f"Successfully moved {file_name} to {DESTINATION_BUCKET} at {timestamp}")
        
        return {
            'statusCode': 200,
            'body': f'File {file_name} successfully moved at {timestamp}'
        }
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise e