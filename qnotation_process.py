from abc import ABC, abstractmethod

class QNotationProcess(ABC):
    def execute(self):
        """Defines the process order."""
        self.step1()
        self.step2()
        self.step3()

    @abstractmethod
    def create_gate_representations(self):
        pass

    @abstractmethod
    def create_state_representations(self):
        pass

    @abstractmethod
    def format_and_simplify_output(self):
        pass

class Circuit(QNotationProcess):
    def create_gate_representations(self):
        print("ProcessA Step 1")

    def create_state_representations(self):
        print("ProcessA Step 2")

    def format_and_simplify_output(self):
        print("ProcessA Step 3")

class Dirac(QNotationProcess):
    def create_gate_representations(self):
        print("ProcessA Step 1")

    def create_state_representations(self):
        print("ProcessA Step 2")

    def format_and_simplify_output(self):
        print("ProcessA Step 3")

class Matrix(QNotationProcess):
    def create_gate_representations(self):
        print("ProcessA Step 1")

    def create_state_representations(self):
        print("ProcessA Step 2")

    def format_and_simplify_output(self):
        print("ProcessA Step 3")

# Usage
process = Circuit()
process.execute()
