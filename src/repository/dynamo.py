import boto3

from src.utils.logger import logger


class DynamoDB:
    def __init__(self, table_name):
        self.table_name = table_name
        self.dynamodb = boto3.client('dynamodb', region_name='us-east-1')

    def scan(self, status):
        logger.info(f'Scanning DynamoDB correioszap for status {status}')

        response = self.dynamodb.scan(
            TableName=self.table_name,
            FilterExpression='current_status = :current_status',
            ExpressionAttributeValues={
                ':current_status': {'S': status}
            }
        )

        items = []

        for item in response.get('Items'):
            data = {}

            for key, value in item.items():
                data[key] = value.get('S')

            items.append(data)

        return items

    def query(self, track_id, status):
        logger.info(f'Querying DynamoDB correioszap: {track_id} for status {status}')

        response = self.dynamodb.query(
            TableName=self.table_name,
            KeyConditionExpression='track_id = :track_id AND current_status = :current_status',
            ExpressionAttributeValues={
                ':track_id': {'S': track_id},
                ':current_status': {'S': status}
            }
        )

        items = []

        for item in response.get('Items'):
            data = {}

            for key, value in item.items():
                data[key] = value.get('S')

            items.append(data)

        return items

    def put_item(self, item):

        data = {}

        for key, value in item.items():
            data[key] = {'S': str(value)}

        logger.info(f'Storing item in DynamoDB correioszap: {data}')

        try:
            self.dynamodb.put_item(
                TableName=self.table_name,
                Item=data
            )
        except Exception as e:
            logger.error(f'Error storing item in DynamoDB: {e}')
            raise

    def get_item(self, track_id):
        logger.info(f'Getting item from DynamoDB correioszap: {track_id}')

        try:
            response = self.dynamodb.get_item(
                TableName=self.table_name,
                Key={
                    'track_id': {'S': track_id}
                }
            )

            data = {}

            for key, value in response.get('Item').items():
                data[key] = value.get('S')

            return data
        except Exception as e:
            logger.error(f'Error getting item from DynamoDB: {e}')
            raise

    def update_item(self, track_id, item):
        logger.info(f'Updating item in DynamoDB correioszap: {track_id}')

        update_expression = "SET " + ", ".join(f"{k} = :{k}" for k in item.keys())
        expression_attribute_values = {f":{k}": {'S': str(v)} for k, v in item.items()}

        try:
            self.dynamodb.update_item(
                TableName=self.table_name,
                Key={
                    'track_id': {'S': track_id}
                },
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values
            )
        except Exception as e:
            logger.error(f'Error updating item in DynamoDB: {e}')
            raise
