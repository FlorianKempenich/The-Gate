
def get_instance():
    return ComplexClass()

class ComplexClass():
    @property
    def nested(self):
        return NestedClass()

class NestedClass():
    def explode_nested(self, arg):
        raise Exception('I am the nested class')

