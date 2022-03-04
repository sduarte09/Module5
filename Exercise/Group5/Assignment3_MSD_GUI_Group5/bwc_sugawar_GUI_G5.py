# Import required libraries

from bokeh.models import Div
from bokeh.models import FileInput, TextInput, CustomJS
from bokeh.layouts import widgetbox, row, column
from bokeh.models.widgets import RadioButtonGroup
from bokeh.models.widgets import Slider, Div, Button
from bokeh.layouts import column, row
from bokeh.plotting import curdoc, figure, show
from bokeh.io import output_file, show, curdoc
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Slider, Div, Button
import pandas as pd
import numpy as np
import os, sys
import sugawara
os.chdir(sys.path[0])


# GUI for Back Water Curve and Sugawara Model
model_option = RadioButtonGroup(labels=["Back Water Curve", "Sugawara Tank Model"], active=0)


# GUI for Input and output for Back Water Curve (BWC) Model
################################################################################################################################
# output_file("BWC.html")
div1 = Div(text="""<h3> <b> Back Water Curve (BWC) </b></h3> """)

div2 = Div(text=""" <b> INPUT </b> """,
width=200, height=50)

div3 = Div(text=""" Want to open already saved project as input file? """,
width=200, height=70)

div4 = Div(text=""" <b> OUTPUT </b> """,
width=200, height=50)

div5 = Div(text=""" """,
width=200, height=50)

file_input = FileInput()
file_input.disabled = True

button1 = Button(label="Geometry Parameters", button_type="danger")
button2 = Button(label="Physical and Hydro Parameters", button_type="danger")
button3 = Button(label="Calculate / Show Results", button_type="success")
button4 = Button(label="Save Input Data", button_type="danger")
button5 = Button(label="Save Graph", button_type="danger")
button6 = Button(label="OK", button_type="primary",visible = False)
button7 = Button(label="OK", button_type="primary",visible = False)
button4.disabled = True 
button5.disabled = True 


scheme_option = RadioButtonGroup(labels=["Explicit Scheme", "Implicit Scheme"], active=0)

#show(row(column(div1, div2, button1, button2), column(div5, div3, file_input, button_group), column(div5, div4, button3, button4, button5)))

# output_file("Input.html")

# Geometry Input Parameters
div6 = Div(text=""" <b> Geometry Parameters </b> """,visible = False)
length = TextInput(value="5000", title="Length of Rectangular Channel (m) = L : ",visible = False)
width = TextInput(value="60", title="Width of Rectangular Channel (m) = B : ",visible = False)

# Physical & Hydro Input Parameters
div7 = Div(text=""" <b> Physical & Hydro Parameters </b> """,visible = False)
slope = TextInput(value="0.001", title="Channel Bed Slope = S0 : ",visible = False)
discharge = TextInput(value="100", title="Flow rate or Discharge in channel (m^3/s) = Q : ",visible = False)
C_text = TextInput(value="50", title="Chezy's Roughness Coefficient (m^(1/2)/s) = C : ",visible = False)
Hd_text = TextInput(value="2", title="Water depth at downstream (or lake) (m) = Hd : ",visible = False)
dx_text = TextInput(value="100", title="Space Interval (m) = dx : ",visible = False)
error_text = TextInput(value="0.01", title="Permissble convergence error for Implicit method : ",visible = False)
iter_text = TextInput(value="19", title="Maximum number of iteration for Implicit method : ",visible = False)

#show(row(column(div7, slope, discharge, C_text, Hd_text, dx_text, button6), column(div6, length, width, button7)))


# Initializing variables using Boundary Conditions

# Euler Numerical Scheme Solution (Explicit method)

graph = figure(width=1000, height=500, title="Backwater Curve (dx={0} m)".format(int(dx_text.value)), x_axis_label = "Distance (m)", y_axis_label = "Level (m)", visible = False)

