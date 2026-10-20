import boto3
import json
import os

def lambda_handler(event, context):
    # Pega do ENV do K8s, se não tiver, usa o padrão
    endpoint = os.getenv('S3_ENDPOINT', 'http://localstack.infra.svc.cluster.local:4566')
    ambiente = os.getenv('AMBIENTE', 'dev')

    s3 = boto3.client('s3', 
        endpoint_url=endpoint,
        aws_access_key_id='test',
        aws_secret_access_key=os.getenv('AWS_SECRET'),
        region_name='us-east-1'
    )

    try:
        buckets = s3.list_buckets()
        s3_status = f"Bucket meu-bucket-teste OK - {len(buckets['Buckets'])} buckets"
    except Exception as e:
        s3_status = f"Erro S3: {str(e)}"

    body = json.loads(event.get('body', '{}')) if isinstance(event.get('body'), str) else {}
    name = body.get('name', 'Deivids')

    return {
        'statusCode': 200,
        'body': json.dumps({
            'ambiente': ambiente,
            's3': s3_status,
            'endpoint_usado': endpoint,
            'message': f"Agora sou {name}!!!"
        })
    }