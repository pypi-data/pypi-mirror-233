import ctypes
import os
import sys

if sys.platform == "darwin":
    ctypes.CDLL(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "lib/libtiledbgenomicsdb.dylib"
        )
    )
else:
    try:
        ctypes.CDLL(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "lib/libtiledbgenomicsdb.so"
            )
        )
    except:
        genomicsdb_home = os.getenv("GENOMICSDB_HOME")
        if genomicsdb_home is None:
            ctypes.CDLL(os.path.join("/usr/local/lib/libtiledbgenomicsdb.so"))
        else:
            ctypes.CDLL(os.path.join(genomicsdb_home, "lib/libtiledbgenomicsdb.so"))

__path__ = __import__("pkgutil").extend_path(__path__, __name__)
from .genomicsdb import *
