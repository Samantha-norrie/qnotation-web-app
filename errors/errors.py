from abc import ABC

from .error_utils import MESSAGE_INPUT_ERROR, MESSAGE_TOO_MANY_QUBITS_ERROR, MESSAGE_TOO_MANY_QUBITS_FOR_TENSOR_ERROR, MESSAGE_INVALID_GATE_ERROR, MESSAGE_GATE_NOT_SUPPORTED_ERROR, MESSAGE_HIGHER_INDEXED_CONTROL_QUBIT_ERROR, MESSAGE_NON_NEIGHBOURING_QUBITS_ERROR, MESSAGE_UNKNOWN_ERROR

class QNotationException(Exception, ABC):
    default_message: str = "An error occurred."

    def __init__(self, message: str = None):
        self.message = message if message is not None else self.default_message
        super().__init__(self.message)

class InputError(QNotationException):
    default_message = MESSAGE_INPUT_ERROR

class InvalidGateError(QNotationException):
    default_message = MESSAGE_INVALID_GATE_ERROR

class TooManyQubitsError(QNotationException):
    default_message = MESSAGE_TOO_MANY_QUBITS_ERROR

class TooManyQubitsForTensorError(QNotationException):
    default_message = MESSAGE_TOO_MANY_QUBITS_FOR_TENSOR_ERROR

class GateNotImplementedError(QNotationException):
    default_message = MESSAGE_GATE_NOT_SUPPORTED_ERROR

class HigherIndexedControlQubitError(QNotationException):
    default_message = MESSAGE_HIGHER_INDEXED_CONTROL_QUBIT_ERROR

class NonNeighbouringQubitsError(QNotationException):
    default_message = MESSAGE_NON_NEIGHBOURING_QUBITS_ERROR

class UnknownError(Exception):
    default_message = MESSAGE_UNKNOWN_ERROR
