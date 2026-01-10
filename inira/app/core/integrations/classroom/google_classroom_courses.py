import logging
from typing import Dict, Any, List
from googleapiclient.errors import HttpError

from inira.app.core.integrations.classroom.google_class_room_base import (
    GoogleClassroomAPIException,
    GoogleClassroomBase
)

logger = logging.getLogger(__name__)


class GoogleClassroomClient(GoogleClassroomBase):

    def create_course(self, course_data: Dict[str, Any]) -> Dict[str, Any]:
        print(f"\n[DEBUG GC] create_course() llamado")
        print(f"[DEBUG GC] course_data: {course_data}")
        logger.info(f"Intentando crear curso: {course_data.get('name', 'Sin nombre')}")
        
        try:
            print(f"[DEBUG GC] Llamando a API de Google Classroom...")
            result = self.service.courses().create(body=course_data).execute()
            print(f"[DEBUG GC] Curso creado exitosamente: {result.get('id', 'N/A')}")
            return result
        except HttpError as error:
            print(f"[DEBUG GC ERROR] HttpError al crear curso: {error.resp.status}")
            print(f"[DEBUG GC ERROR] Content: {error.content}")
            self.handle_error(error, "crear curso")

    def get_courses(self, filters: Dict[str, Any] = None, page_size: int = 100, max_pages: int = None) -> List[Dict[str, Any]]:
        print(f"\n[DEBUG GC] get_courses() llamado")
        print(f"[DEBUG GC] filters: {filters}, page_size: {page_size}, max_pages: {max_pages}")
        logger.info(f"Obteniendo cursos con filtros: {filters}")

        try:
            params = filters or {}
            params['pageSize'] = page_size  # Controlar el tamaño de página
            
            courses = []
            page_token = None
            page_count = 0
            max_retries = 3

            while True:
                page_count += 1
                print(f"[DEBUG GC] Obteniendo página {page_count}...")
                
                # Verificar límite de páginas si está configurado
                if max_pages and page_count > max_pages:
                    print(f"[DEBUG GC] Límite de páginas alcanzado ({max_pages})")
                    break
                
                if page_token:
                    params["pageToken"] = page_token

                # Reintentar en caso de error 500
                for attempt in range(max_retries):
                    try:
                        response = self.service.courses().list(**params).execute()
                        break  # Éxito, salir del loop de reintentos
                    except HttpError as e:
                        if e.resp.status == 500 and attempt < max_retries - 1:
                            import time
                            wait_time = (attempt + 1) * 2
                            print(f"[DEBUG GC] Error 500 en intento {attempt + 1}/{max_retries}. Reintentando en {wait_time}s...")
                            time.sleep(wait_time)
                        else:
                            raise
                
                page_courses = response.get("courses", [])
                courses.extend(page_courses)
                
                print(f"[DEBUG GC] Página {page_count}: {len(page_courses)} cursos (total: {len(courses)})")
                
                page_token = response.get("nextPageToken")

                if not page_token:
                    break

            print(f"[DEBUG GC] Total de cursos obtenidos: {len(courses)}")
            return courses

        except HttpError as error:
            print(f"[DEBUG GC ERROR] HttpError al obtener cursos: {error.resp.status}")
            print(f"[DEBUG GC ERROR] Content: {error.content}")
            print(f"[DEBUG GC ERROR] Cursos obtenidos antes del error: {len(courses)}")
            
            # Retorno parcial en caso de error 500
            if error.resp.status == 500 and len(courses) > 0:
                print(f"[DEBUG GC] Retornando {len(courses)} cursos obtenidos antes del error 500")
                logger.warning(f"Error 500 pero se obtuvieron {len(courses)} cursos")
                return courses
            
            self.handle_error(error, "obtener cursos")

    def get_course(self, course_id: str) -> Dict[str, Any]:
        print(f"\n[DEBUG GC] get_course() llamado")
        print(f"[DEBUG GC] course_id: {course_id}")
        logger.info(f"Obteniendo curso {course_id}")

        try:
            print(f"[DEBUG GC] Llamando a API de Google Classroom...")
            result = self.service.courses().get(id=course_id).execute()
            print(f"[DEBUG GC] Curso obtenido: {result.get('name', 'N/A')}")
            return result
        except HttpError as error:
            print(f"[DEBUG GC ERROR] HttpError al obtener curso: {error.resp.status}")
            print(f"[DEBUG GC ERROR] Content: {error.content}")
            self.handle_error(error, "obtener curso")

    def get_all_courses(self, page_size: int = 100, max_pages: int = None) -> List[Dict[str, Any]]:
        print(f"\n[DEBUG GC] get_all_courses() llamado")
        print(f"[DEBUG GC] page_size: {page_size}, max_pages: {max_pages}")
        logger.info("Obteniendo todos los cursos")

        try:
            courses = []
            page_token = None
            page_count = 0
            max_retries = 3

            while True:
                page_count += 1
                print(f"[DEBUG GC] Obteniendo página {page_count}...")
                
                # Verificar límite de páginas si está configurado
                if max_pages and page_count > max_pages:
                    print(f"[DEBUG GC] Límite de páginas alcanzado ({max_pages})")
                    break
                
                # Reintentar en caso de error 500
                for attempt in range(max_retries):
                    try:
                        response = self.service.courses().list(
                            pageToken=page_token,
                            pageSize=page_size
                        ).execute()
                        break  # Éxito, salir del loop de reintentos
                    except HttpError as e:
                        if e.resp.status == 500 and attempt < max_retries - 1:
                            import time
                            wait_time = (attempt + 1) * 2  # Espera incremental: 2s, 4s, 6s
                            print(f"[DEBUG GC] Error 500 en intento {attempt + 1}/{max_retries}. Reintentando en {wait_time}s...")
                            time.sleep(wait_time)
                        else:
                            raise  # Re-lanzar si no es 500 o se acabaron los reintentos
                
                page_courses = response.get("courses", [])
                courses.extend(page_courses)
                
                print(f"[DEBUG GC] Página {page_count}: {len(page_courses)} cursos (total acumulado: {len(courses)})")
                
                page_token = response.get("nextPageToken")

                if not page_token:
                    print(f"[DEBUG GC] No hay más páginas")
                    break

            print(f"[DEBUG GC] Total de cursos obtenidos: {len(courses)}")
            return courses

        except HttpError as error:
            print(f"[DEBUG GC ERROR] HttpError al obtener todos los cursos: {error.resp.status}")
            print(f"[DEBUG GC ERROR] Content: {error.content}")
            print(f"[DEBUG GC ERROR] Cursos obtenidos antes del error: {len(courses)}")
            
            # Si obtuvimos algunos cursos antes del error, podrías considerarlo un éxito parcial
            if error.resp.status == 500 and len(courses) > 0:
                print(f"[DEBUG GC] Retornando {len(courses)} cursos obtenidos antes del error 500")
                logger.warning(f"Error 500 pero se obtuvieron {len(courses)} cursos")
                return courses
            
            self.handle_error(error, "obtener todos los cursos")

    def update_course(self, course_id: str, course_data: Dict[str, Any]):
        print(f"\n[DEBUG GC] update_course() llamado")
        print(f"[DEBUG GC] course_id: {course_id}")
        print(f"[DEBUG GC] course_data: {course_data}")
        logger.info(f"Actualizando curso {course_id} con datos: {course_data}")
        
        try:
            update_mask = ",".join(course_data.keys())
            print(f"[DEBUG GC] update_mask: {update_mask}")

            result = self.service.courses().patch(
                id=course_id,
                updateMask=update_mask,
                body=course_data
            ).execute()
            
            print(f"[DEBUG GC] Curso actualizado exitosamente")
            return result
            
        except TypeError as e:
            print(f"[DEBUG GC ERROR] TypeError: {str(e)}")
            if "Missing required parameter" in str(e) and "id" in str(e):
                raise GoogleClassroomAPIException(
                    detail="No se puede actualizar el curso porque el ID es inválido o está ausente.",
                    code="curso_id_invalido"
                )
            raise e 
            
        except HttpError as error:
            print(f"[DEBUG GC ERROR] HttpError al actualizar curso: {error.resp.status}")
            print(f"[DEBUG GC ERROR] Content: {error.content}")
            
            if error.resp.status == 404:
                raise GoogleClassroomAPIException(
                    detail="El curso no existe en Google Classroom y no puede ser actualizado.",
                    code="curso_no_encontrado"
                )
            self.handle_error(error, "actualizar curso")

    def delete_course(self, course_id: str) -> bool:
        print(f"\n[DEBUG GC] delete_course() llamado")
        print(f"[DEBUG GC] course_id: {course_id}")
        logger.info(f"Eliminando curso {course_id}")

        try:
            print(f"[DEBUG GC] Intentando eliminar curso...")
            self.service.courses().delete(id=course_id).execute()
            print(f"[DEBUG GC] Curso eliminado exitosamente")
            return True

        except HttpError as error:
            print(f"[DEBUG GC ERROR] HttpError al eliminar curso: {error.resp.status}")
            print(f"[DEBUG GC ERROR] Content: {error.content}")
            
            if error.resp.status == 400 and "Precondition check failed" in str(error):
                print(f"[DEBUG GC] Intentando archivar curso en lugar de eliminar...")
                try:
                    self.service.courses().patch(
                        id=course_id,
                        updateMask="courseState",
                        body={"courseState": "ARCHIVED"}
                    ).execute()
                    print(f"[DEBUG GC] Curso archivado exitosamente")
                    return True
                except HttpError as error2:
                    print(f"[DEBUG GC ERROR] HttpError al archivar curso: {error2.resp.status}")
                    print(f"[DEBUG GC ERROR] Content: {error2.content}")
                    self.handle_error(error2, "archivar curso")
            
            self.handle_error(error, "eliminar curso")