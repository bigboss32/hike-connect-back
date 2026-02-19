# inira/app/routes/infrastructure/docs/create_route_docs.py

from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from inira.app.routes.infrastructure.out.route_output_serializer import (
    RouteOutputSerializer,
)
from inira.app.routes.infrastructure.input.route_input_serializer import (
    RouteInputSerializer,
)

create_route_docs = extend_schema(
    tags=["Rutas"],
    summary="Crear una ruta de senderismo",
    description=(
        "Crea una nueva ruta de senderismo en el sistema.\n\n"
        "- Requiere autenticación y pertenecer al grupo **ofertante**.\n"
        "- Las coordenadas se envían como objeto `{ lat, lng }`.\n"
        "- La dificultad acepta: `Fácil`, `Medio`, `Difícil`.\n"
        "- El tipo acepta: `pública`, `privada`, `agroturismo`.\n"
        "- La categoría acepta: `senderismo`, `agroturismo`.\n"
        "- Los campos opcionales tienen valores por defecto definidos en el modelo."
    ),
    request=RouteInputSerializer,
    responses={
        201: RouteOutputSerializer,
        400: OpenApiTypes.OBJECT,
        401: OpenApiTypes.OBJECT,
        403: OpenApiTypes.OBJECT,
    },
    examples=[
        # 🔹 REQUEST COMPLETO (primero = default en Swagger)
        OpenApiExample(
            name="Crear ruta completa",
            summary="Body con absolutamente todos los campos disponibles",
            value={
                # ── Obligatorios ──────────────────────────────────────
                "title": "Ruta Cascada Azul",
                "location": "Antioquia, Colombia",
                "distance": "8 km",
                "duration": "3-4 horas",
                "difficulty": "Fácil",
                "image": "https://example.com/imagen.jpg",
                "type": "pública",
                "category": "senderismo",
                "description": "Hermosa ruta que lleva a una cascada de aguas cristalinas en medio del bosque.",
                "coordinates": {
                    "lat": 6.25184,
                    "lng": -75.56359,
                },
                "phone": "3001234567",
                "email": "info@rutacascada.com",
                "whatsapp": "3001234567",
                # ── Empresa (opcional) ────────────────────────────────
                "company": "Ecoturismo Antioquia SAS",
                # ── Pricing (opcional) ────────────────────────────────
                "base_price": "45000.00",
                "requires_payment": True,
                # ── Capacidad (opcional) ──────────────────────────────
                "max_capacity": 25,
                "min_participants": 2,
                "max_participants_per_booking": 8,
                # ── Disponibilidad (opcional) ─────────────────────────
                "requires_date_selection": True,
                "is_active": True,
                # ── Información adicional (opcional) ──────────────────
                "included_services": "Guía certificado\nRefrigerio\nSeguro de vida\nTransporte al punto de inicio",
                "requirements": "Buena condición física\nMayores de 12 años\nFirmar acuerdo de responsabilidad",
                "what_to_bring": "Ropa cómoda\nAgua mínimo 2 litros\nProtector solar\nZapatos de senderismo",
            },
            request_only=True,
        ),
        # 🔹 REQUEST MÍNIMO
        OpenApiExample(
            name="Crear ruta básica",
            summary="Body con solo los campos obligatorios",
            value={
                "title": "Ruta Cascada Azul",
                "location": "Antioquia, Colombia",
                "distance": "8 km",
                "duration": "3-4 horas",
                "difficulty": "Fácil",
                "image": "https://example.com/imagen.jpg",
                "type": "pública",
                "category": "senderismo",
                "description": "Hermosa ruta que lleva a una cascada de aguas cristalinas.",
                "coordinates": {
                    "lat": 6.25184,
                    "lng": -75.56359,
                },
                "phone": "3001234567",
                "email": "info@ruta.com",
                "whatsapp": "3001234567",
            },
            request_only=True,
        ),
        # 🔹 RESPUESTA 201
        OpenApiExample(
            name="Ruta creada exitosamente",
            summary="Respuesta al crear una ruta correctamente",
            value={
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Ruta Cascada Azul",
                "location": "Antioquia, Colombia",
                "distance": "8 km",
                "duration": "3-4 horas",
                "difficulty": "Fácil",
                "image": "https://example.com/imagen.jpg",
                "type": "pública",
                "category": "senderismo",
                "description": "Hermosa ruta que lleva a una cascada de aguas cristalinas en medio del bosque.",
                "coordinates": {
                    "lat": 6.25184,
                    "lng": -75.56359,
                },
                "company": "Ecoturismo Antioquia SAS",
                "phone": "3001234567",
                "email": "info@rutacascada.com",
                "whatsapp": "3001234567",
                "base_price": "45000.00",
                "requires_payment": True,
                "max_capacity": 25,
                "min_participants": 2,
                "max_participants_per_booking": 8,
                "requires_date_selection": True,
                "is_active": True,
                "included_services": "Guía certificado\nRefrigerio\nSeguro de vida\nTransporte al punto de inicio",
                "requirements": "Buena condición física\nMayores de 12 años\nFirmar acuerdo de responsabilidad",
                "what_to_bring": "Ropa cómoda\nAgua mínimo 2 litros\nProtector solar\nZapatos de senderismo",
                "rating_avg": None,
                "rating_count": 0,
                "created_at": "2025-01-01T10:00:00Z",
                "updated_at": "2025-01-01T10:00:00Z",
            },
            response_only=True,
            status_codes=["201"],
        ),
        # 🔹 ERROR 400
        OpenApiExample(
            name="Datos inválidos",
            summary="Error de validación en el body",
            value={
                "difficulty": ['"invalido" is not a valid choice.'],
                "email": ["Enter a valid email address."],
                "coordinates": {
                    "lat": ["This field is required."],
                },
            },
            response_only=True,
            status_codes=["400"],
        ),
        # 🔹 ERROR 401
        OpenApiExample(
            name="No autenticado",
            summary="Token no enviado o inválido",
            value={"detail": "Authentication credentials were not provided."},
            response_only=True,
            status_codes=["401"],
        ),
        # 🔹 ERROR 403
        OpenApiExample(
            name="Sin permisos",
            summary="Usuario autenticado pero sin grupo ofertante",
            value={"detail": "No tienes permisos para realizar esta acción."},
            response_only=True,
            status_codes=["403"],
        ),
    ],
)
