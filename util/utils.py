from constants import *
from square import Square


def coordinate_to_index(coordinate):
    """Takes coordinate (ex. 'g3') and returns index"""
    file_num, rank = coordinate
    return FILE_TO_NUM_DICTIONARY[file_num] + rank * 8 - 1

def index_to_coordinate(index):
    if index == None:
        return '-'
    file_num =  get_x(index)
    file = NUM_TO_FILE_DICTIONARY[file_num]
    rank = get_y(index)
    return file + str(rank + 1)

def xy_to_index(file, rank):
    return file + rank * 8

def get_x(index):
    return index % 8

def get_y(index):
    return index // 8