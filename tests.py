from logic import print_matrix
from logic import nextGen
matrix = [
    [0, 0, 1, 0],
    [1, 1, 0, 0],
    [0, 0, 1, 1],
    [1, 0, 0, 1]
]

wraped_matrix = [[0, 0, 1, 0] ,
          [1, 1, 0, 0]    ,
          [0, 0, 1, 1]   ,
          [1, 0, 0, 1]
          ]

gen = 1
print (f"{'matrix Generation'} {0}")
print_matrix(matrix)
print (f"{'wraped_matrix Generation'} {0}")
print_matrix(wraped_matrix)
for i in range(10):
    print (f"{'matrix Generation'} {gen}")
    print_matrix(matrix)
    print (f"{'wraped_matrix Generation'} {gen}")
    print_matrix(wraped_matrix)
    nextGen(matrix, gen,False)
    nextGen(wraped_matrix, gen,True)
    gen += 1




