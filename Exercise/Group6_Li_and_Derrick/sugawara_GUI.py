# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 20:18:37 2022

@author: qli003
"""
from __future__ import division
from cProfile import label
from bokeh.layouts import row,column
from bokeh.models import Div, TextInput,Button, FileInput, Slider
from bokeh.io import output_file, show
from bokeh.plotting import figure, show,curdoc
import numpy as np
import scipy.optimize as opt
import pandas as pd
import os, sys
os.chdir(sys.path[0])
# output_file("my_GUI.html")




# set up textarea (div)
top = Div(
    text="""
          <h1 style="width:800px; height:40px;text-align:center;border-style:solid;position:relative;left:200px">Sugawara</h3>
          """,
    width = 1200,
    height = 60,
)
subtitle1 = Div(
    text="""
          <p>Input</p>
          """,
    width=200,
    height=30,
    margin = [0,0,0,15],
)

# set up textarea (div)
prec_textarea = Div(
    text="""
          <p>Precipitation [mm]:</p>
          """,
    width=250,
    height=30,
    margin = [0,0,0,30],
)
prec_file_input = FileInput(
    accept = '.xlsx',
    filename = 'prec.xlsx',
    width = 200,
    height = 30,
)
prec = row(prec_textarea,prec_file_input)



# set up textarea (div)
evap_textarea = Div(
    text="""
          <p>Evaporation [mm]:</p>
          """,
    width=250,
    height=30,
    margin = [0,0,0,30],
)
evap_file_input = FileInput(
    accept = '.xlsx',
    filename = 'evap.xlsx',
    width = 150,
    height = 30,
)
evap = row(evap_textarea,evap_file_input)



# set up textarea (div)
S1_textarea = Div(
    text="""
          <p>Initial level of the top tank [mm]:</p>
          """,
    width=250,
    height=30,
    margin = [0,0,0,30],
)
S1_text_input = TextInput(
    value = '10',
    width = 100,
    height = 30
)
S1 = row(S1_textarea,S1_text_input)

# set up textarea (div)
S2_textarea = Div(
    text="""
          <p>Initial level of the bottom tank [mm]:</p>
          """,
    width=250,
    height=30,
    margin = [0,0,0,30],
)
S2_text_input = TextInput(
    value = '10',
    width = 100,
    height = 30
)
S2 = row(S2_textarea,S2_text_input)

# set up textarea (div)
k1_textarea = Div(
    text="""
          <p>Upper tank upper discharge coefficient:</p>
          """,
    width=250,
    height=30,
    margin = [0,0,0,30],
)
k1_slider_input = Slider(start = 0, end = 1, value = 0.1819, step = 0.0001, width = 200)
k1 = row(k1_textarea,k1_slider_input)

# set up textarea (div)
k2_textarea = Div(
    text="""
          <p>Upper tank lower discharge coefficient:</p>
          """,
    width=250,
    height=30,
    margin = [0,0,0,30],
)

k2_slider_input = Slider(start = 0, end = 1, value = 0.0412, step = 0.0001, width = 200)
k2 = row(k2_textarea,k2_slider_input)

# set up textarea (div)
k3_textarea = Div(
    text="""
          <p>Percolation to lower tank coefficient:</p>
          """,
    width=250,
    height=30,
    margin = [0,0,0,30],
)
k3_slider_input = Slider(start = 0, end = 1, value = 0.3348, step = 0.0001, width = 200)
k3 = row(k3_textarea,k3_slider_input)

# set up textarea (div)
k4_textarea = Div(
    text="""
          <p>Lower tank discharge coefficient:</p>
          """,
    width=250,
    height=30,
    margin = [0,0,0,30],
)

k4_slider_input = Slider(start = 0, end = 1, value = 0.0448, step = 0.0001, width = 200)

k4 = row(k4_textarea,k4_slider_input)

# set up textarea (div)
d1_textarea = Div(
    text="""
          <p>Upper tank upper discharge position:</p>
          """,
    width=250,
    height=30,
    margin = [0,0,0,30],
)

d1_slider_input = Slider(start = 1, end = 10, value = 3.2259, step = 0.001, width = 200)
d1 = row(d1_textarea, d1_slider_input)


# set up textarea (div)
d2_textarea = Div(
    text="""
          <p>Upper tank lower discharge position:</p>
          """,
    width=250,
    height=30,
    margin = [0,0,0,30],
)

d2_slider_input = Slider(start = 0, end = 1, value = 0.38, step = 0.01, width = 200)

d2 = row(d2_textarea, d2_slider_input)

# set up textarea (div)
dt_textarea = Div(
    text="""
          <p>Number of hours in the time step [s]:</p>
          """,
    width=250,
    height=30,
    margin = [0,0,0,30],
)
# dt_text_input = TextInput(
#     value = '1',
#     width = 100,
#     height = 30
# )
dt_slider_input = Slider(start = 1, end = 24, value = 1, step = 1, width = 200)
dt = row(dt_textarea, dt_slider_input)

# set up textarea (div)
area_textarea = Div(
    text="""
          <p>Catchment area [km²]:</p>
          """,
    width=250,
    height=30,
    margin = [0,0,0,30],
)
area_text_input = TextInput(
    value = '145',
    width = 100,
    height = 30
)


area = row(area_textarea,area_text_input)

input = column(subtitle1,prec,evap,S1,S2,k1,k2,k3,k4,d1,d2,dt,area)





#######################################################################################
# Calculate Sugawara
#######################################################################################
INITIAL_STATES = [10, 10]
INITIAL_Q = 1.0
INITIAL_PARAM = [0.5, 0.2, 0.01, 0.1, 10.0, 20.0, 1, 1]
#INITIAL_PARAM = [0.1819, 0.0412, 0.3348, 0.0448, 3.2259, 0.3800]

PARAM_BND = ((0.0, 1.1),
             (0.0, 1.1),
             (0.0, 1.5),
             (0.0, 1.1),
             (1.0, 15.0),
             (0.1, 1.0),
             (0.8, 1.2),
			 (0.8, 1.2))


def _step(prec, evap, st, param, extra_param):
    '''
    #this function takes the following arguments
    #I -> inputs(2)[prec, evap]
    #    I(1) prec: Precipitation [mm]
    #    I(2) evap: Evaporation [mm]
    #
    #S -> System states(2)[S1, S2]
    #    S(1) S1: Level of the top tank [mm]
    #    S(2) S2: Level of the bottom tank [mm]
    #
    #P -> Parameter vector(6)
    #    P(1) k1: Upper tank upper discharge coefficient
    #    P(2) k2: Upper tank lower discharge coefficient
    #    P(3) k3: Percolation to lower tank coefficient
    #    P(4) k4: Lower tank discharge coefficient
    #    P(5) d1: Upper tank upper discharge position
    #    P(6) d2: Upper tank lower discharge position
    #
    #EP -> Extra parameters(2)
    #    EP(1) DT: Number of hours in the time step [s]
    #    EP(2) AREA: Catchment area [km²]
    #
    #Outputs
    #Q -> Flow [m³/s]
    #S -> Updated system states(2)[S1, S2] mm
    '''

    # Old states
    S1Old = st[0]
    S2Old = st[1]

    #Parameters
    k1 = param[0]
    k2 = param[1]
    k3 = param[2]
    k4 = param[3]
    d1 = param[4]
    d2 = param[5]
    rfcf = param[6]
    ecorr = param[7]
    
    # Extra Parameters
    DT = extra_param[0]
    Area = extra_param[1]

    ## Top tank
    H1 = np.max([S1Old + prec*rfcf - evap*ecorr, 0])

    if H1 > 0:
        #direct runoff
        if H1 > d1:
            q1 = k1*(H1-d1)
        else:
            q1 = 0

        #Fast response component
        if H1 > d2:
            q2 = k2*(H1-d2)
        else:
            q2 = 0

        #Percolation to bottom tank
        q3 = k3 * H1
        #Check for availability of water in upper tank
        q123 = q1+q2+q3
        if q123 > H1:
            q1 = (q1/q123)*H1
            q2 = (q2/q123)*H1
            q3 = (q3/q123)*H1
    else:
        q1 = 0
        q2 = 0
        q3 = 0

    Q1 = q1+q2
    #State update top tank
    S1New = max(H1 - (q1+q2+q3), 0.0)
    
    ## Bottom tank
    H2 = S2Old+q3
    Q2 = k4* H2

    #check if there is enough water
    if Q2 > H2:
        Q2 = H2

    #Bottom tank update
    S2New = H2 - Q2

    ## Total Flow
    # DT = 86400 #number of seconds in a day
    # Area = 2100# Area km²
    if (Q1 + Q2) >= 0:
        Q = (Q1+Q2)*Area/(3.6*DT)
    else:
        Q = 0

    S = [S1New, S2New]
#    if S1New < 0:
#        print('s1 below zero')
    return Q, S

def simulate(prec, evap, param, extra_param):
    '''

    '''
    st = [INITIAL_STATES,]
    q = [10,]

    for i in range(len(prec)):
        step_res = _step(prec[i], evap[i], st[i], param, extra_param)
        q.append(step_res[0])
        st.append(step_res[1])
        
    return q, st

def calibrate(prec, evap, extra_param, q_rec, verbose=False):

    def mod_wrap(param_cal):
        q_sim = simulate(prec[:-1], evap[:-1], param_cal, extra_param)[0]
        try:
            perf_fun = -NSE(q_sim, q_rec)
        except:
            perf_fun = 9999

        if verbose: print -perf_fun
        return perf_fun

    cal_res = opt.minimize(mod_wrap, INITIAL_PARAM, bounds=PARAM_BND,
                           method='L-BFGS-B')

    return cal_res.x, cal_res.fun

def NSE(x,y,q='def',j=2.0):
    """
    Performance Functions
    x - calculated value
    y - recorded value
    q - Quality tag (0-1)
    j - exponent to modify the inflation of the variance (standard NSE j=2)
    """
    x = np.array(x)
    y = np.array(y)
    a = np.sum(np.power(x-y,j))
    b = np.sum(np.power(y-np.average(y),j))
    F = 1.0 - a/b
    return F


'''
callback  
'''
p = figure( x_axis_label='Time', y_axis_label='Discharge',width = 800, height = 480)
def calculate_discharge():
    global x
    global Q_arr
    p.renderers = []
    print('on_click: run')
    print(prec_file_input.filename)
    df_prec = pd.read_excel('Exercise/Group6_Li_and_Derrick/'+prec_file_input.filename)
    print(evap_file_input.filename)
    df_evap = pd.read_excel('Exercise/Group6_Li_and_Derrick/'+evap_file_input.filename)
    
    st = [float(S1_text_input.value),float(S2_text_input.value)]
    print(f'st: {st}')
    param = [float(k1_slider_input.value), float(k2_slider_input.value), float(k3_slider_input.value), float(k4_slider_input.value), float(d1_slider_input.value), float(d2_slider_input.value),1,1]
    print(f'param:{param}')
    extra_param = [float(dt_slider_input.value), float(area_text_input.value)]
    print(f'extra_param:{extra_param}')
    Q_arr = np.zeros(len(df_prec))
    for i in range(len(df_prec)):
        Q,st = _step(df_prec.loc[i,'prec'], df_evap.loc[i,'evap'], st, param, extra_param)
        Q_arr[i] = Q
    x = np.arange(0,len(df_prec)*int(dt_slider_input.value),int(dt_slider_input.value))
    p.line(x,Q_arr,legend_label = 'slope of bed level', line_width = 2)
    print('Done.')
    button_save.disabled = False
def save_res():
    print('Save Results....')
    np.savetxt('Exercise/Group6_Li_and_Derrick/sugawara_res.txt',np.array([x,Q_arr]).T)
    print('Done.')
#######################################################################################

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

button_calculate = Button(label="Calculate and Display",
    width = 150,
    height = 30,
    margin=[5,5,5,5]
)

button_save = Button(label="Save Results",
    width = 150,
    height = 30,
    disabled = True,
    margin=[5,5,5,50]
)

buttons = row(button_calculate,button_save,margin=[30,5,5,450])

button_calculate.on_click(calculate_discharge)
button_save.on_click(save_res)
# show result
curdoc().add_root(column(top,main,buttons))



# bokeh serve --show sugawara_GUI.py
# http://localhost:5006/sugawara_GUI