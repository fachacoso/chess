import constants


def coordinate_to_index(coordinate):
    """Takes coordinate and returns index
    >>> coordinate_to_index('b2'))
    9
    >>> coordinate_to_index('h5'))
    47
    """
    file_num, rank = coordinate
    return constants.FILE_TO_NUM_DICTIONARY[file_num] + int(rank) * 8 - 1

def index_to_coordinate(index):
    """Takes index and returns coordinate
    >>> index_to_coordinate(9))
    'b2'
    >>> index_to_coordinate(47))
    'h5'
    """
    if index == None:
        return '-'
    file_num =  get_x(index)
    file = constants.NUM_TO_FILE_DICTIONARY[file_num]
    rank = get_y(index)
    return file + str(rank + 1)

def xy_to_index(file, rank):
    """Takes x, y pair and returns index
    >>> xy_to_index(1, 2))
    17
    """
    
    return file + rank * 8

def get_x(index):
    """Takes index and returns x index
    >>> get_x(17))
    1
    """
    return index % 8

def get_y(index):
    """Takes index and returns y index
    >>> get_y(17))
    2
    """
    return index // 8