# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 20:18:37 2022

@author: qli003
"""
from cProfile import label
from turtle import left
from bokeh.layouts import row,column
from bokeh.models import Div, TextInput, Button, Slider
from bokeh.io import output_file, show, export_png
from bokeh.plotting import figure, show,curdoc
import numpy as np

# output_file("my_GUI.html")

# set up textarea (div)
top = Div(
    text="""
          <h1 style="width:800px; height:40px;text-align:center;border-style:solid">Calculate Backward Curve</h3>
          """,
    width = 800,
    height = 60,
    margin=[0,0,0,15],
)
subtitle1 = Div(
    text="""
          <p>Input</p>
          """,
    width=150,
    height=30,
    margin = [0,0,0,15],
)

# set up textarea (div)
channel_length_textarea = Div(
    text="""
          <p>L (Channel Length):</p>
          """,
    width=150,
    height=30,
    margin = [0,0,0,30],
)

channel_length_slider_input = Slider(start=5000, end=20000, value=5000, step=100, width = 150)
L = row(channel_length_textarea,channel_length_slider_input)

# set up textarea (div)
channel_width_textarea = Div(
    text="""
          <p>b (Channel Width):</p>
          """,
    width=150,
    height=30,
    margin = [0,0,0,30],
)

channel_width_slider_input = Slider(start=10, end=100, value=50, step=1, width = 150)
b = row(channel_width_textarea,channel_width_slider_input)

# set up textarea (div)
Q_textarea = Div(
    text="""
          <p>Q (Discharge):</p>
          """,
    width=150,
    height=30,
    margin = [0,0,0,30],
)

Q_slider_input = Slider(start=10, end=1000, value=50, step=1, width = 150)
Q = row(Q_textarea,Q_slider_input)

# set up textarea (div)
C_textarea = Div(
    text="""
          <p>C (Chezy Coefficient):</p>
          """,
    width=150,
    height=30,
    margin = [0,0,0,30],
)
C_slider_input = Slider(start = 1, end = 1000, value = 45, step = 1, width = 150)
C = row(C_textarea,C_slider_input)

# set up textarea (div)
h0_textarea = Div(
    text="""
          <p>Water Depth at downstream:</p>
          """,
    width=150,
    height=30,
    margin = [0,0,0,30],
)
h0_slider_input = Slider(start = 1, end = 20, value = 3, step = 1, width = 150)
h0 = row(h0_textarea,h0_slider_input)

# set up textarea (div)
S0_textarea = Div(
    text="""
          <p>S0 (Slope):</p>
          """,
    width=150,
    height=30,
    margin = [0,0,0,30],
)

S0_slider_input = Slider(start = 0, end = 0.1, value = 0.001, step = 0.0001, width = 150)
S0 = row(S0_textarea,S0_slider_input)

# set up textarea (div)
dx_textarea = Div(
    text="""
          <p>dx (Distance Step):</p>
          """,
    width=150,
    height=30,
    margin = [0,0,0,30],
)

dx_slider_input = Slider(start = 10, end = 1000, value = 100, step = 10, width = 150)
dx = row(dx_textarea,dx_slider_input)

input = column(subtitle1,L,b,Q,C,h0,S0,dx)




p = figure(title='Back water curve', x_axis_label='Distance [m]', y_axis_label='Height [m]',width = 500, height = 340)
####################################################################


def BWC():
    global x
    global hg                 # vertical height due to bed slope hg(i+1) = x(i+1)*s0
    global hw 
    print('Run BWC...')
    
    # Define variables
    b = int(channel_width_slider_input.value)          #m
    Q = int(Q_slider_input.value)        #m3/s
    c = int(C_slider_input.value)
    S0 = float(S0_slider_input.value)
    dx = int(dx_slider_input.value)       #m
    h0 = int(h0_slider_input.value)      # depth at the downstream end
    X = int(channel_length_slider_input.value)            #m

    #initial values
    h = [h0]
    x = [0]
    hg = [0]                 # vertical height due to bed slope hg(i+1) = x(i+1)*s0
    hw = [h0]
    computations = int(X/dx)+1

    for i in range (1, computations):
        x.append(dx*i)
        h.append(h[i-1] + dx*((Q**2/(c**2*h[i-1]**3*b**2))-S0))    # Explicit h
        hg.append(x[i]*S0)       # hg(i+1) = x(i+1) * S0
        hw.append(h[i]+hg[i])    # hw(i+1) = hg(i+1) + h(i+1) 
    print('Plot....')
    p.renderers = []
    # add a line renderer with legend and line thickness to the plot
    p.line(x,hg,legend_label = 'slope of bed level', line_width = 2)
    p.line(x, hw,legend_label = 'Water Level', line_width = 2)
    print('Done.')
    button_save_data.disabled = False
    button_save_img.disabled = False


    

def save_data():
    print('Save...')
    res = np.array([x,hg,hw]).T
    np.savetxt('Exercise/Group6_Li_and_Derrick/BWC_data.txt',res)
    print('Done.')

def save_img():
    print('Plot...')
    export_png(p, filename='Exercise/Group6_Li_and_Derrick/BWC_plot.png')
    print('Done.')
###################################################################


subtitle2 = Div(
    text="""
          <p>Output</p>
          """,
    width=150,
    height=30,
    margin = [0,0,0,15],
)
ouput = column(subtitle2,p)
main = row(input,ouput)

button_calculate = Button(label= 'Calculate and Display',
    width = 150,
    height = 30,
)


button_save_data = Button(label = "Save Data",
    width = 150,
    height = 30,
    margin=[5,5,5,30],
    disabled= True,)
button_save_img = Button(label = "Save Plot",
    width = 150,
    height = 30,
    margin=[5,5,5,30],
    disabled= True,)
button_calculate.on_click(BWC)
button_save_data.on_click(save_data)
button_save_img.on_click(save_img)

buttons = row(button_calculate,button_save_data, button_save_img, margin=[30,5,5,180])



# show result
curdoc().add_root(column(top,main,buttons))



# bokeh serve --show My_GUI.py
# http://localhost:5006/My_GUI