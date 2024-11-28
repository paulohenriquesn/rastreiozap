from dependency_injection import tracking_service, repository
from src.utils.logger import logger


def update_tracks():
    logger.info('Running cron update tracks schedule.')

    items = repository.scan(status='PENDING')

    logger.info(f'Found {len(items)} items to update.')

    for item in items:
        tracking_status = tracking_service.track(
            deliver_company='correios',
            code=item['track_id']
        )

        last_update_date = tracking_status[0]['date']
        last_status = tracking_status[0]['message']
        last_destiny = tracking_status[0]['destiny']

        try:
            old_item = repository.get_item(item['track_id'])

            if old_item['last_update_date'] != last_update_date:
                logger.info(f'Item {old_item["track_id"]} updated. Last update: {last_update_date}')
                logger.info(f'New status: {last_status} - {last_destiny}')

                repository.update_item(
                    track_id=item['track_id'],
                    item={
                        'events': tracking_status,
                        'destiny': last_destiny,
                        'current_status': last_status,
                        'last_update_date': last_update_date
                    }
                )
            pass
        except Exception as e:
            logger.error(f'Item not found on dynamo: {str(e)}')