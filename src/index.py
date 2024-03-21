import boto3
import hashlib
import uuid
 
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
 
def lambda_handler(event, context):
    # Obteniendo los datos del Evento
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
   # Descargo el archivo del bucket
    s3.download_file(bucket, key, download_path)
   # Leo el archivo
    with open(download_path, 'r') as file:
        lines = file.readlines()

    data = {}
    # Recorro el archivo y uno todos los valores menos el Hash
    for line in lines:
        parts = line.strip().split('=')
        if len(parts) >= 2:
            key, value = parts
            if key != 'hash':
                data[key] = value
    # Creo el Hash MD5 a comparar con el que viene en el archivo
    hash_string = '~'.join([data[key] for key in (data.keys())])
    hash_object = hashlib.md5(hash_string.encode())
    md5_hash = hash_object.hexdigest()
    # Validacion Hash
    last_line_parts = lines[-1].strip().split('=')
    if len(last_line_parts) >=2:
        if md5_hash != lines[-1].strip().split('=')[1]:
            raise ValueError('Hash does not match')
    else:
        raise ValueError('Invalid format for hash line')
    # Insertar datos en la tabla
    table = dynamodb.Table('ai-technical-__test__-javier-eduardo')
    table.put_item(Item=data)
    # Elimina el archivo del bucket
    s3.delete_object(Bucket=bucket, Key=key)

