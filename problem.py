import random as rd

def random_field(n):
    a = [[0] * n for i in range(n)]
    m = n * n // 2
    Q = [i for i in range(m)] + [i for i in range(m)]
    rd.shuffle(Q)
    
    for i in range(n):
        for j in range(n):
            a[i][j] =  Q[i*n +j]
    return a

def random_rotate_field(n):
    pass

class Problem:

    def __init__(self, n, start_time, gen_type = 1):
        self.n = n
        self.start_time = start_time
        self.field = None
        if gen_type == 1:
            self.field = random_field(n)
        else:
            self.field = random_rotate_field(n)
            

    def __str__(self):
        field = str(self.field)
        return "{" + '"startAt":' + str(self.start_time) +  "," + \
            '"problem": {' + \
            '"field": {' + \
            '"size":' + str(self.n) + ',' + \
            '"entities": ' + field + \
            '}' + \
            '}' + \
            '}'
    

