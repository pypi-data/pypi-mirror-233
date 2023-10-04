import ctypes

# Load the shared library
schedulers = ctypes.CDLL('./cpp_extensions/schedulers.so')


# Define Python wrappers

class CosineScheduler:

    def __init__(self, start_step: int, stop_step: int, start_value: float, stop_value: float):

        super().__init__()

        # method signatures
        schedulers.CosineScheduler_create.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double]
        schedulers.CosineScheduler_create.restype = ctypes.c_void_p

        schedulers.CosineScheduler_step.argtypes = [ctypes.c_void_p, ctypes.c_int]
        schedulers.CosineScheduler_step.restype = ctypes.c_double

        schedulers.CosineScheduler_destroy.argtypes = [ctypes.c_void_p]

        # constructor
        self.s = schedulers.CosineScheduler_create(start_step, stop_step, start_value, stop_value)

    def step(self, step: int):
        return schedulers.CosineScheduler_step(self.s, step)

    def destroy(self):
        schedulers.CosineScheduler_destroy(self.s)


class LinearScheduler:

    def __init__(self, start_step: int, stop_step: int, start_value: float, stop_value: float):

        super().__init__()

        # method signatures
        schedulers.LinearScheduler_create.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double]
        schedulers.LinearScheduler_create.restype = ctypes.c_void_p

        schedulers.LinearScheduler_step.argtypes = [ctypes.c_void_p, ctypes.c_int]
        schedulers.LinearScheduler_step.restype = ctypes.c_double

        schedulers.LinearScheduler_destroy.argtypes = [ctypes.c_void_p]

        # constructor
        self.s = schedulers.LinearScheduler_create(start_step, stop_step, start_value, stop_value)

    def step(self, step: int):
        return schedulers.LinearScheduler_step(self.s, step)

    def destroy(self):
        schedulers.LinearScheduler_destroy(self.s)


class LinearCosineScheduler:
    def __init__(self, start_step: int, stop_step: int, start_value: float, stop_value: float, th_step: int):

        # method signatures
        schedulers.LinearCosineScheduler_create.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_double,
                                                            ctypes.c_double]
        schedulers.LinearCosineScheduler_create.restype = ctypes.c_void_p

        schedulers.LinearCosineScheduler_step.argtypes = [ctypes.c_void_p, ctypes.c_int]
        schedulers.LinearCosineScheduler_step.restype = ctypes.c_double

        schedulers.LinearCosineScheduler_destroy.argtypes = [ctypes.c_void_p]

        # constructor
        self.s = schedulers.LinearCosineScheduler_create(start_step, stop_step, start_value, stop_value, th_step)

    def step(self, step: int):
        return schedulers.LinearCosineScheduler_step(self.s, step)

    def destroy(self):
        schedulers.LinearCosineScheduler_destroy(self.s)
