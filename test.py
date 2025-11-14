from problem import Problem
import problem
a = [\
     [1, 2, 3, 4],
     [1, 2, 3, 4],
     [0, 0, 5, 5],
     [6, 6, 7, 7]
    ]
N = 4
# problem.rotate(a, 5, 1, 1, 3)
for i in range(N):
    for j in range(N):
        print(a[i][j], end = ' ')
    print()

print(problem.eval_score(a, N))
