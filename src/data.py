import numpy as np
import TkEasyGUI as eg
from curve import curve
from point import point

color_list = ['#000000', '#ff0000', '#0000ff', '#00ff00', '#ff8000', '#800080', '#808080', '#00ffff', '#ff00ff']
color_name = ['Black', 'Red', 'Blue', 'Green', 'Orange', 'Purple', 'Gray', 'Cyan', 'Magenta']

marker_list = ['', '.', 'o', 'v', '^', '<', '>', 'x', '+', 'd', '|', '-']
marker_name = ['None', '・', '〇', '▽', '△', '◁', '▷', '×', '+', '◇', '|', '-']

axis_type = ['x', 'y1', 'y2', 'y3']
yaxis_type = ['y1', 'y2', 'y3']
axis_id = [-1,0,1,2]

curve_list = ['None', 'PolyLine', 'Liner', 'PolyNomial', 'Log', 'Exponetial', 'Power', 'Moving Average']
line_list = ['-', '--', '-.', ':']
line_name = ['―――', '‐ ‐', '－・－', '・・・']


        


class data:
    def __init__(self, id:int, label:str):
        self.axis = 0
        self.data : list[point] = [] 
        self.id = id
        self.color = 0
        self.marker = 0
        self.enable = True
        self.legend = True
        self.label = label
        self.curve = curve()
    
    def add(self, p:point):
        self.data.append(p)
        
    def get(self):
        return [p.x for p in self.data], [p.y for p in self.data]

class data_wizard:
    def __init__(self, d:data):
        self.data = d
        
        self.layout = [
            [eg.Text('Data Name'), eg.InputText(d.label, key='-label-')],
        ]
        
        if d.id >= 0:
            self.layout.append([eg.Text('Axis'), eg.Combo(yaxis_type, default_value=yaxis_type[d.axis], key='-axis-')])
            self.layout.append([eg.Text('Color'), eg.Combo(color_name, default_value=color_name[d.color], key='-color-')])
            self.layout.append([eg.Text('Marker'), eg.Combo(marker_name, default_value=marker_name[d.marker], key='-marker-')])
            
            self.layout.append([eg.Frame('Curve', [
                [eg.Text('Curve Type'), eg.Combo(curve_list, default_value=curve_list[d.curve.type], key='-curve-')],
                [eg.Text('Line Type'), eg.Combo(line_name, default_value=line_name[d.curve.line], key='-line-')],
                [eg.Text('PloyNomial-N'), eg.InputText(d.curve.poly_n, key='-poly_n-')],
                [eg.Text('Moving-N'), eg.InputText(d.curve.poly_n, key='-move_n-')],
                [eg.Checkbox('Enable', default=d.enable, key='-Enable-'), eg.Checkbox('Legend', default=d.legend, key='-legend-')]
            ])])
            
        
        self.layout.append([eg.Button('OK', key='-ok-'), eg.Button('Cancel', key='-cancel-')])
        
        self.window = eg.Window('Data Setting', self.layout, finalize=True)
        
    def update(self)->data:
        while True:
            event, values = self.window.read()
            
            if event in (None, '-cancel-', eg.WINDOW_CLOSED):
                self.window.close()
                return None
            
            elif event == '-ok-':
                self.data.label = values['-label-']
                self.data.enable = values['-Enable-']
                self.data.legend = values['-legend-']
                
                if self.data.id >= 0:
                    self.data.axis = yaxis_type.index(values['-axis-'])
                    self.data.color = color_name.index(values['-color-'])
                    self.data.marker = marker_name.index(values['-marker-'])
                    self.data.curve.type = curve_list.index(values['-curve-'])
                    self.data.curve.line = line_name.index(values['-line-'])
                    self.data.curve.poly_n = int(values['-poly_n-'])
                    self.data.curve.move_sec = int(values['-move_n-'])
                    
                break
            
        self.window.close()
        return self.data