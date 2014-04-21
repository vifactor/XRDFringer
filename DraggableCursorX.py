from DraggableLine import DraggableLine

class DraggableCursorX(DraggableLine):
    def __init__(self, axes):
        
        xmin, xmax = axes.get_xlim()
        ymin, ymax = axes.get_ylim()
        xmed = (xmin + xmax) / 2
        line, = axes.plot([xmed, xmed], [ymin, ymax], "k-", linewidth = 1.5)
        DraggableLine.__init__(self, line)
    
    def get_dxdy(self, event):
        """returns change of the line position, overriden method of DraggableLine: dy = 0"""
        xpress, ypress = self.press
        
        dx = (event.xdata - xpress)

        #save the current data as press data
        self.press = event.xdata, event.ydata
        
        return dx, 0.0
    
    def get_position(self):
        return self.line.get_xdata()[0]
