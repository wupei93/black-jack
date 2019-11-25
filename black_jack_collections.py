from black_jack_exception import UnsupportedException


class ImmutableList(list):
    def __setitem__(self, *args, **kwargs): # real signature unknown
        raise UnsupportedException()