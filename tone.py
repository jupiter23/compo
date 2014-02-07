from pyo import *

class Notes():
  def __init__(self, root = 277.2):
    self.root = root
    self.setNotes(self.root)
  
  def setNotes(self, root):
    self.notes = {
      'just' : [root, root * 16/15, root * 9/8, root * 6/5, root * 5/4, root * 4/3, root * 64/45, root * 3/2, root * 8/5, root * 5/3, root * 16/9, root * 15/8],
      'equal' : [root * pow(2, i/12)  for i in range(0, 11)]
    }
    
  def getNotes(self):
    return self.notes
    
  def getNote(self, tuning = 'equal', degree = 0):
    return self.notes[tuning[degree + 1]]  