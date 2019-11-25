class UnsupportedException(Exception):
    def __str__(self):
        return 'UnsupportedException:' + str(super())

