# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 19:43:40 2022

@author: mab020
"""
# Eplicit solution function
def BWC_Explict(L = 10000,b = 65 ,So = 0.001,C = 45,Q = 200,dx = 250, hd = 5):
    # Initial Variables
    
    A = Q**2/(C**2*b**2) # Calculation simplification
     
    # Initialising variables using Initial Condition
    maxcomp = int(L/dx)
    x = [0]
    h = [hd]
    bed = [0]
    wlev = [hd]

    # Numerical Scheme Solution
    # Explicit
    for i in range(1,maxcomp):
         x.append(i*dx)
         # Bed level
         bed.append(So*i*dx)
         # Water depth
         h.append(dx*(A/h[i-1]**(3)-So)+h[i-1])
         # Water level
         wlev.append(h[i]+bed[i])
    #data = np.array(())
    return(x,h,bed,wlev)

# Implicit solution function

def BWC_Implict(L = 10000,b = 65 ,So = 0.001,C = 45,Q = 200,dx = 250, hd = 5,max_itter = 15):
    # Initial Variables
    
    A = Q**2/(C**2*b**2) # Calculation simplification
     
    # Initialising variables using Initial Condition
    maxcomp = int(L/dx)
    x = [0]
    h = [hd]
    bed = [0]
    wlev = [hd]

    # Numerical Scheme Solution
   
    # Implicit
    for i in range(1,maxcomp):
        # first assumption for iteration
        htriR = h[i-1] #m
        x.append(i*dx)
        # Bed level
        bed.append(So*i*dx)
        j = 0
        # Water depth
        error = 10
        
        while error > 0.01:
            if j > max_itter:
                break
            else:
                RHS = A/htriR**3-So
                htril = dx*RHS+h[i-1]
                error = abs(htril-htriR)
                htriR = htril
                j += 1
        h.append(htril)
        # Water level
        wlev.append(h[i]+bed[i])
    return(x,h,bed,wlev)