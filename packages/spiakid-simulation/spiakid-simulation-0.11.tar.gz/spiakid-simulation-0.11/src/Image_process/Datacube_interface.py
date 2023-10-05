from tkinter import * 
from matplotlib.figure import Figure
import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import Image_process.Image_generation as IG



def Interface(Image_size,Object_number):
    fenetre = Tk()
    fenetre.geometry("1250x600")
    fenetre.grid()

    def double_plot(event):
        
        x = int(var_1.get())
        y = int(var_2.get())
        axes_2.clear()
        
        axes_2.plot(data[1],data[0][x,y,1:])
        axes_2.set_xlabel('Wavelength nm')
        axes_2.set_ylabel('Amplitude W/m**2/nm')
        axes_2.set_xscale('log')
        canvas2.draw()
        canvas2.get_tk_widget().grid(column = 2, row = 0)

        pointer = np.zeros(np.shape(data[0][:,:,0]))
        pointer[x,y] = 1
        pointer = np.ma.masked_where(pointer !=1, pointer)
        axes.imshow(data[0][:,:,0],cmap='gray_r')
        axes.imshow(pointer,cmap = 'spring')
        canvas.draw()
    data = IG.Image_Sim(Image_size,Object_number)
    figure = Figure(figsize=(6, 5), dpi=100)
    axes = figure.add_subplot()
    axes.imshow(data[0][:,:,0],cmap='gray_r')
    canvas = FigureCanvasTkAgg(figure,master = fenetre)  

    canvas.draw()
    toolbar = NavigationToolbar2Tk(canvas,fenetre,pack_toolbar = False)
    toolbar.grid(column = 0,row = 1)
    canvas.get_tk_widget().grid(column = 0,row = 0)

    figure_2 = Figure(figsize=(6, 5), dpi=100)
    axes_2 = figure_2.add_subplot()
    canvas2 = FigureCanvasTkAgg(figure_2,master = fenetre) 

    var_1 = DoubleVar()
    var_2 = DoubleVar()
    scale_1 = Scale(fenetre, variable=var_2,from_=0,to=Image_size-1,orient=HORIZONTAL,length= 300)
    scale_1.grid(column = 0,row = 2)
    scale_2 = Scale(fenetre,variable=var_1,from_=0,to=Image_size-1,length = 300)
    scale_2.grid(column = 1,row = 0)
    scale_1.bind("<ButtonRelease-1>",double_plot)
    scale_2.bind("<ButtonRelease-1>",double_plot)


    fenetre.mainloop()
