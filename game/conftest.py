import pytest
from pieces.piece import Piece

'''
Pytest fixtures
'''

@pytest.fixture(scope="function")
def tear_down():
    """ Reset test environment for next test """
    yield
    Piece.reset_pieces()