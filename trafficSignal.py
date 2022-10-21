import tkinter as Tkinter
import tkinter.font as tkFont
import time
# Starting point for traffice light simulation # this file provides a GUI of four traffic_signals at an intersection
# Author: John M. Hunt
# traffic_signal provides a three light - red, yellow, green - signal displayed with a label over the top

class traffic_signal:
  def __init__(self,name,C,offset):
    self.name = name # name used as a label over the top of the signal
    self.C = C # canvas   to draw on
    self.offset = offset # position left to right for this instance to draw its light
    name_font = tkFont.Font(family="Helvetica",size=20, weight="bold")
    C.create_text(offset+50,15,font=name_font,text=name)
    C.create_rectangle(offset+0,30,offset+100,370,fill="black")
    C.create_oval(offset+3,40,offset+100,140,fill="grey")
    C.create_oval(offset+3,150,offset+100,250,fill="grey")
    C.create_oval(offset+3,260,offset+100,360,fill="grey")
    self.redLight = self.C.create_oval(self.offset+3,40,self.offset+100,140,fill="red")
    self.yellowLight = self.C.create_oval(self.offset+3,150,self.offset+100,250,fill="yellow")
    self.greenLight = self.C.create_oval(self.offset+3,260,self.offset+100,360,fill="green")

  def setRed(self):
    self.redLight = self.C.create_oval(self.offset+3,40,self.offset+100,140,fill="red")

  def setYellow(self):
    self.yellowLight = self.C.create_oval(self.offset+3,150,self.offset+100,250,fill="yellow")

  def setGreen(self):
    self.greenLight = self.C.create_oval(self.offset+3,260,self.offset+100,360,fill="green")

  def clearAll(self):
    self.C.delete(self.redLight)
    #self.C.delete(self.yellowLight)
    self.C.delete(self.greenLight)
