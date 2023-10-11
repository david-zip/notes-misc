import boto3

def lambda_handler(event: dict, context: dict): 
    """
    Delete specifed files in inbound and/or aligned s3 bucket
    
    Expects an dictionary input with the following example format:
    {
        "inbound": ["filename.csv", "filename2.csv", ...],
        "aligned": ["filename.csv", "filename2.csv", ...]
    } 

    Args:
        event (dict): dictionary containing bucket name and filenames to delete
        context (dict): information about lambda function invoked
    """
    s3 = boto3.resource('s3')
    for bucket_name, file_keys in event.items():
        # single delete
        # bucket keys
        
        print(bucket_name)
        
        if not isinstance(file_keys, list):
            file_keys = list(file_keys)
        
        source_bucket = f'gdp-iag-hrdata-prd-datalake-{bucket_name}'
        output_folder = 'HR-DATA/'
        
        # initialise bucket resource
        s3 = boto3.resource('s3')
        bucket=s3.Bucket(source_bucket)
        
        # create bucket contents list
        bucket_contents = []
        for key in bucket.objects.all():
            if key.key.startswith(output_folder):
                bucket_contents.append(key.key)
        
        for file_key in file_keys:
            print(f'File getting deleted: {source_bucket}/{output_folder}{file_key}')
            
            # guard clause
            if f'{output_folder}{file_key}' not in bucket_contents:
                print('File does not exist in the bucket')
                continue
            
            # delete files
            try:
                s3.Object(source_bucket, f'{output_folder}{file_key}').delete() 
                print('File deleted')
            except Exception as error:
                # print error and continue to next file
                print(f'File has not been deleted --> error: {error}')
            else:
                print('Process has finished running')

    return{
        'statusCode':200,
        'body':'Success'
    }

