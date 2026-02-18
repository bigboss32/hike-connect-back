# inira/app/routes/domain/entities.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal


@dataclass
class Coordinates:
    lat: float
    lng: float


@dataclass
class RouteEntity:

    title: str
    location: str
    distance: str
    duration: str
    difficulty: str
    image: str
    type: str
    category: str
    description: str
    coordinates: Coordinates

    # Campos opcionales originales
    id: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    whatsapp: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Campos de pricing y configuración
    base_price: Decimal = Decimal("0.00")
    requires_payment: bool = False
    max_capacity: int = 20
    min_participants: int = 1
    max_participants_per_booking: int = 10
    requires_date_selection: bool = True
    is_active: bool = True

    # Información adicional
    included_services: Optional[str] = None
    requirements: Optional[str] = None
    what_to_bring: Optional[str] = None

    # Campos calculados
    rating_avg: Optional[float] = None
    rating_count: int = 0

    # -------------------------
    # 🔧 MÉTODOS DE DOMINIO
    # -------------------------

    def validate_booking_capacity(self, number_of_people: int):
        """
        Valida que se cumplan los límites de capacidad.

        Raises:
            ValueError: Si no se cumplen los límites
        """
        if number_of_people < self.min_participants:
            raise ValueError(
                f"Se requieren mínimo {self.min_participants} participantes"
            )

        if number_of_people > self.max_participants_per_booking:
            raise ValueError(
                f"Máximo {self.max_participants_per_booking} participantes por reserva"
            )

    def calculate_amount_in_cents(self, number_of_people: int) -> int:
        """
        Calcula el monto total en centavos para Wompi.

        Returns:
            Monto en centavos (COP)
        """
        if number_of_people < 1:
            raise ValueError("El número de personas debe ser mayor a 0")

        return int(self.base_price * number_of_people * 100)

    def calculate_total_price(self, number_of_people: int) -> Decimal:
        """
        Calcula el precio total en COP.

        Returns:
            Precio total en COP
        """
        if number_of_people < 1:
            raise ValueError("El número de personas debe ser mayor a 0")

        return self.base_price * number_of_people

    def has_available_slots(self, available_slots: int, number_of_people: int) -> bool:
        """
        Verifica si hay suficientes cupos disponibles.
        """
        return available_slots >= number_of_people
