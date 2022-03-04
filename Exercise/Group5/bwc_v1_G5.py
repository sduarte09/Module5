# Import required libraries

from bokeh.models import Div
from bokeh.models import FileInput, TextInput
from bokeh.layouts import widgetbox
from bokeh.models.widgets import RadioButtonGroup
from bokeh.models.widgets import Button
from bokeh.layouts import column, row
from bokeh.plotting import curdoc, figure, show
import numpy as np



# GUI for Input and output

# output_file("BWC.html")
div1 = Div(text="""<h2> <b> Back Water Curve (BWC) </b></h2> """)

div2 = Div(text=""" <b> INPUT </b> """,
width=200, height=50)

div3 = Div(text=""" Want to open already saved project as input file? """,
width=200, height=70)

div4 = Div(text=""" <b> OUTPUT </b> """,
width=200, height=50)

div5 = Div(text=""" """,
width=200, height=50)

file_input = FileInput()


button1 = Button(label="Geometry Parameters", button_type="danger")
button2 = Button(label="Physical and Hydro Parameters", button_type="danger")
button3 = Button(label="Calculate / Show Results", button_type="success")
button4 = Button(label="Save Input Data", button_type="primary")
button5 = Button(label="Save Graph", button_type="success")
button6 = Button(label="OK", button_type="primary",visible = False)
button7 = Button(label="OK", button_type="primary",visible = False)


button_group = RadioButtonGroup(labels=["Explicit Scheme", "Implicit Scheme"], active=0)

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
error_text = TextInput(value="0.01", title="Permissble convergence error for Implicit method (m) = Converge_error : ",visible = False)
iter_text = TextInput(value="19", title="Maximum number of iteration for Implicit method = n_iter : ",visible = False)

#show(row(column(div7, slope, discharge, C_text, Hd_text, dx_text, button6), column(div6, length, width, button7)))


# Initializing variables using Boundary Conditions

# Euler Numerical Scheme Solution (Explicit method)

graph = figure(width=1000, height=500, title="Backwater Curve (dx={0} m)".format(dx_text.value), x_axis_label = "Distance (m)", y_axis_label = "Level (m)", visible = False)

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
    graph.line(x, wl, line_color = "blue", line_dash = "solid", legend_label = "Water Level (Explicit Solution")
    graph.line(x, h_cr, line_color = "red", line_dash = "dashed", legend_label = "Critical Depth of Channel")
    #graph.varea(x=x, y1=gl, y2=wl, fill_color='#89c8ff')
    graph.line(x, gl, line_color = "black", line_dash = "solid", legend_label = "Bed Level of Channel")
    graph.legend.location = 'bottom_right'
    graph.visible = True

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
        abs_error = 1.0
        h_left = h[i-1]
        x.append(i*dx)
        gl.append(i*dx*S0)
        while abs_error > Converge_error:
            h_right = h[i-1]+(dx*K/(h_left**3)-S0)
            abs_error = abs(h_left-h_right)
            h_right = h_left
            n = n + 1
            if n > n_iter:
                break
        h.append()
        wl.append(gl[i]+h[i])
        h_cr.append(gl[i]+h_critical)
    
    # Plotting results
    graph.line(x, wl, line_color = "blue", line_dash = "solid", legend_label = "Water Level (Explicit Solution")
    graph.line(x, h_cr, line_color = "red", line_dash = "dashed", legend_label = "Critical Depth of Channel")
    graph.line(x, gl, line_color = "black", line_dash = "solid", legend_label = "Bed Level of Channel")
    #graph.varea(x=x, y1=gl, y2=wl, fill_color='#89c8ff')
    graph.legend.location = 'bottom_right'
    graph.visible = True

# Defining different functions for different click events
def Geometry():
    div7.visible = True
    slope.visible = True
    discharge.visible = True
    C_text.visible = True
    Hd_text.visible = True
    dx_text.visible = True
    button6.visible = True
    graph.visible = False

def Geometry_OK():
    div7.visible = False
    slope.visible = False
    discharge.visible = False
    C_text.visible = False
    Hd_text.visible = False
    dx_text.visible = False
    button6.visible = False
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


# Defining click events

button3.on_click(Explicit)
button1.on_click(Geometry)
button2.on_click(Hydro)
button6.on_click(Geometry_OK)
button7.on_click(Hydro_OK)

curdoc().add_root(row(column(div1, div2, button1, button2), column(div5, div3, file_input, button_group), column(div5, div4, button3, button4, button5)))
curdoc().add_root(row(column(div7, slope, discharge, C_text, Hd_text, dx_text, button6)))
curdoc().add_root(row(column(div6, length, width, button7)))
curdoc().add_root(row(graph))


