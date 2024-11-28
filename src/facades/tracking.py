from src.models.item import Status
from src.services.correios import CorreiosService


class TrackingFacade:
    def __init__(self):
        self.correios_service = CorreiosService()

    def track(self, deliver_company, code):
        if deliver_company == 'correios':
            return self.correios_service.track(code)


