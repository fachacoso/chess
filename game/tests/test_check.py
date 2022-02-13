import pytest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import game_state
from testing_constants import *


class TestCheck:
    def test_check_displayed_in_move_object():
        NotImplemented
    
    def test_check():
        NotImplemented
        
    def test_pinned():
        NotImplemented
        
    def test_discovered():
        NotImplemented
        
    def test_cannot_castle():
        NotImplemented