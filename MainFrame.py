import wx
# Matplotlib Figure object
from matplotlib.figure import Figure
# import the WxAgg FigureCanvas object, that binds Figure to
# WxAgg backend. In this case, this is a wxPanel
from matplotlib.backends.backend_wxagg import \
            FigureCanvasWxAgg as FigureCanvas
import os
#Draggable line for matplotlib picture
from DraggableCursorX import DraggableCursorX

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # initialize the superclass, the wx.Frame
        wx.Frame.__init__(self, None, wx.ID_ANY, title='XRDFringer', size=(640, 480))
        
        # usual Matplotlib functions
        self.figure = Figure()#figsize=(6, 4), dpi=100)
        self.axes = self.figure.add_subplot(111)
        # initialize the FigureCanvas, mapping the figure to
        # the Wx backend
        self.canvas = FigureCanvas(self, wx.ID_ANY, self.figure)
        
        #Temporary DraggableLine preparation
        self.cursor = DraggableCursorX(self.axes)
        self.cursor.connect()
        


