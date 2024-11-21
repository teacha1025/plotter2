import TkEasyGUI as eg
import figure
from data import data_wizard, axis_type
from axis import axis_wizard
from process_data import process_data
from dataset import dataset

class main_window:
    def __init__(self):
        self.dataset = dataset()
        
        layout = [[
        eg.Frame('',[
            [eg.Canvas(key='-CANVAS-')],
            [eg.Button('Open', key='-open-'), eg.Button('Clear',key='-clear-'), eg.Button('Save', key='-save-'), eg.Button('Exit', key='-exit-')]
        ]),
        eg.Frame('',[
            [eg.Text('Axis Edit')],
            [eg.Combo(axis_type, default_value=axis_type[0], key='-axis_edit_combo-', readonly=True), eg.Button('Edit', key='-axis_edit-')],
            [eg.Text('Data Edit')],
            [eg.Combo(self.dataset.labels, default_value=self.dataset.labels[0], key='-data_edit_combo-', readonly=True), eg.Button('Edit', key='-data_edit-')],
        ])     
        ]]

        self.window = eg.Window('Plot', layout, finalize=True)

        self.fig = figure.figure(self.window['-CANVAS-'].TKCanvas)

    def update(self):
        while True:
            event, values = self.window.read()

            if event in (None, '-exit-', eg.WINDOW_CLOSED):
                break
            
            elif event == '-open-':
                path = eg.popup_get_file(title='Select file', file_types=[('CSV file', '*.csv *.tsv')], multiple_files=False)
                if path != None and path != '':
                    d = process_data(path)
                    self.dataset.set(d)
                    
                    self.window['-data_edit_combo-'].set_values(self.dataset.labels)
                    self.window['-data_edit_combo-'].set_value(self.dataset.labels[0])
                    
                    self.fig.clear()
                    for d in self.dataset.list:
                        self.fig.plot(d)
                    self.fig.draw()
                
            
                
            elif event == '-clear-':
                self.fig.clear()
                
            elif event == '-save-':
                title = eg.popup_get_file(title="Select file to save", save_as=True)     
                if title != None and title != '':
                    pass 
                self.fig.figure.savefig(title)
                
            
            elif event == '-axis_edit-':
                i = axis_type.index(values['-axis_edit_combo-'])-1
                if i >= 0:
                    editor = axis_wizard(self.fig.axes[i])
                    d = editor.update()
                    if d is not None:
                        self.fig.axes[i] = d
                        self.fig.draw()
                        
                else:
                    editor = axis_wizard(self.fig.x_axis)
                    d = editor.update()
                    if d is not None:
                        self.fig.x_axis = d
                        self.fig.draw()
                
            elif event == '-data_edit-':
                editor = data_wizard(self.dataset.list[self.dataset.labels.index(values['-data_edit_combo-'])])
                d = editor.update()
                if d is not None:
                    self.dataset.list[self.dataset.labels.index(values['-data_edit_combo-'])] = d
                    self.fig.clear()
                    for d in self.dataset.list:
                        self.fig.plot(d)
                    self.fig.draw()

        self.window.close()
        
        
main = main_window()

if __name__ == '__main__':
    main.update()