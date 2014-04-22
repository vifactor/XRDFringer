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
        
        # Menu Bar
        self.menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        self.Open = wx.MenuItem(wxglade_tmp_menu, wx.ID_OPEN, "&Open", "Open directory", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.Open)
        self.Exit = wx.MenuItem(wxglade_tmp_menu, wx.ID_EXIT, "E&xit", "Terminate the program", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.Exit)
        self.menubar.Append(wxglade_tmp_menu, "File")
        wxglade_tmp_menu = wx.Menu()
        self.About = wx.MenuItem(wxglade_tmp_menu, wx.ID_ABOUT, "&About", "Information about this program", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.About)
        self.menubar.Append(wxglade_tmp_menu, "Help")
        self.SetMenuBar(self.menubar)
        # Menu Bar end
        # Menu bindings
        self.Bind(wx.EVT_MENU, self.onOpen, self.Open)
        self.Bind(wx.EVT_MENU, self.onExit, self.Exit)
        self.Bind(wx.EVT_MENU, self.onAbout, self.About)
        # Menu bindings end
        
        self.cid_rightclick = self.canvas.mpl_connect(
                    'button_press_event', self.onRightClick)
    
    def onRightClick(self, event):
        if event.button == 3:
            print self.cursor.get_position()
    
    #menu event handlers
    def onOpen(self, event):
        pass
    
    def onExit(self, event):
        self.Close(True)
        
    def onAbout(self, event):
        #Create a message dialog box
        dlg = wx.MessageDialog(self, "XRD Fringer v0.1", "XRD", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

