class PickleError(Exception):
    pass

class PicklingError(PickleError):
    pass

class UnpicklingError(PickleError):
    pass
