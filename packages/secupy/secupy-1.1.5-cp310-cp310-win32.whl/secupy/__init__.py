"""""" # start delvewheel patch
def _delvewheel_patch_1_5_1():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, '.'))
    if os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_5_1()
del _delvewheel_patch_1_5_1
# end delvewheel patch

import _secupy


def __getattr__(name):
    if hasattr(_secupy, name):
        return getattr(_secupy, name)
    raise AttributeError(f"module {__name__} has no attribute {name}")
