import wx
# Matplotlib Figure object
from matplotlib.figure import Figure
# import the WxAgg FigureCanvas object, that binds Figure to
# WxAgg backend. In this case, this is a wxPanel
from matplotlib.backends.backend_wxagg import \
            FigureCanvasWxAgg as FigureCanvas
import numpy as np

#Draggable line for matplotlib picture
from DraggableCursorX import DraggableCursorX
#Data files handler
from DataLoader import DataLoader

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
        
        self.cid_right_press = self.canvas.mpl_connect(
                    'button_press_event', self.onRightPress)
        self.cid_right_release = self.canvas.mpl_connect(
                    'button_release_event', self.onRightRelease)
        
    
    def onRightPress(self, event):
        if event.button == 3:
        
            if self.save:
                #save cursor position from previous data
                self.positions[(self.l, self.pos)] = self.cursor.get_position()
            
            x, y = None, None
            try:
                while not x and not y:
                    l, pos, x, y = self.dataloader.next()
                
                self.save = True
                #save indices for the next rightButtonClick
                self.l = l
                self.pos = pos
                
                #clean axes
                self.axes.cla()
                
                #set title of the figure as wafer coordinates
                self.axes.set_title("%s, %s" % (l, pos))
                #give title to axes
                self.axes.set_xlabel(r'$2\theta$ (deg)')
                self.axes.set_ylabel(r'intensity (cps)')
                #plot intensity versus 2theta in log scale
                self.axes.semilogy(x, y, 'b-', linewidth = 3)

                #draggable cursor
                self.cursor = DraggableCursorX(self.axes)
                self.cursor.connect()
                
                self.canvas.draw()
                
            except StopIteration:
                self.cursor.disconnect()
                self.save = False
                if not self.saved:
                    self.time_to_save = True
                    
    
    def onRightRelease(self, event):
        #on right mouse button release
        if event.button == 3:
            if self.saved:
                #Create a message dialog box
                dlg = wx.MessageDialog(self, "Load new data to analize or exit", "Warning", wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
            if self.time_to_save:
                #propose to save file
                dlg = wx.FileDialog(self, "Save data file", self.dirname, "",
                            "*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
                if dlg.ShowModal() == wx.ID_OK:
                    # save content in the file
                    path = dlg.GetPath()
                    self.saveData(path, self.positions)
                    dlg.Destroy()
                    
                    #indicates whether data was saved
                    self.saved = True
                    self.time_to_save = False
                    
    
    def saveData(self, path, positions_map):
        letter_positions = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        number_positions = [-45, -35, -25, -15, -5, 5, 15, 25, 35, 45]
        
        with open(path, 'w') as f:
            for i in range(len(number_positions)):
                pos = number_positions[i]
                for letter in letter_positions:
                    tup = (letter, pos)
                    if tup in positions_map:
                        f.write('%.4f\t' % positions_map[tup])
                        #print letter, i, positions_map[tup]
                    else:
                        f.write('--\t')
                f.write('\n')
                    
    #menu event handlers
    def onOpen(self, event):
        dlg = wx.DirDialog(self, "Choose a directory:")
        if dlg.ShowModal() == wx.ID_OK:
            self.dirname = dlg.GetPath()
        dlg.Destroy()
        
        self.saved = False
        self.save = False
        self.time_to_save = False
        self.positions = {}
        self.dataloader = DataLoader(self.dirname, "y-scan*.dat")
        
    def onExit(self, event):
        self.Close(True)
        
    def onAbout(self, event):
        #Create a message dialog box
        dlg = wx.MessageDialog(self, "XRD Fringer v0.92", "XRD", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
