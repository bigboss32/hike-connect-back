# inira/app/payments/domain/services/wompi_service.py

from abc import ABC, abstractmethod
from typing import Dict, Any


class WompiService(ABC):
    @abstractmethod
    def create_pse_transaction(self, **kwargs) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_transaction_status(self, transaction_id: str) -> Dict[str, Any]:
        pass
