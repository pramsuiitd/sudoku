from typing import Tuple,List

def input_sudoku() -> List[List[int]]:
	"""Function to take input a sudoku from stdin and return
	it as a list of lists.
	Each row of sudoku is one line.
	"""
	sudoku= list()
	for _ in range(9):
		row = list(map(int, input().rstrip(" ").split(" ")))
		sudoku.append(row)
	return sudoku

def print_sudoku(sudoku:List[List[int]]) -> None:
	"""Helper function to print sudoku to stdout
	Each row of sudoku in one line.
	"""
	for i in range(9):
		for j in range(9):
			print(sudoku[i][j], end = " ")
		print()

def get_block_num(sudoku:List[List[int]], pos:Tuple[int, int]) -> int:   
    return 3*int((pos[0]-1)/3) + int((pos[1]-1)/3) + 1

def get_position_inside_block(sudoku:List[List[int]], pos:Tuple[int, int]) -> int:
    return ((pos[0] - 1)%3)*3 + ((pos[1] - 1)%3) + 1

def get_block(sudoku:List[List[int]], x: int) -> List[int]:
    i = ((x-1)//3)*3
    j = ((x-1)%3)*3
    C = []
    for a in range(i,i+3):
        for b in range(j,j+3):
            C.append(sudoku[a][b])
    return C

def get_row(sudoku:List[List[int]], i: int)-> List[int]:
    """This function takes an integer argument i and then returns
    the ith row. Row indexing have been shown above.
    """
    return sudoku[i-1]

def get_column(sudoku:List[List[int]], x: int)-> List[int]:
    """This function takes an integer argument i and then
	returns the ith column. Column indexing have been shown above.
	"""
    A = []
    for i in range(9) : A.append(sudoku[i][x-1])
    return A

def find_first_unassigned_position(sudoku : List[List[int]]) -> Tuple[int, int]: 
    """This function returns the first empty position in the Sudoku. 
	If there are more than 1 position which is empty then position with lesser
	row number should be returned. If two empty positions have same row number then the position
	with less column number is to be returned. If the sudoku is completely filled then return `(-1, -1)`.
	"""
    for i in range(9): 
        for j in range(9):
            if sudoku[i][j] == 0: return (i+1,j+1)
    return (-1,-1)

def valid_list(lst: List[int])-> bool:
    """This function takes a lists as an input and returns true if the given list is valid. 
	The list will be a single block , single row or single column only. 
	A valid list is defined as a list in which all non empty elements doesn't have a repeating element.
	"""
    A = [0,0,0,0,0,0,0,0,0]
    for i in range(9):
        if lst[i] != 0 : A[lst[i]-1] += 1
    for j in A:
        if j > 1: return False

    return True

def valid_sudoku(sudoku:List[List[int]])-> bool:
    """This function returns True if the whole Sudoku is valid.
	"""
    for i in range(1,10):
        if (valid_list(get_row(sudoku,i))) == False : return False
        if (valid_list(get_block(sudoku,i))) == False : return False
        if (valid_list(get_column(sudoku,i))) == False : return False
    return True

def get_candidates(sudoku:List[List[int]], pos:Tuple[int, int]) -> List[int]:
    C = []
    a = sudoku[pos[0]-1][pos[1]-1]
    for i in range(1,10):
        sudoku[pos[0]-1][pos[1]-1] = i
        if valid_sudoku(sudoku):C.append(i)
        sudoku[pos[0]-1][pos[1]-1] = a
    return C

def make_move(sudoku:List[List[int]], pos:Tuple[int, int], num:int) -> List[List[int]]:
    """This function fill `num` at position `pos` in the sudoku and then returns
	the modified sudoku.
	"""
    sudoku[pos[0]-1][pos[1]-1] = num
    return sudoku

def undo_move(sudoku:List[List[int]], pos:Tuple[int, int]):
    """This function fills `0` at position `pos` in the sudoku and then returns
	the modified sudoku. In other words, it undoes any move that you 
	did on position `pos` in the sudoku.
	"""
    sudoku[pos[0]-1][pos[1]-1] = 0
    return sudoku

def find_all_unassigned_loc(sudoku : List[List[int]]) -> List[Tuple] :
    loc =[]
    pos = find_first_unassigned_position(sudoku)
    while pos != (-1,-1) :
        pos = find_first_unassigned_position(sudoku)
        if pos != (-1,-1):
            make_move(sudoku,pos,1)
        loc.append(pos)
    
    if (-1,-1) in loc:
        loc.remove((-1,-1))
    for pos in loc:
        undo_move(sudoku,pos)
    return loc

def least_freq_loc(sudoku: List[List[int]], ls_empty:List[Tuple[int,int]]) -> Tuple[Tuple[int,int], int]:
    freq = []
    for i in range(len(ls_empty)):
        freq.append(len(get_candidates(sudoku,ls_empty[i])))
    if len(freq) == 0:
        return ((-1,-1),0)
    min_freq = min(freq)
    index = freq.index(min_freq)
    return (ls_empty[index],index)

def sudoku_solver(sudoku: List[List[int]]) -> Tuple[bool, List[List[int]]]:
    """ This is the main Sudoku solver. This function solves the given incomplete Sudoku and returns 
	true as well as the solved sudoku if the Sudoku can be solved i.e. after filling all the empty positions the Sudoku remains valid.
	It return them in a tuple i.e. `(True, solved_sudoku)`.

	However, if the sudoku cannot be solved, it returns False and the same sudoku that given to solve i.e. `(False, original_sudoku)`
	"""
    ls_empty = find_all_unassigned_loc(sudoku)
    return solver(sudoku, ls_empty)

def solver(sudoku: List[List[int]], ls_empty : List[Tuple[int, int]]):
    n = len(ls_empty)
    ls_fill = []
    pos,index = least_freq_loc(sudoku,ls_empty)
    ls_fill.append(pos)
    ls_empty.pop(index)
    copy = sudoku.copy() 
    i = 0
    gc_j_list = []
    back_trace_not = True
    if valid_sudoku(sudoku) == False : return (False,sudoku)
    while i < n:
        if len(ls_empty) == 0:
            if valid_sudoku(sudoku):
                pos = find_first_unassigned_position(sudoku)
                gc = get_candidates(sudoku,pos)
                if len(gc) == 0:return (False,copy)
                else:
                    make_move(sudoku, pos,gc[0])
                    return (True, sudoku)
            else: return(False,copy)
        if back_trace_not:
            gc_j_list.append([get_candidates(sudoku,ls_fill[i]),0])
            i  = len(gc_j_list) - 1
            if i == -1 : return (False,copy)

        if len(gc_j_list[i][0]) == 0 or len(gc_j_list[i][0]) <= gc_j_list[i][1] : 
            gc_j_list.pop()
            undo_move(sudoku,ls_fill[i])
            pos = ls_fill.pop()
            ls_empty.append(pos)
            i -= 1
            if i == -1 : return (False,copy)
            gc_j_list[i][1] += 1
            back_trace_not = False
            continue
        # pos_m = l[i]
        # pointer_gc = gc_j_list[i][1]
        # num = gc_j_list[i][0][gc_j_list[i][1]]

        make_move(sudoku, ls_fill[i], gc_j_list[i][0][gc_j_list[i][1]])
        pos,index = least_freq_loc(sudoku,ls_empty)
        ls_fill.append(pos)
        ls_empty.pop(index)
        back_trace_not = True
        i += 1
        if len(gc_j_list) == 0:
            return (False, copy)
    return (True , sudoku)

def in_lab_component(sudoku: List[List[int]]):
	print("Testcases for In Lab evaluation")
	print("Get Block Number:")
	print(get_block_num(sudoku,(4,4)))
	print(get_block_num(sudoku,(7,2)))
	print(get_block_num(sudoku,(2,6)))
	print("Get Block:")
	print(get_block(sudoku,3))
	print(get_block(sudoku,5))
	print(get_block(sudoku,9))
	print("Get Row:")
	print(get_row(sudoku,3))
	print(get_row(sudoku,5))
	print(get_row(sudoku,9))

if __name__ == "__main__":
    sudoku = input_sudoku()
    possible, sudoku = sudoku_solver(sudoku)
    if possible:
        print("Found a valid solution for the given sudoku :)")
        print_sudoku(sudoku)

    else:
        print("The given sudoku cannot be solved :(")
        print_sudoku(sudoku)


# Find the location with the least frequency - say (x,y)
# l[i] in my program is a list which is generated previously, instead of that update that list dynamically
# How : make a get least pos such that freq is least func. Now think when l[i] needs to be updated/poped?
# Also require a list which stores the positions which are empty - why - to get the frequency
# This list say ls_empty - and ls_full - have sum as my original l[i]
