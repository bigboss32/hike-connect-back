import logging
from typing import List, Dict, Any
from googleapiclient.errors import HttpError

from inira.app.core.integrations.classroom.google_class_room_base import (
    GoogleClassroomBase,
)

logger = logging.getLogger(__name__)


class GoogleClassroomStudents(GoogleClassroomBase):
    """Servicio para gestionar estudiantes de Google Classroom"""

    def add_student(self, course_id: str, email: str) -> Dict[str, Any]:
        logger.info(f"Agregando estudiante {email} en curso {course_id}")
        try:
            return self.service.courses().students().create(
                courseId=course_id,
                body={"userId": email}
            ).execute()
        except HttpError as error:
            self.handle_error(error, "agregar estudiante")

    def add_students_batch(self, course_id: str, emails: List[str]) -> Dict[str, Any]:
        results = {"successful": [], "failed": []}

        for email in emails:
            try:
                data = self.add_student(course_id, email)
                results["successful"].append({"email": email, "data": data})
            except Exception as e:
                results["failed"].append({"email": email, "error": str(e)})

        return results

    def get_students(self, course_id: str) -> List[Dict[str, Any]]:
        logger.info(f"Obteniendo estudiantes del curso {course_id}")

        try:
            students = []
            page_token = None

            while True:
                response = self.service.courses().students().list(
                    courseId=course_id,
                    pageToken=page_token
                ).execute()

                students.extend(response.get("students", []))
                page_token = response.get("nextPageToken")

                if not page_token:
                    break

            return students

        except HttpError as error:
            self.handle_error(error, "obtener estudiantes")

    def remove_student(self, course_id: str, student_id: str) -> bool:
        logger.info(f"Eliminando estudiante {student_id} del curso {course_id}")
        try:
            self.service.courses().students().delete(
                courseId=course_id,
                userId=student_id
            ).execute()
            return True
        except HttpError as error:
            self.handle_error(error, "eliminar estudiante")

    def get_student(self, course_id: str, student_id: str) -> Dict[str, Any]:
        try:
            return self.service.courses().students().get(
                courseId=course_id,
                userId=student_id
            ).execute()
        except HttpError as error:
            self.handle_error(error, "obtener estudiante")
