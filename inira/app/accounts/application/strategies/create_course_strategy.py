from inira.app.shared.container import container
class CreateCoursetStrategy:
    def execute(self, data):
        return container.course().create().ejecutar(data)
