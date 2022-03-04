# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 15:05:16 2022

@author: yge001
"""


from bokeh.models import CustomJS, TextInput
from bokeh.io import output_file, show, curdoc
from bokeh.plotting import figure
from bokeh.layouts import widgetbox, row, column
from bokeh.models.widgets import Slider, Div, Button, RadioButtonGroup
import pandas as pd
import numpy as np
import os, sys
import sugawara
os.chdir(sys.path[0])

# GUI for Back Water Curve and Sugawara Model
model_option = RadioButtonGroup(labels=["Back Water Curve", "Sugawara Tank Model"], active=1)

State = Div(text="<b>Sugawara Tank Model : System states</b>")     # bold 
s_s1 = Slider(start=1.0, end=20.0, value=10.0, step=0.5, title="Select S1")
s_s2 = Slider(start=1.0, end=15.0, value=8.0, step=0.5, title="Select S2")

parameter = Div(text="<b>Sugawara Tank Model : Parameter vector</b>") 
s_d1 = Slider(start=1.0, end=15.0, value=10.0, step=0.5, title="Select d1")
s_d2 = Slider(start=0.1, end=1.0, value=0.2, step=0.1, title="Select d2")
s_k1 = Slider(start=0.0, end=1.1, value=0.5, step=0.1, title="Select k1")
s_k2 = Slider(start=0.0, end=1.1, value=0.2, step=0.1, title="Select k2")
s_k3 = Slider(start=0.0, end=1.5, value=0.01, step=0.01, title="Select k3")
s_k4 = Slider(start=0.0, end=1.1, value=0.1, step=0.1, title="Select k4")
EP = Div(text="<b>Sugawara Tank Model : Extra Parameters</b>") 
dt = TextInput(value="30", title="Number of hours in the time step [s]:")
area = TextInput(value="100", title="Catchment area [km²]:")
sugwara_graph = figure(plot_width=600, plot_height=300)

graph= Div(text="""<img src="sugawara.png">""", width=50, height=50,)



button_OK = Button(label="OK", button_type="danger",visible = True)

def sugwara_click():
 
    sugwara_graph.renderers=[]
    skip_rows = 16  # Initial Number of text rows to skip
    output_file = 'output.asc' # For getting data from the output file in current folder
    
    # Read data from the output file
    data = pd.read_csv(output_file,
                        skiprows=skip_rows,
                        skipinitialspace=True,
                        index_col='Time')
    
    # Create vector with time steps
    time_index = pd.date_range('1994 12 07 20:00', periods=len(data), freq='H')
    
    # Add time steps to observations
    data.set_index(time_index, inplace=True)
        
    
    # read the parameters from sliders 
    
    
    k1=  float(s_k1.value)
    k2=  float(s_k2.value)
    k3=  float(s_k3.value)
    k4=  float(s_k4.value)
    d1=  float(s_d1.value)
    d2=  float(s_d2.value)
    s1=  float(s_s1.value)
    s2=  float(s_s2.value)

            
    extra_pars = [float(dt.value), float(area.value)]
    pars = [k1,k2,k3,k4,d1,d2,s1,s2] # Setting intial parameter set
    prec = np.array(data['Rainfall']) + np.array(data['Snowfall']) # Precipitation input as sum of Rainfall and Snowfall
    evap = np.array(data['ActualET'])  # The Actual Evapotranspiration

    

    q_simu, st_simu = sugawara.simulate(prec=prec[:-1], evap=evap[:-1], param=pars, extra_param=extra_pars)  # Running the model
    
    # plotting the results
    sugwara_graph.xaxis.axis_label = 'Time [hrs]'   
    sugwara_graph.yaxis.axis_label = 'Runoff [m³/s]' 
    
    x= np.linspace(0,1000,1000)
    sugwara_graph.line(x,q_simu,legend_label="Model Runoff ")
    sugwara_graph.line(x,np.array(data['Qrec']), color='red',legend_label="Observed Runoff ")

    button_OK.button_type="success"
    




button_OK.on_click(sugwara_click)

#show(row(column(parameter, s_d1, s_d2, s_k1, s_k2, s_k3,s_k4, State, s_s1, s_s2,EP,dt, area, button_OK, height=80),column(graph, sugwara_graph)))
curdoc().add_root(row(column(model_option, parameter, s_d1, s_d2, s_k1, s_k2, s_k3,s_k4, State, s_s1, s_s2,EP,dt, area, button_OK, height=80),column(graph, sugwara_graph)))
