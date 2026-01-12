from inira.app.shared.container import container
class CreateusersStrategy:
    def execute(self, data):
        return container.student().crear_estudiante().ejecutar(data)
