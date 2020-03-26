import boto3

def upload_to_s3(file_name, bucket, object_name):
   # Upload the file
    s3_client = boto3.client('s3')
    
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        print(e)
        return False
    return True 
