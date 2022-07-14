import time
import os
import sys
import test


with open(os.path.join(sys.path[0], "p096_sudoku.txt") , "r") as f :
    lines = f.readlines()
    
l = []
for i in range(50):
    sudoku = []
    for j in range(i*10 + 1, ((i+1)*10)):
        string_1 = lines[j]
        row = []
        for k in range(9):
            row.append(int(string_1[k]))
        sudoku.append(row)
    l.append(sudoku)
time_lst = []
for i in range(50) :
    start = time.time()
    possible, sudoku = test.sudoku_solver(l[i])
    if possible:
        print("\nFound a valid solution for the given sudoku :)")
        test.print_sudoku(sudoku)
    else:
        print("\nThe given sudoku cannot be solved :(")
        test.print_sudoku(sudoku)
    end = time.time()
    t = end - start
    if t == None: t = 0
    print("\nExecution time is : ", t)
    time_lst.append(t)
    print(i)

time_lst = time_lst.sort()
print(time_lst)
# sum = 0
# for i in range(50):
#     sum += float(time_lst[i])

# mean = sum/50
# median = (time_lst[25] + time_lst[24])/2
# print("Mean : ", mean)
# print("Median : ", median)
# print("Total : ", sum)
