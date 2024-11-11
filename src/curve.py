import numpy as np
from ranges import ranges
import math
from point import point

def pnt(x, y):
    p = point()
    p.x = x
    p.y = y
    return p

#y= a * x + b
def LinearRegression (d: list[point]) :
    sum_x : float = 0
    sum_y : float = 0
    sum_xy : float = 0
    sum_x2 : float = 0
    for p in d:
        sum_x += p.x
        sum_y += p.y
        sum_xy += p.x * p.y
        sum_x2 += p.x * p.x
    
    n = len(d)
    a = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
    b = (sum_x2 * sum_y - sum_xy * sum_x) / (n * sum_x2 - sum_x * sum_x)
    return a, b


#y = a * x^b
def PowerRegression (d: list[point]) :
    log_data:list[point] = []
    for p in d:
        if p.x <= 0 :
            continue
        
        if p.y <= 0 :
            continue
        
        log_data.append(pnt(math.log10(p.x), math.log10(p.y)))
    
    B, A = LinearRegression(log_data)    
    a = pow(10, A)
    b = B
    return a, b


#y = a * exp(b * x)
def ExponentialRegression (d: list[point]) :
    log_data:list[point] = []
    for p in d :
        if p.y <= 0 :
            continue
        
        log_data.append(pnt(p.x, math.log(p.y)))
    
    B, A = LinearRegression(log_data)
    a = math.exp(A)
    b = B
    return a, b


#y = a * log(x) + b
def LogarithmicRegression (d: list[point]) :
    log_data:list[point] = []

    for p in d:
        if p.x <= 0 :
            continue
        
        if p.y <= 0 :
            continue
        
        log_data.append(pnt(math.log(p.x), p.y))
    
    A, B = LinearRegression(log_data)
    a = A
    b = B
    return a, b


#y=a*x^n + b*x^(n-1) + ... + z
def PolynomialRegression (d: list[point], n) :
    matrix = [[]]

    for i in range(n + 1) :
        matrix.append([])
        for j in range(n + 2) :
            matrix[i].append(0)

    for i in range(n + 1) :
        for j in range(n + 1) :
            for p in d:
                matrix[i][j] += pow(p.x, i + j)
            
        
        for p in d:
            matrix[i][n + 1] += pow(p.x, i) * p.y
        
    
    for i in range(n):
        for j in range(i + 1, n + 1) :
            r = matrix[j][i] / matrix[i][i]
            for k in range(i, n + 2) :
                matrix[j][k] -= r * matrix[i][k]
            
        
    
    a = []
    for i in range(n + 1) :
        a.append(0)
    
    for i in range(n, 0, -1):
        for j in range(i + 1, n + 1) :
            matrix[i][n + 1] -= matrix[i][j] * a[j]
        
        a[i] = matrix[i][n + 1] / matrix[i][i]
    
    return a


def MovingAverage (d: list[point], n) :
    ret = []

    for i in range(len(d)) :
        sum = 0
        count = 0
        j = i
        for j in range(j, min(len(d), i + n)):
            sum += d[j].y
            count += 1
        
        ret.append(pnt(d[j-1].x, sum / count))
    
    return ret




class curve:
    def __init__(self):
        self.x = []
        self.y = []
        self.type = 1
        self.line = 0
        self.poly_n = 2
        self.move_sec = 2
        
    def calc(self, d: list[point], x : ranges, accuracy = 1000) :
        _x = [d.x for d in d]
        min_x = min(_x)
        max_x = max(_x)
        delta = (x.max - x.min) / accuracy
        min_x = min(min_x, x.min - delta)
        max_x = max(max_x, x.max + delta)
        
        values: list[point] = []
        if self.type == 0:
            pass

        elif self.type == 1:
            values = d

        elif self.type == 2 :
            a, b = LinearRegression(d)
            for i in np.arange(min_x, max_x, delta) :
                values.append(pnt(i, a * i + b))
        
        elif self.type == 3 :
            a, b = PowerRegression(d)
            for i in np.arange(min_x, max_x, delta) :
                values.append(pnt(i, a * math.pow(i, b)))    
        
        elif self.type == 4 :
            a, b = ExponentialRegression(d)
            for i in np.arange(min_x, max_x, delta) :
                values.append(pnt(i, a * math.exp(b * i)))
            
        
        elif self.type == 5 :
            a, b = LogarithmicRegression(d)
            for i in np.arange(min_x, max_x, delta) :
                if i <= 0 :
                    continue
                
                values.append(pnt(i, a * math.log(i) + b))
            
        
        elif self.type == 6 :
            a = PolynomialRegression(d, self.poly_n)
            for i in np.arange(min_x, max_x, delta) :
                y = 0    
                for j in range(self.poly_n + 1) :
                    y += a[j] * pow(i, j)
                
                values.append(pnt(i, y))
            
        
        elif self.type == 7 :
            values = MovingAverage(d, self.move_sec)    
    
        return [p.x for p in values], [p.y for p in values]