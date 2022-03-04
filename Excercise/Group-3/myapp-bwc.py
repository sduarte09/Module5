from turtle import width
import numpy as np
from bokeh.io import output_file, show
from bokeh.layouts import widgetbox, Row, Column
from bokeh.models.widgets import Button, RadioButtonGroup, Select, Slider, Div, PreText
from bokeh.models import CustomJS, TextInput, Slider, Button, VArea
from bokeh.plotting import curdoc, figure
from sqlalchemy import column, false

#######################################################################################################################
################## Front End ########################

output_file("Hydrological_Models.html")
# create some widgets

Title_0 = Div(text="<b>Backwater Curve Calculator</b>")

model_type = RadioButtonGroup(labels=["Backwater Curve", "Sugawara Model"], active = 0)

#######################################################################################################################

Title_1  = Div(text="<b>Channel Geometry")
C_Length = TextInput(value="20000", title="Channel Length (m)")
C_Length.js_on_change("value", CustomJS(code="""console.log('C_Length: value=' + this.value, this.toString())"""))

C_Width = TextInput(value="60", title="Channel Width (m)")
C_Width.js_on_change("value", CustomJS(code="""console.log('C_Width: value=' + this.value, this.toString())"""))

H_Res = TextInput(value="8", title="Height at Reservoir Mouth (m)")
H_Res.js_on_change("value", CustomJS(code="""console.log('H_Res: value=' + this.value, this.toString())"""))

slope = TextInput(value="0.001", title="Slope (-)")
slope.js_on_change("value", CustomJS(code="""console.log('H_Res: value=' + this.value, this.toString())"""))

#######################################################################################################################

Title_2  = Div(text="<b>Hydraulic Parameters")
R_value  = TextInput(title="Chezy Coefficient Value:", value="50")

Disch = TextInput(value="50", title="Discharge (m^3/s)")
Disch.js_on_change("value", CustomJS(code="""
    console.log('Disch: value=' + this.value, this.toString())"""))

#######################################################################################################################

Title_3 = Div(text="<b>Numerical Parameters")
d_x = Slider(start=0, end=1000, value=150, step=1, title="Delta X (m)")
itterslider = Slider(start=0, end=100, value=10, step=1, title="No. of Iterations", visible = False)

#######################################################################################################################

Title_4 = Div(text="<b>Solution Type")
scheme_type = RadioButtonGroup(labels=["Explicit", "Implicit"], active=0)
run_e  = Button(label="Run Explicit Model", button_type="success", visible = True)
run_i  = Button(label="Run Implicit Model", button_type="success", visible = False)
table  = Button(label="Export Tables", button_type="primary", visible = False)
p1 = figure(plot_width=1350, plot_height=780, title= "Back Water Curve", x_axis_label= 'Length (m)', y_axis_label='Water Level (m)')

#######################################################################################################################
  
################## Back End ########################

def explicit():
    # Initial Variables
    b = float(C_Width.value)        #River Width (m)
    X =  float(C_Length.value)       #Total Length
    hd = float(H_Res.value)          #Water Depth at Downstream end (m)
    S0 = float(slope.value)          #Slope
    C = float(R_value.value)         #Chezy Coefficient(m^1/2/s)
    Q = float(Disch.value)           #Discharge (m^3/s)
    dx = float(d_x.value)            #Step Size(m)
    itter = float(itterslider.value) #Iteration for Implicit

    x_ticks = 500

    # Initialising variables using Initial Condition for Explicit Solution
    steps_e = int(X/dx) + 1
    x_e  = [0]
    hg_e = [0]
    h_e  = [hd]
    wl_e  = [hd]
    y0 = [0]

    # Explicit/ Euler Numerical Scheme Solution
    for i in range(1, steps_e):
        x_e.append(i*dx)
        hg_e.append(i*dx*S0)
        h_e.append(h_e[i-1] + dx * ((Q*Q) / (C*C*(h_e[i-1]**3)*b*b)-S0))
        wl_e.append(hg_e[i]+h_e[i])
        
    p1.renderers = []
    p1.varea(x=x_e, y1=wl_e, y2=hg_e, fill_color="lightblue")
    p1.varea(x=x_e, y1=hg_e, y2=0, fill_color="lightyellow")
    p1.line(x_e, wl_e, line_width=2, line_color='navy', legend_label= "Water Level (m)")        #, 'b', label = " Water Level (Implicit)")
    p1.line(x_e, hg_e,line_width=2, line_color='brown', legend_label= "Geodetic Height (m)")         #, 'brown', label = " Geodetic Height (Implicit)")
    p1.legend.location = "top_left"

def implicit():
        # Initial Variables
    b = float(C_Width.value)        #River Width (m)
    X =  float(C_Length.value)       #Total Length
    hd = float(H_Res.value)          #Water Depth at Downstream end (m)
    S0 = float(slope.value)          #Slope
    C = float(R_value.value)         #Chezy Coefficient(m^1/2/s)
    Q = float(Disch.value)           #Discharge (m^3/s)
    dx = float(d_x.value)            #Step Size(m)
    itter = float(itterslider.value) #Iteration for Implicit
    # Initial Variables
    
    A = Q**2/(C**2*b**2) # Calculation simplification
     
    # Initialising variables using Initial Condition
    maxcomp = int(X/dx)
    x_i = [0]
    h_i = [hd]
    hg_i = [0]
    wl_i = [hd]

    # Numerical Scheme Solution
   
    # Implicit
    for i in range(1,maxcomp):
        # first assumption for iteration
        htriR = h_i[i-1] #m
        x_i.append(i*dx)
        # Bed level
        hg_i.append(S0*i*dx)
        j = 0
        # Water depth
        error = 10
        
        while error > 0.01:
            if j > itter:
                break
            else:
                RHS = A/htriR**3-S0
                htril = dx*RHS+h_i[i-1]
                error = abs(htril-htriR)
                htriR = htril
                j += 1
        h_i.append(htril)
        # Water level
        wl_i.append(h_i[i] + hg_i[i])

    p1.renderers = []
    p1.varea(x=x_i, y1=wl_i, y2=hg_i, fill_color="lightblue")
    p1.varea(x=x_i, y1=hg_i, y2=0, fill_color="lightyellow")
    p1.line(x_i, wl_i, line_width=2, line_color='navy', legend_label= "Water Level (m)")       
    p1.line(x_i, hg_i, line_width=2, line_color='brown', legend_label= "Geodetic Height (m)")     
    p1.legend.location = "top_left"


bwc_set = Column(model_type, Title_0, scheme_type, Title_1 ,C_Length, C_Width, H_Res, slope, Title_2, R_value, Disch, Title_3 ,d_x, itterslider, Title_4, run_e, run_i, table, width=500)
Graph = Column(p1, width = 600)

run_e.on_click(explicit)
run_i.on_click(implicit)
curdoc().add_root(Row(bwc_set, Graph))

def ei_interface(active): 
    if active==0:
        #explicit
        itterslider.visible = False
        run_e.visible = True
        run_i.visible = False 
    else:
        #implicit
        itterslider.visible = True 
        run_e.visible = False
        run_i.visible = True

scheme_type.on_click(ei_interface)

# bokeh serve --show myapp.py
# http://localhost:5006/myapp