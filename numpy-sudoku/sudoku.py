import numpy as np
import collections
import itertools

# Part 1:
def string_puzzle_to_arr(puzzle):
    return np.array([list(line.strip()) for line in puzzle.split('\n') if line.strip()], dtype=np.int)

class Board:
    def __init__(self, puzzle):
        
        # Check if the incoming puzzle is string
        if isinstance(puzzle, str):
            rows = [ list(r.strip()) for r in puzzle.split('\n') if r.strip() ]
            self.arr = np.array(rows, dtype=int)
        else:
            self.arr = puzzle
        
    def get_row(self, row_index):
        return self.arr[row_index]

    def get_column(self, col_index):
        return self.arr[:, col_index]
    
    def get_block(self, pos_1, pos_2):
        
        # Get the row starting and ending index of the entire board
        r_start = pos_1 * 3
        r_end = r_start + 3
        
        # Get the column starting and ending positions for the entire board
        c_start = pos_2 * 3
        c_end = c_start + 3
        
        # Return only the section of the board corresponding to the correct block
        return self.arr[r_start:r_end, c_start:c_end]
    
    def iter_rows(self):
        final = list()
        for row in self.arr:
            final.append(row)
            
        return final
            
    
    def iter_columns(self):
        final = list()
        
        for i in range(self.arr.shape[1]):
            final.append(self.get_column(i))
            
        return final
    
    def iter_blocks(self):
        
        final = list()
        
        for i in range(3):
            for j in range(3):
                
                final.append(self.get_block(i, j))
        
        return final
    
# Part 2:

def is_subset_valid(arr):
    clean_arr = arr[arr > 0]
    arr_set = set(clean_arr)
    if len(arr_set) == clean_arr.size:
        return True
    return False

def is_valid(board):
    
    tests = list() # Holds all of the True and False values of the tests being run
    
    # Test all rows 
    for row in board.iter_rows():
        tests.append(is_subset_valid(row))
    
    # Test all columns
    for col in board.iter_columns():
        tests.append(is_subset_valid(col))
        
    # Test all Blocks
    for block in board.iter_blocks():
        tests.append(is_subset_valid(block))
        
    # Return True if all values in tests are True, False otherwise
    return all(tests)

# Part 3:

def find_empty(board):
    arr = np.stack(np.where(board.arr == 0), axis=-1)
    
    return arr

def is_full(board):
    return bool((board.arr != 0).all())

def find_possibilities(board, x, y):
    
    # Stores the currently available items for the given empty position
    available = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    
    # Get block position
    block_x = x // 3
    block_y = y // 3
    
    # Get the block, row, and column for the board position
    block = board.get_block(block_x, block_y)
    row = board.get_row(x)
    col = board.get_column(y)
    
    # concatenate all of the arrays for block, row, column into one array 
    con = np.concatenate((block, row, col), axis=None)
    
    # Get all of the unique values from block, row, and col
    taken = np.unique(con)
    # Create mask for the available values not already taken
    available = np.setdiff1d(available, taken)
    
    # Return the available values
    return available


# Part 4:

def adapt_long_sudoku_line_to_array(line):
    
    return np.array([ r.strip() for r in line ], dtype=int).reshape(9, 9)


def read_sudokus_from_csv(filename, read_solutions=False):
    pos = 0
    # Read all of the data from the file as strings and skip the header row
    all_data = np.genfromtxt(filename, delimiter = ',', dtype=str, skip_header=1)
    # Determine the position to be used for the array (quizzes or solutions)
    if read_solutions:
        pos = 1
        
    # Create the final 3d array
    arr_3d = np.array([ adapt_long_sudoku_line_to_array(s[pos]) for s in all_data ])
    
    return arr_3d


def detect_invalid_solutions(filename):
    # Read all of the solutions from the file
    arr_3d = read_sudokus_from_csv(filename, read_solutions=True)
    invalid_boards = list() # holds all of the invalid boards in arr_3d
    
    # Cycle through all of the solution boards and test for validity
    for puzzle in arr_3d:
        b = Board(puzzle)   # Create a board object
        valid = is_valid(b) # Pass board to function checking for validity
        if not valid:       # If not valid add the boards inner numpy array to the invalid boards list
            invalid_boards.append(b.arr)
    
    # Create the final numpy array and return it
    final_arr = np.array(invalid_boards)
    return final_arr