import numpy as np
from data import data, point
import csv

def process_data(path : str) -> list[data]:
    with open(path, 'r', encoding='UTF-8') as f:
        ext = path.split('.')[-1]
        delimiter = ','
        if ext == 'tsv':
            delimiter = '\t'
        reader = csv.reader(f, delimiter=delimiter)
        header = True
        data_list = []
        ret = []
        labels = []
        for row in reader:
            if header:
                for i in range(len(row)):
                    labels.append(row[i])
                    data_list.append([])
                header = False
            else:
                for i in range(len(row)):
                    data_list[i].append(row[i])
        
        x = data_list[0]
        
        ret.append(data(-1, labels[0]))
        for i in range(1, len(data_list)):
            d = data(i-1, labels[i])
            for j in range(len(x)):
                _x = 0.0
                _y = 0.0
                try:
                    _x = float(x[j])
                    _y = float(data_list[i][j])
                except:
                    continue
                p = point()
                p.x = _x
                p.y = _y
                d.add(p)
            d.axis = 0
            ret.append(d)
        
        return ret
        
            
        