def Explicit(): 
    graph.renderers=[]
    g = 9.81
    x = [0.0]
    hd = float(Hd_text.value)
    gl = [0.0]
    wl = [Hd_text.value]
    h = [hd]                                   # Initial Water depth at downstream end in meters
    b = float(width.value)                     # Breadth of the rectangular open flow channel in meters
    Q = float(discharge.value)                 # Flow rate or discharge in m^3/s
    C = float(C_text.value)                    # Chezy's coefficient in m^(1/2)/s
    S0 = float(slope.value)                    # bed slope of channel
    X = float(length.value)                    # Total distance or length of channel for which calculation is required, in meters
    dx = float(dx_text.value)                  # space step interval or space step
    max_range =int(X/dx)+1
    h_critical = ((Q/b)**2/g)**(1/3)
    h_cr = [h_critical]
    for i in range(1,max_range):
        x.append(i*dx)
        gl.append(i*dx*S0)
        h.append(h[i-1]+dx*(Q*Q/(C*C*h[i-1]**3*b*b)-S0))
        wl.append(gl[i]+h[i])
        h_cr.append(gl[i]+h_critical) 
    # Plotting results
    graph.varea(x=x, y1=gl, y2=wl, fill_color='#89c8ff')
    graph.line(x, wl, line_color = "blue", line_dash = "solid", legend_label = "Water Level (Explicit Solution")
    graph.line(x, h_cr, line_color = "red", line_dash = "dashed", legend_label = "Critical Depth of Channel")
    graph.line(x, gl, line_color = "black", line_dash = "solid", legend_label = "Bed Level of Channel")
    graph.legend.location = 'bottom_right'
    graph.visible = True
    graph.title.text="Backwater Curve (dx={0} m)".format(int(dx))
    graph.title.text_font_size = '16pt'



def Implicit():  
    graph.renderers=[]
    g = 9.81
    x = [0.0]
    hd = float(Hd_text.value)
    gl = [0.0]
    wl = [Hd_text.value]
    h = [hd]                                   # Initial Water depth at downstream end in meters
    b = float(width.value)                     # Breadth of the rectangular open flow channel in meters
    Q = float(discharge.value)                 # Flow rate or discharge in m^3/s
    C = float(C_text.value)                    # Chezy's coefficient in m^(1/2)/s
    S0 = float(slope.value)                    # bed slope of channel
    X = float(length.value)                    # Total distance or length of channel for which calculation is required, in meters
    dx = float(dx_text.value)                  # space step interval or space step
    Converge_error = float(error_text.value)         # Permissble convergence error for Implicit method in meters
    n_iter = int(iter_text.value)                  # Maximum number of iteration for Implicit method
    max_range =int(X/dx)+1
    h_critical = ((Q/b)**2/g)**(1/3)
    h_cr = [h_critical]
    K = Q**2/(C**2*b**2)

    for i in range(1,max_range):
        n = 0
        abs_error = 10.0
        h_left = h[i-1]
        x.append(i*dx)
        gl.append(i*dx*S0)
        while abs_error > Converge_error:
            h_right = h[i-1]+(dx*(K/(h_left**3)-S0))
            abs_error = abs(h_left-h_right)
            h_left = h_right
            n = n + 1
            if n > n_iter:
                break
        h.append(h_right)
        wl.append(gl[i]+h[i])
        h_cr.append(gl[i]+h_critical)
    
    # Plotting results
    graph.varea(x=x, y1=gl, y2=wl, fill_color='#89c8ff')
    graph.line(x, wl, line_color = "blue", line_dash = "solid", legend_label = "Water Level (Explicit Solution")
    graph.line(x, h_cr, line_color = "red", line_dash = "dashed", legend_label = "Critical Depth of Channel")
    graph.line(x, gl, line_color = "black", line_dash = "solid", legend_label = "Bed Level of Channel")
    graph.legend.location = 'bottom_right'
    graph.visible = True
    graph.title.text="Backwater Curve (dx={0} m)".format(int(dx))
    graph.title.text_font_size = '16pt'


# Defining different functions for different click events

def option_select(active):
    ch = active
    if ch == 0:
        model_option.visible = True
        div1.visible = True
        div2.visible = True
        button1.visible = True
        button2.visible = True
        div5.visible = True
        div3.visible = True
        file_input.visible = True
        scheme_option.visible = True
        div5.visible = True
        div4.visible = True
        button3.visible = True
        button4.visible = True
        button5.visible = True
        graph.visible = False

        parameter.visible = False
        s_d1.visible = False
        s_d2.visible = False
        s_k1.visible = False
        s_k2.visible = False
        s_k3.visible = False
        s_k4.visible = False
        State.visible = False
        s_s1.visible = False
        s_s2.visible = False
        EP.visible = False
        dt.visible = False
        area.visible = False
        button_OK.visible = False

    elif ch == 1:
        model_option.visible = True
        div1.visible = False
        div2.visible = False
        button1.visible = False
        button2.visible = False
        div5.visible = False
        div3.visible = False
        file_input.visible = False
        scheme_option.visible = False
        div5.visible = False
        div4.visible = False
        button3.visible = False
        button4.visible = False
        button5.visible = False
        graph.visible = False

        parameter.visible = True
        s_d1.visible = True
        s_d2.visible = True
        s_k1.visible = True
        s_k2.visible = True
        s_k3.visible = True
        s_k4.visible = True
        State.visible = True
        s_s1.visible = True
        s_s2.visible = True
        EP.visible = True
        dt.visible = True
        area.visible = True
        button_OK.visible = True


