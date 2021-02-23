import io
import sys


class IteratorFile(io.TextIOBase):
    """Файловий об'єкт із рядків """

    def __init__(self, it):
        self._it = it
        self._f = io.StringIO()

    def read(self, length=sys.maxsize):

        try:
            while self._f.tell() < length:
                self._f.write(next(self._it) + "\n")

        except StopIteration as e:
            # цей блок не є необхідним
            pass

        except Exception as e:
            print("uncaught exception: {}".format(e))

        finally:
            self._f.seek(0)
            data = self._f.read(length)

            # збережемо залишок для наступного читання
            remainder = self._f.read()
            self._f.seek(0)
            self._f.truncate(0)
            self._f.write(remainder)
            return data

    def readline(self):
        return next(self._it)
