from src.facades.tracking import TrackingFacade
from src.repository.dynamo import DynamoDB

tracking_service = TrackingFacade()
repository = DynamoDB('correiozap')