from inira.app.shared.container import container
class UnenrolStudentStrategy:
    def execute(self, data):
        return container.student().matricular().ejecutar(data)
