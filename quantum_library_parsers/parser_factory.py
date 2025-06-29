from .qiskit_parser import QiskitParser
from .pennylane_parser import PennylaneParser
from .cirq_parser import CirqParser
from . import Parser

class ParserFactory:
    parsers = {
        "qiskit": QiskitParser,
        "pennylane": PennylaneParser,
        "cirq": CirqParser
    }

    @staticmethod
    def get_parser(qc_type: str) -> Parser:
        parser_cls = ParserFactory.parsers.get(qc_type.lower())
        if not parser_cls:
            raise ValueError(f"Unknown parser type: {qc_type}")
        return parser_cls()
