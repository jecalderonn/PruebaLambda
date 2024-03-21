import unittest
import boto3
import moto

from src import index

@moto.mock_dynamodb
@moto.mock_s3
class TestLambdaHandler(unittest.TestCase):

    def test_lambda_handler(self):
        # Crear Evento
        event = {
            'Records': [
                {
                    's3': {
                        'bucket': {
                            'name': 'test-bucket'
                        },
                        'object': {
                            'key': 'test-key'
                        }
                    }
                }
            ]
        }
        context = {}

        # Generar Mocks
        s3 = boto3.client('s3')
        s3.create_bucket(Bucket='test-bucket')
        s3.put_object(Bucket='test-bucket', Key='test-key', Body='body')

        dynamodb = boto3.resource('dynamodb')
        table_name = 'ai-technical-tests-javier-eduardo'
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
        )

        # Invocar Lambda
        index.lambda_handler(event, context)

        # Verificaciones de la lambda
        response = s3.get_object(Bucket='test-bucket', Key='test-key')
        self.assertEqual(response['Body'].read().decode(), 'body')


if __name__ == '__main__':
    unittest.main()