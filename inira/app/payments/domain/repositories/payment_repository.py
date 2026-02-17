# inira/app/payments/domain/repositories/payment_repository.py

from abc import ABC, abstractmethod


class PaymentRepository(ABC):

    @abstractmethod
    def create(self, **kwargs):
        pass

    @abstractmethod
    def get_by_id(self, payment_id: str):
        pass

    @abstractmethod
    def get_by_transaction_id(self, transaction_id: str):
        pass

    @abstractmethod
    def get_by_reference(self, reference: str):
        pass

    @abstractmethod
    def update_status(self, payment_id: str, status: str):
        pass

    # 🆕
    @abstractmethod
    def update_status_and_url(
        self,
        payment_id: str,
        status: str,
        redirect_url: str = None,
    ):
        pass

    @abstractmethod
    def get_user_payments(self, user_id: int):
        pass
