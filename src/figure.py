import TkEasyGUI as eg

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from axis import axis
from data import data, color_list, marker_list, line_list
from ranges import ranges

class figure:
        def createCanvas(self, window_canvas):
            self.canvas = FigureCanvasTkAgg(self.figure, window_canvas)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
    
        def __init__(self, window_canvas):
            plt.rcParams["font.family"] = "Times New Roman"
            plt.rcParams['mathtext.fontset'] = 'stix'

            # 全体のフォントサイズの設定
            plt.rcParams["font.size"] = 24

            # グラフ目盛りの内向き設定
            plt.rcParams['xtick.direction'] = 'in'
            plt.rcParams['ytick.direction'] = 'in'
            plt.legend(fontsize=24,frameon=False)
            
            
            self.figure = plt.figure(figsize=(8, 6))
            
            self.createCanvas(window_canvas)
            
            self.axes = [axis('y1'), axis('y2'), axis('y3')]
            self.axes[0].data = self.figure.add_subplot(111)
            
            self.x_axis = axis('x')
        
        def clear(self):
            self.figure.clear()
            self.axes[0].data = self.figure.add_subplot(111)
            self.axes[0].data.cla()
            self.draw()
                        
        def draw(self):           
            for i in range(3):
                if(self.axes[i].enable == True):
                    self.axes[i].set(self.x_axis)
            
            h = []
            l = []
            for i in range(3):
                _h, _l = self.axes[i].data.get_legend_handles_labels()
                h.append(_h)
                l.append(_l)
            
            _h = h[0]
            _l = l[0]
            for i in range(1, len(h)):
                if self.axes[i].enable == True:
                    _h += h[i]
                    _l += l[i]

            plt.legend(_h, _l, fontsize=24, frameon=False)
            
            plt.tight_layout()
            self.canvas.draw()
            
            for i in range(1, 3):
                #self.axes[i+1].data = self.figure.add_subplot(111)
                self.axes[i].data.cla()
                self.axes[i].enable = False
            
        def plot(self, d:data):
            if d.id < 0:
                return
            if d.axis < 0 or d.axis > 2:
                return
            if d.enable == False:
                return
            
            if(self.axes[d.axis].enable == False):
                self.axes[d.axis].data = self.axes[0].data.twinx()
                self.axes[d.axis].data.set_axisbelow(True)
                self.axes[d.axis].enable = True
            
            x, y = d.get()
            np_x = np.array(x, dtype=np.float64)
            np_y = np.array(y, dtype=np.float64)
            if d.legend == True:
                if d.curve.type != 0:
                    _x, _y = d.curve.calc(d.data, self.x_axis.range)
                    np__x = np.array(_x, dtype=np.float64)
                    np__y = np.array(_y, dtype=np.float64)
                    self.axes[d.axis].data.plot(np__x, np__y, color=color_list[d.color], marker='', linestyle=line_list[d.curve.line], linewidth=1, label = d.label, zorder = 1)
                    self.axes[d.axis].data.scatter(np_x, np_y, color=color_list[d.color], marker=marker_list[d.marker], zorder = 2)
                else :    
                    self.axes[d.axis].data.scatter(np_x, np_y, color=color_list[d.color], marker=marker_list[d.marker], label = d.label, zorder = 2)
            else:
                if d.curve.type != 0:
                    _x, _y = d.curve.calc(d.data, self.x_axis.range)
                    np__x = np.array(_x, dtype=np.float64)
                    np__y = np.array(_y, dtype=np.float64)
                    self.axes[d.axis].data.plot(np__x, np__y, color=color_list[d.color], marker='', linestyle=line_list[d.curve.line], linewidth=1, zorder = 1)
                    self.axes[d.axis].data.scatter(np_x, np_y, color=color_list[d.color], marker=marker_list[d.marker], zorder = 2)

                else :    
                    self.axes[d.axis].data.scatter(np_x, np_y, color=color_list[d.color], marker=marker_list[d.marker], zorder = 2)

            