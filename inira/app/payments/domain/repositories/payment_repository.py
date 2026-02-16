# inira/app/payments/domain/repositories/payment_repository.py

from abc import ABC, abstractmethod


class PaymentRepository(ABC):
    @abstractmethod
    def create(self, **kwargs):
        pass

    @abstractmethod
    def get_by_id(self, payment_id: int):
        pass

    @abstractmethod
    def get_by_transaction_id(self, transaction_id: str):
        pass

    @abstractmethod
    def update_status(self, payment_id: int, status: str):
        pass
