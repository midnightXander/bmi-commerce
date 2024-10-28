import boto3
s3 = boto3.client('s3',
                  aws_access_key_id = '#',
                  aws_secret_access_key = '#'
                  )

s3.upload_file('test.txt', 'bmiecommercebuckets','test.txt')

print('done')