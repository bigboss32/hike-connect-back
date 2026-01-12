from inira.app.shared.container import container
class DeleteCourseStrategy:
    def execute(self, data):
        return container.course().delete().ejecutar(data)
