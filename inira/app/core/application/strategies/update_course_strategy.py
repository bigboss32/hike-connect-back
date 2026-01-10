from inira.app.shared.container import container
class UpdateCourseStrategy:
    def execute(self, data):
        return container.course().update().ejecutar(data)
