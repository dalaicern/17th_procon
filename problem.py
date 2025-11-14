import random as rd
import copy
from datetime import datetime
import threading

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


def eval_score(a, n):
    score = 0
    for i in range(n):
        for j in range(n):
            if a[i][j] >= 0:
                if i + 1 < n and a[i][j] == a[i+1][j]:
                    score += 1
                    a[i][j] = a[i+1][j] = -1
                elif j + 1 < n and a[i][j] == a[i][j+1]:
                    score += 1
                    a[i][j] = a[i][j+1] = -1
    return score

def rotate(a, n, x, y, size):
    b = [[0] * size for i in range(size)]
    for i in range(size):
        for j in range(size):
            b[i][j] = a[x + i][y + j]

    for i in range(size):
        for j in range(size):
            a[x + j][y + size - 1 - i] = b[i][j]


class Problem:
    def __init__(self, n, start_time, gen_type = 1):
        self.n = n
        self.start_time = start_time
        self.field = None
        if gen_type == 1:
            self.field = random_field(n)
        else:
            self.field = random_rotate_field(n)

        self.teams = {}
        self.score_board = []
        self.lock = threading.Lock()
            

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

    def add_team(self, team):
        self.lock.acquire()
        self.teams[team] = (0, 0)
        self.lock.release()
        
    def new_submission(self, team, d):
        submission_time = int(datetime.now().timestamp())
        a = copy.deepcopy(self.field)
        for op in d.ops:
            x, y, size = op.x, op.y, op.n
            if x + size > self.n or y + size > self.n or x < 0 or y < 0:
                print('invalid ops', x, y, size, self.n)
                return -1, submission_time
            rotate(a, self.n, x, y, size)

        score = eval_score(a, self.n)
        self.lock.acquire()
        self.teams[team] = (score, submission_time)
        self.lock.release()
        return score, submission_time
