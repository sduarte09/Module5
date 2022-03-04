from bokeh.layouts import widgetbox, column
from bokeh.models.widgets import  Select, Button, TextInput
from bokeh.plotting import figure, curdoc

River_W = TextInput(value="0", title="River Width (m)")


River_L = TextInput(value="0", title="River Length (m)")


Slope = TextInput(value="0", title="Bottom Slope")


h_0 = TextInput(value="0", title="Depth at the Mouth (m)")


Chezy_C = TextInput(value="0", title="Chezy Coeficient")


Q_0 = TextInput(value="0", title="Discharge (m3/sec)")


Dx = TextInput(value="1", title="Computational Step (m)")

Run_Button = Button(label="Run Model", button_type="success")

p = figure(width=400, height=400, title="Back Water Curve")

def plot_function():
    p.renderers=[]
    b  = float(River_W.value)                                                                     
    hd = float(h_0.value)                                                                         
    Q  = float(Q_0.value)                                                                      
    C  = float(Chezy_C.value)                                                                        
    So = float(Slope.value)                                                                 
    L  = float(River_L.value)                                                                      
    dx = float(Dx.value)

    maxcom = int(L/dx) + 1 
    x1      = [0]                                                                    
    Hw_Exp = [hd]                                                                 
    Hw_Imp = [hd]                                                                 
    Hw_Comb= [hd]                                                                  
    Hg     = [0]                                                                   
    Wl_Exp = [hd]                                                                  

    i = 1
    while i <= maxcom:
        x1.append(x1[i-1] + dx)
        Hg.append(i * dx * So)
        Hw_Exp.append(Hw_Exp[i-1] + dx * (((Q**2 / (C**2 * Hw_Exp[i-1]**3 * b**2))-So)))
        Wl_Exp.append(Hw_Exp[i] + Hg[i])
        i = i + 1

    p.varea(x=x1, y1=Hg, y2=Wl_Exp)
    p.line(x=x1,y=Hg, color="black", width=2)
    p.line(x=x1, y=Wl_Exp, color="black", width=2)        

    

Run_Button.on_click(plot_function)
curdoc().add_root(column(River_W, River_L, Slope, h_0, Chezy_C, Q_0, Dx, Run_Button, p))

# bokeh serve --show Assignment.py
# http://localhost:5006/Assignment