from data import data, point

class dataset:
    def __init__(self):
        self.list = []
        self.labels = ['']
    
    def clear(self):
        self.list = []
        self.labels = []
        self.labels.append('')
    
    def set(self, d : list[data]):
        self.list = d
        self.labels = []
        for i in range(len(d)):
            self.labels.append(d[i].label)