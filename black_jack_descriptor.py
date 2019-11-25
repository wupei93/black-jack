from black_jack_exception import UnsupportedException


class immutable(property):
    def __set__(self, instance, value):
        raise UnsupportedException()