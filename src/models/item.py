from enum import Enum

class Status(Enum):
    PICKED_UP = 'PICKED_UP'
    AWAITING_PAYMENT = 'AWAITING_PAYMENT'
    IN_TRANSIT = 'IN_TRANSIT'
    COMING_TO_DELIVERY = 'COMING_TO_DELIVERY'
    DELIVERED = 'DELIVERED'

class Item:
    def __init__(self, name, status: Status):
        self.name = name
        self.status = None