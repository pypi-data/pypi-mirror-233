import pathlib
import os


from cffi import FFI

ffi = FFI()
data_dir = pathlib.Path(os.path.dirname(__file__)).absolute().parent / "data"

with open(data_dir / "hypertune.h") as header:
    ffi.cdef(header.read())

lib = data_dir / "libclib.dylib"
clib = ffi.dlopen(str(lib))
