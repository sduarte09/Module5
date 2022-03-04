# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 19:43:40 2022

@author: mab020
"""
# Importing the Libraries
import numpy as np
import BWC_backend
from bokeh.io import output_file
from bokeh.layouts import widgetbox, row,column
from bokeh.models.widgets import Button, RadioButtonGroup, Dropdown, NumericInput
from bokeh.plotting import figure, curdoc
#from bokeh.models.callbacks import CustomJS
output_file("BWC_GUI.html")


#Figure
s1 = figure(plot_width=600, plot_height=300, title=None)
# Scheme choise
menu = [("Implicit", "item_1"), ("Explicit", "item_2")]
dropdown = Dropdown(label="Scheme choice:", button_type="warning", menu=menu)
button_group = RadioButtonGroup(labels=["Implicit", "Explicit"], active=None)
# Inputs
L = NumericInput(value=10000, title="L (m)",mode = 'float', high = None,low = 0)
b = NumericInput(value=100, title="b (m)",mode = 'float', high = None,low = 0)
So = NumericInput(value=0.0006, title="I (-)",mode = 'float', high = None,low = 0)
C = NumericInput(value=45, title="C (m1/2/S)",mode = 'float', high = None,low = 0)
Q = NumericInput(value=500, title="Q (m3/S)",mode = 'float', high = None,low = 0)
hint = NumericInput(value=5.0, title="int_h (m)",mode = 'float', high = None,low = 0)
dx = NumericInput(value=100, title="dx (m)", mode = 'float',high = None,low = 0)
No_itter = NumericInput(value=15, title="No. Iteration", mode = 'int',high = None,low = 0,visible = False)
numric = [L,b,So,C,Q,hint,dx,No_itter]
tit = ["L (m)","b (m)","I (-)""C (m1/2/S)","Q (m3/S)","int_h (m)","dx (m)","No. Iteration"]

def choise(active):
    if active == 0:
         No_itter.visible = True
    else:
        No_itter.visible = False
button_group.on_click(choise)
# Buttons
help = Button(label="Help")
Load_from_file = Button(label="Load Data From file")
Show_equation = Button(label="Show equation")
Save_to_file = Button(label="Save Data to file")
Draw_BWC = Button(label="Draw BWC")
Save_Graph = Button(label="Save Graph")

#def modify_doc():

# add a callback to a widget

def update_plot():
        s1.renderers=[]
        len = float(L.value)
        wid = float(b.value)
        I = float(So.value)
        flow = float(Q.value)
        chezy  = float(C.value)
        int_h = float(hint.value)
        DX = float(dx.value)
        itter = int(No_itter.value)
        check =  button_group.active #
        if check ==1: # 'Explicit':
            x = np.array(BWC_backend.BWC_Explict(len,wid ,I,chezy,flow,DX, int_h))
            s1.varea(x=x[0], y1=x[3], y2=x[2], fill_color="lightblue")
            s1.varea(x=x[0], y1=x[2], y2=0, fill_color="darkgoldenrod")
            s1.line(x[0], x[3],  line_width=3, line_color='blue')
            s1.line(x[0], x[2],  line_width=3, line_color='black')
            
        elif check == 0: # 'Implicit':
            x = np.array(BWC_backend.BWC_Implict(len,wid ,I,chezy,flow,DX, int_h,itter))
            s1.varea(x=x[0], y1=x[3], y2=x[2], fill_color="lightblue")
            s1.varea(x=x[0], y1=x[2], y2=0, fill_color="darkgoldenrod")
            s1.line(x[0], x[3],  line_width=3, line_color='blue')
            s1.line(x[0], x[2],  line_width=3, line_color='black')

Draw_BWC.on_click(update_plot)

# create a layout for everything
layout = widgetbox(row(column(),column(help)),column(row(column(Load_from_file,L,b,So,C,Q,hint,dx,),s1)) #
                    ,column(row(button_group,Show_equation,Save_to_file,Save_Graph))
                    ,column(No_itter,Draw_BWC))

# add the layout to curdoc 
curdoc().add_root(layout)

# bokeh serve --show BWC_GUI.py
