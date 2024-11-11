import matplotlib.pyplot as plt
import TkEasyGUI as eg
import numpy as np
from ranges import ranges

class axis:
    def __init__(self, type = 'x'):
        self.range = ranges(0, 3)
        self.tick_range = ranges(0, 10)
        self.tick_label = ['0', '', '2', '', '4', '', '6', '', '8', '', '10']
        self.label = ''
        self.scale = 'linear'
        
        self.type = type;
        self.enable = type == 'x' or type == 'y1'
        if(type == 'x'):
            self.label = 'X axis'
        elif(type == 'y1'):
            self.label = 'Y1 axis'
        elif(type == 'y2'):
            self.label = 'Y2 axis'
        elif(type == 'y3'):
            self.label = 'Y3 axis'
        else:
            self.enable = False
            self.label = ''
            
        self.data = plt.subplot(111)
        
    def set(self, xaxis):
        self.data.set_xlabel(xaxis.label)
        self.data.set_ylabel(self.label)
        
        self.data.set_xlim(xaxis.range.min, xaxis.range.max)
        self.data.set_ylim(self.range.min, self.range.max)
        
        self.data.set_xticks(np.linspace(xaxis.tick_range.min, xaxis.tick_range.max, len(xaxis.tick_label)))
        self.data.set_yticks(np.linspace(self.tick_range.min, self.tick_range.max, len(self.tick_label)))
        self.data.set_xticklabels(xaxis.tick_label)
        self.data.set_yticklabels(self.tick_label)
        
        self.data.set_axisbelow(True)
        
class axis_wizard:
    def __init__(self, d:axis):
        self.d = d
        
        tick_label = ''
        for i in range(len(d.tick_label)):
            tick_label += d.tick_label[i]
            if(i < len(d.tick_label) - 1):
                tick_label += ','
        
        self.layout = [
            [eg.Text('Axis Name'), eg.InputText(d.label, key='-label-')],
            [eg.Text('Range'), eg.InputText(str(d.range.min), key='-range_min-'), eg.InputText(str(d.range.max), key='-range_max-')],
            [eg.Text('Tick Range'), eg.InputText(str(d.tick_range.min), key='-tick_range_min-'), eg.InputText(str(d.tick_range.max), key='-tick_range_max-')],
            [eg.Text('Tick Label'), eg.InputText(str(tick_label), key='-tick_label-')],
            [eg.Button('OK', key='-ok-'), eg.Button('Cancel', key='-cancel-')]
        ]
        
        self.window = eg.Window('Axis Edit', self.layout, finalize=True)
        
    def update(self):
        while True:
            event, values = self.window.read()
            
            if event in (None, '-cancel-', eg.WINDOW_CLOSED):
                break
            
            elif event == '-ok-':
                self.d.label = values['-label-']
                self.d.range.min = float(values['-range_min-'])
                self.d.range.max = float(values['-range_max-'])
                self.d.tick_range.min = float(values['-tick_range_min-'])
                self.d.tick_range.max = float(values['-tick_range_max-'])
                
                self.d.tick_label = values['-tick_label-'].split(',')
                
                break
        self.window.close()
        return self.d