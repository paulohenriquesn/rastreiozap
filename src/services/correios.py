import os
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from src.models.item import Status
from src.utils.logger import logger


class CorreiosService:
    def track(self, tracking_number):
        retry_strategy = Retry(
            total=16,
            backoff_factor=1,
            status_forcelist=[413, 429, 503]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()

        session.mount("https://", adapter)
        session.mount("http://", adapter)

        try:
            logger.info(f'Calling Correios API with tracking number: {tracking_number}')
            response = session.get(
                f'https://api.linketrack.com/track/json?user=teste&token=1abcd00b2731640e886fb41a8a9671ad1434c599dbaa0a0de9a5aa619f29a83f&codigo={tracking_number}')
            response.raise_for_status()
            data = response.json()

            events = []

            for event in data['eventos']:
                status = {
                    'message': event['status'],
                    'date': f'{event["data"]} {event["hora"]}',
                    'destiny': event['local']
                }

                events.append(status)
            return events

        except Exception as e:
            logger.error(e)
            raise
