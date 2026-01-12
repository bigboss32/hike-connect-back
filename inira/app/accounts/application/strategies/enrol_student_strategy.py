from inira.app.shared.container import container
class EnrolStudentStrategy:
    def execute(self, data):
        return container.student().matricular().ejecutar(data)