def Geometry():
    div7.visible = True
    slope.visible = True
    discharge.visible = True
    C_text.visible = True
    Hd_text.visible = True
    dx_text.visible = True
    button6.visible = True
    graph.visible = False
    if model_option.active==0 and scheme_option.active==1:
        error_text.visible = True
        iter_text.visible = True


def Geometry_OK():
    div7.visible = False
    slope.visible = False
    discharge.visible = False
    C_text.visible = False
    Hd_text.visible = False
    dx_text.visible = False
    button6.visible = False
    error_text.visible = False
    iter_text.visible = False
    button1.button_type= "success"
    

def Hydro():
    div6.visible = True
    length.visible = True
    width.visible = True
    button7.visible = True
    graph.visible = False

def Hydro_OK():
    div6.visible = False
    length.visible = False
    width.visible = False
    button7.visible = False
    button2.button_type= "success"

def Result_BWC():
    if model_option.active==0 and scheme_option.active==0:
        Explicit()
    elif model_option.active==0 and scheme_option.active==1:
        Implicit()



# Defining click events

button3.on_click(Result_BWC)
button1.on_click(Geometry)
button2.on_click(Hydro)
button6.on_click(Geometry_OK)
button7.on_click(Hydro_OK)
model_option.on_click(option_select)


# Main and Back Water Curve GUI 
curdoc().add_root(row(column(model_option, div1, div2, button1, button2), column(div5, div3, file_input, scheme_option), column(div5, div4, button3, button4, button5)))
curdoc().add_root(row(column(div7, slope, discharge, C_text, Hd_text, dx_text, error_text, iter_text, button6)))
curdoc().add_root(row(column(div6, length, width, button7)))
curdoc().add_root(row(graph))




# GUI for Input and output for Sugawara Model
################################################################################################################################

State = Div(text="<b>Sugawara Tank Model : System states</b>", visible = False)     # bold 
s_s1 = Slider(start=1.0, end=20.0, value=10.0, step=0.5, title="Select S1", visible = False)
s_s2 = Slider(start=1.0, end=15.0, value=8.0, step=0.5, title="Select S2", visible = False)

parameter = Div(text="<b>Sugawara Tank Model : Parameter vector</b>", visible = False) 
s_d1 = Slider(start=1.0, end=15.0, value=10.0, step=0.5, title="Select d1", visible = False)
s_d2 = Slider(start=0.1, end=1.0, value=0.2, step=0.1, title="Select d2", visible = False)
s_k1 = Slider(start=0.0, end=1.1, value=0.5, step=0.1, title="Select k1", visible = False)
s_k2 = Slider(start=0.0, end=1.1, value=0.2, step=0.1, title="Select k2", visible = False)
s_k3 = Slider(start=0.0, end=1.5, value=0.01, step=0.01, title="Select k3", visible = False)
s_k4 = Slider(start=0.0, end=1.1, value=0.1, step=0.1, title="Select k4", visible = False)
EP = Div(text="<b>Sugawara Tank Model : Extra Parameters</b>", visible = False) 
dt = TextInput(value="30", title="Number of hours in the time step [s]:", visible = False)
area = TextInput(value="100", title="Catchment area [km²]:", visible = False)
sugwara_graph = figure(plot_width=600, plot_height=300, visible = False)

graph= Div(text="""<img src="sugawara.png">""", width=50, height=50, visible = False)



button_OK = Button(label="OK", button_type="danger",visible = False)

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



# Main and Sugawara Model GUI 
curdoc().add_root(row(column(parameter, s_d1, s_d2, s_k1, s_k2, s_k3,s_k4, State, s_s1, s_s2,EP,dt, area, button_OK, height=80),column(graph, sugwara_graph)))


