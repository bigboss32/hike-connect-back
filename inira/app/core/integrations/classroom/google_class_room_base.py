import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)

class GoogleClassroomAPIException(APIException):
    status_code = 400
    default_detail = "Error en la API de Google Classroom"
    default_code = "google_classroom_error"


class GoogleClassroomBase:
    """Base para servicios de Google Classroom"""

    def __init__(self, credentials):
        print(f"\n[DEBUG GCB] Inicializando GoogleClassroomBase")
        print(f"[DEBUG GCB] Tipo de credentials: {type(credentials)}")
        
        # Detectar tipo de credenciales
        if isinstance(credentials, service_account.Credentials):
            print(f"[DEBUG GCB] Credenciales tipo: Service Account")
            print(f"[DEBUG GCB] Service account email: {credentials.service_account_email}")
            print(f"[DEBUG GCB] Scopes: {credentials.scopes}")
            print(f"[DEBUG GCB] Subject (impersonation): {getattr(credentials, '_subject', 'N/A')}")
        elif isinstance(credentials, Credentials):
            print(f"[DEBUG GCB] Credenciales tipo: OAuth2 User")
            print(f"[DEBUG GCB] Valid: {credentials.valid}")
            print(f"[DEBUG GCB] Expired: {credentials.expired}")
        else:
            print(f"[DEBUG GCB] Credenciales tipo: Desconocido")
        
        self.credentials = credentials
        self._service = None
        print(f"[DEBUG GCB] Inicialización completada\n")
    
    @property
    def service(self):
        """Crea el servicio solo una vez (lazy loading)"""
        if not self._service:
            print(f"\n[DEBUG GCB] Construyendo servicio de Google Classroom...")
            print(f"[DEBUG GCB] Credentials type: {type(self.credentials)}")
            print(f"[DEBUG GCB] Credentials valid: {getattr(self.credentials, 'valid', 'N/A')}")
            print(f"[DEBUG GCB] Credentials expired: {getattr(self.credentials, 'expired', 'N/A')}")
            
            logger.debug("Construyendo servicio base de Google Classroom")
            
            try:
                self._service = build("classroom", "v1", credentials=self.credentials)
                print(f"[DEBUG GCB] Servicio construido exitosamente")
            except Exception as e:
                print(f"[DEBUG GCB ERROR] Error al construir servicio: {type(e).__name__}")
                print(f"[DEBUG GCB ERROR] Mensaje: {str(e)}")
                import traceback
                print(f"[DEBUG GCB ERROR] Traceback:\n{traceback.format_exc()}")
                raise
            
            print(f"[DEBUG GCB] Servicio listo para usar\n")
        
        return self._service

    def handle_error(self, error: HttpError, action: str):
        print(f"\n[DEBUG GCB] handle_error() llamado")
        print(f"[DEBUG GCB] action: {action}")
        print(f"[DEBUG GCB] error.resp.status: {error.resp.status}")
        print(f"[DEBUG GCB] error.reason: {error.reason}")
        print(f"[DEBUG GCB] error.content: {error.content}")
        
        logger.error(f"✗ Error en {action}: {error.resp.status} - {error.reason}")
        logger.debug(f"Detalles: {error.content}")

        # Decodificar el contenido del error si es posible
        try:
            import json
            error_details = json.loads(error.content.decode('utf-8'))
            print(f"[DEBUG GCB] Error decodificado: {json.dumps(error_details, indent=2)}")
        except:
            print(f"[DEBUG GCB] No se pudo decodificar el contenido del error")

        exception = GoogleClassroomAPIException(
            detail=f"Error al {action}: {error.reason}",
            code=f"{action}_{error.resp.status}"
        )
        
        print(f"[DEBUG GCB] Lanzando GoogleClassroomAPIException")
        print(f"[DEBUG GCB] detail: {exception.detail}")
        print(f"[DEBUG GCB] code: {exception.get_codes()}\n")
        
        raise exception