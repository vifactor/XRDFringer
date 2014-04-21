from matplotlib.lines import Line2D

class DraggableLine:
    def __init__(self, line):
        self.line = line
        self.press = None
    
    def connect(self):
        # connect to all the matplotlib events we need
        self.cid_press = self.line.figure.canvas.mpl_connect(
                    'button_press_event', self.onLeftPress)
        self.cid_release = self.line.figure.canvas.mpl_connect(
                    'button_release_event', self.onLeftRelease)
        self.cid_motion = self.line.figure.canvas.mpl_connect(
                    'motion_notify_event', self.onMotion)
    
    def onLeftPress(self, event):
        #only left button event is considered
        if event.button != 1: return
        #return if press event has happened outside the axes of the figure
        if event.inaxes != self.line.axes: return
        
        contains, attrd = self.line.contains(event)
        if not contains: return
        
        self.press =  event.xdata, event.ydata
        
        
    def onLeftRelease(self, event):
        #right button release is ignored
        if event.button != 1: return
        #on release we reset the press data
        self.press = None
        self.line.figure.canvas.draw()
        
    def onMotion(self, event):
        #on motion we will move the line
        if self.press is None: return
        
        if event.inaxes != self.line.axes: return
        x0 = self.line.get_xdata()
        y0 = self.line.get_ydata()
        
        xpress, ypress = self.press
        
        dx = (event.xdata - xpress)
        dy = (event.ydata - ypress)
        
        #print "event.data:", event.xdata, event.ydata
        #print "press:", xpress, ypress
        #print "dr:", dx, dy
        
        #save the current data as press data
        self.press = event.xdata, event.ydata
        
        x0[:] = [x + dx for x in x0]
        y0[:] = [y + dy for y in y0]
        
        print dx, dy
        print x0, y0
        
        self.line.set_xdata(x0)
        self.line.set_ydata(y0)
        
        self.line.figure.canvas.draw()
    
    def disconnect(self):
        # disconnect to all the stored connection events
        self.line.figure.canvas.mpl_disconnect(self.cid_press)
        self.line.figure.canvas.mpl_disconnect(self.cid_release)
        self.line.figure.canvas.mpl_disconnect(self.cid_motion)
