import os
import boto3


class DynamoDatabase:
    def __init__(self):
        try:
            self.client = boto3.client(
                'dynamodb',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )
            self.recurso_db = boto3.resource(
                'dynamodb',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )

            self.nome_tabela = 'top_dez_som_artista'

            self.tabela = self.recurso_db.Table(self.nome_tabela)

            self.create_tables()
        except Exception as error:
            print(error)

    def create_tables(self):
        try:
            existe_tabela = self.client.list_tables()['TableNames']

            if self.nome_tabela not in existe_tabela:
                self.client.create_table(
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'search_term',
                            'AttributeType': 'S',
                        }
                    ],
                    KeySchema=[
                        {
                            'AttributeName': 'search_term',
                            'KeyType': 'HASH',
                        }
                    ],
                    ProvisionedThroughput={
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5,
                    },
                    TableName=self.nome_tabela,
                )
        except Exception as error:
            print(error)

    def set_item(self, artista, item_data):
        try:
            response = self.tabela.update_item(
                Key={
                    'artista': artista
                },
                UpdateExpression="set artist_data=:s",
                ExpressionAttributeValues={
                    ":s": item_data
                }
            )

            return response
        except Exception as error:
            print(error)

            return None
