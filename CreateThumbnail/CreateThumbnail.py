import boto3
import os
import sys
import uuid
from PIL import Image
import PIL.Image
     
s3_client = boto3.client('s3')
     
def resize_image(image_path, resized_path, size):
    with Image.open(image_path) as image:
        image.thumbnail((size, size))
        image.save(resized_path)
     
def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        right_key = key.rsplit('/', 1)[1]
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), right_key)
        upload_path = '/tmp/resized-{}'.format(right_key)
        
        s3_client.download_file(bucket, key, download_path)

        for size in [2500, 1500, 1000, 500, 300, 128]:
            resize_image(download_path, upload_path, size)
            s3_client.upload_file(upload_path, bucket, key.replace('fullSize/', str(size) + '/'))
