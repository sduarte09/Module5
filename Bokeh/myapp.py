import numpy as np
from bokeh.layouts import column
from bokeh.models import Slider, Button
from bokeh.plotting import curdoc
from bokeh.models.widgets import PreText


# Sliders
texto = PreText(text="""Please click to compute velocity""",width=500, height=100)
sliderH1 = Slider(start=1, end=10, step=0.1, value=5,title='Tank_Height(m)')
sliderL = Slider(start=50, end=200, step=5, value=100,title='Pipe_Length(m)')
sliderD = Slider(start=0.1, end=1, step=0.05, value=0.15,title='Pipe_Diameter(m)')
sliderf = Slider(start=0.01, end=0.1, step=0.001, value=0.01,title='Friction_coefficient')
button = Button(label="Compute Velocity", button_type="success")

def velocity():
    H1=sliderH1.value
    L=sliderL.value
    D=sliderD.value
    f=sliderf.value
    vel=np.sqrt((2*9.81*H1)/(1+f*(L/D)))
    texto.text=str(vel)
    sliderH1.visible=False

button.on_click(velocity)  
curdoc().add_root(column(sliderH1,sliderL,sliderD,sliderf,button,texto))

# bokeh serve --show myapp.py
# http://localhost:5006/myapp