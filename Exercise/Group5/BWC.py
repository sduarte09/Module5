from bokeh.layouts import column
from bokeh.models.widgets import RadioButtonGroup,Select, Div, Button,PreText
from bokeh.models import  TextInput, RadioGroup
from bokeh.plotting import curdoc

button_group = RadioButtonGroup(labels=["Physical parameters", "Geometric parameters", "Initial  conditions"], active=1)

## Add the elements inside each radio button

slope  = TextInput(value='25', title="slope:")

###### Drop down menus

Coefficient = Select(title="Coefficient:", value="chezy", options=["Manning", "chezy"])
Coefficient_value1  = TextInput(value=" ", title="chezy:" )
Coefficient_value2  = TextInput(value=" ", title="Manning:" )

#### Add geometric parameters
length  = TextInput(value=" ", title="Length:")
width  = TextInput(value=" ", title="Width:")

#LABELS = ["km", "m"]
#radio_group = RadioGroup(labels=LABELS, active=0)
#### Add ginitial conditiions
depth = TextInput(value=" ", title="Depth(m):")
Q = TextInput(value=" ", title="Discharge(m3/sec):")
texto = PreText(text="""Please click here""",width=500, height=100)
layout = ()
def button_group_change(active):
    ch = active
    if ch == 0:
       slope.visible=True
       Coefficient.visible=True
       Coefficient_value1.visible=True
       Coefficient_value2.visible=True
       length.visible=False
       width.visible=False
       depth.visible=False
       Q.visible=False
       # layout= column(slope, Coefficient,Coefficient_value1, Coefficient_value2)
   
    elif ch == 1:
         length.visible=True
         width.visible=True
         slope.visible=False
         Coefficient.visible=False
         Coefficient_value1.visible=False
         Coefficient_value2.visible=False
         depth.visible=False
         Q.visible=False
        # layout= column(length, width)

    elif ch == 2:
        depth.visible=True
        Q.visible=True
        slope.visible=False
        Coefficient.visible=False
        Coefficient_value1.visible=False
        Coefficient_value2.visible=False
        length.visible=False
        width.visible=False
        # layout= column(length, width )
    texto.text ='text' #str(layout)

    #curdoc().add_root(column(button_group,slope, Coefficient))
    #curdoc().add_root(row(button_group,length))
layout= column(slope, Coefficient,Coefficient_value1, Coefficient_value2,length, width,length)    
button_group.on_click(button_group_change)
###show
curdoc().add_root(column(texto,button_group,layout))
#bokeh serve --show BWC.py
