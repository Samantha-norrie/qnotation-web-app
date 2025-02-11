import pytest
import httpx
import asyncio
import json
from test_utils import *

class TestEmpty:
    @classmethod
    def setup_class(cls):
        cls.data = asyncio.run(send_request(EMPTY))

    def test_status_code(self):
        assert self.data["status"] == BAD_REQUEST_ERR

class TestTypo:
    @classmethod
    def setup_class(cls):
        cls.data = asyncio.run(send_request(TYPO))

    def test_status_code(self):
        assert self.data["status"] == BAD_REQUEST_ERR

class TestSingleColumnTwoQubitNeighbouringGate:
    @classmethod
    def setup_class(cls):
        cls.data = asyncio.run(send_request(SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE))

    def test_status_code(self):
        assert self.data["status"] == SUCCESS

class TestSingleColumnTwoQubitNeighbouringGateReverse:
    @classmethod
    def setup_class(cls):
        cls.data = asyncio.run(send_request(SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE_REVERSE))

    def test_status_code(self):
        assert self.data["status"] == SUCCESS
