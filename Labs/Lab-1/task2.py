#Task 2
#input for 1 matrix
r1 = int(input("Enter the number of rows for matrix 1: "))
c1 = int(input("Enter the number of columns matrix 1 : "))
matrix1 = []
for i in range(r1):
    row = []
    for j in range(c1):
        row.append(int(input("enter val: ")))
    matrix1.append(row)
#print(matrix1)
#input for 2 matrix
r2 = int(input("Enter the number of rows matrix 2 : "))
c2 = int(input("Enter the number of columns matrix 2 : "))
matrix2 = []
for i in range(r2):
    row1 = []
    for j in range(c2):
        row1.append(int(input("enter val: ")))
    matrix2.append(row1)
#print(matrix2)


def matrix_multiplication(m1, m2):
    # List to store matrix multiplication result   4 by 4 matrix
    res = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for var1 in range(0, 4):
        for var2 in range(0, 4):
            for k in range(0, 4):
                res[var1][var2] += m1[var1][k] * m2[k][var2]
    return res


matrix3 = [matrix_multiplication(matrix1, matrix2)]
for o in range(0, 4):
    for m in range(0, 4):
        print(matrix3[o][m])

