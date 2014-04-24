import os
import glob

class DataLoader:
    def __init__(self, directory, pattern):
        """searches for all files from the directory which satisfy the regex"""
        os.chdir(directory)
        self.filelist = iter(glob.glob(pattern))
        self.fileitem = None
    
    def __iter__(self):
        return self
        
    def next(self):
        try:
            return self.fileitem.next()
        except (StopIteration, AttributeError):
            filename = self.filelist.next()
            self.fileitem = FileItem(filename)
            self.fileitem.load()
            return self.fileitem.next()

import csv
import re
class FileItem:
    def __init__(self, filename):
        """creates an object of fileitem with handy methods"""
        self.filename = filename
        self.collection = {}
        
        #index is a letter between "_" and "." characters 
        match = re.search(r".*_(\w)\..*$", self.filename)
        self.lindex = match.group(1)
        
        
    def load(self):
        with open(self.filename, 'rb') as f:
            csv_file = csv.reader(CommentedFile(f), delimiter='\t')
            for row in csv_file:
                if row:
                    # Omega	2Theta	Phi  	Chi   	X    	Y    	Z    	q_para	q_perp	Intensity
                    omega, ttheta, phi, chi, x, y, z, q_para, q_perp, intensity = map(float, row)
                    if y in self.collection:
                        self.collection[y].append((ttheta, intensity))
                    else:
                        self.collection[y] = [(ttheta, intensity)]
                        
            self.collection_iterator = iter(self.collection)
        
    def getFilename(self):
        return self.filename
    
    def __iter__(self):
        return self
    
    def next(self):
        #key is y position, val is two arrays defining scan
        key = self.collection_iterator.next()
        val = self.collection[key]
        
        x, y = zip(*val)
        
        return self.lindex, key, x, y
        
class CommentedFile:

    def __init__(self, f, commentstring="#"):
        self.f = f
        self.commentstring = commentstring
        
    def next(self):
        line = self.f.next()
        while line.startswith(self.commentstring):
            line = self.f.next()
        return line
        
    def __iter__(self):
        return self
