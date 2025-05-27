from . import QiskitParser, PennylaneParser, Parser
class ParserFactory:
    parsers = {
        "qiskit": QiskitParser,
        "pennylane": PennylaneParser,
    }

    @staticmethod
    def get_parser(name: str) -> Parser:
        parser_cls = ParserFactory.parsers.get(name.lower())
        if not parser_cls:
            raise ValueError(f"Unknown parser type: {name}")
        return parser_cls()
