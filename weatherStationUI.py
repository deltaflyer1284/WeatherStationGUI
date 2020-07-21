# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 14:13:32 2020

@author: adyru
"""


from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

import matplotlib
matplotlib.use('TkAgg')


import requests
import json
import pandas as pd
# from tkinter import ttk
# from tkinter import font





from datetime import datetime

        
        
     
class WeatherStationWidget(QMainWindow):
    
    def __init__(self):
        
        QMainWindow.__init__(self)

        loadUi("weatherStationMain.ui",self)
        
        self.listWidget.itemClicked.connect(self.updatePlot)
        self.refreshButton.clicked.connect(self.refresh)
        self.actionRefresh.triggered.connect(self.refresh)
        self.quitButton.clicked.connect(QApplication.instance().quit)
        self.refresh()

        
 

        
    def refresh(self):       
        url = requests.get('https://api.thingspeak.com/channels/773699/feeds.json?api_key=SPTQSAZ4BK8EO3C8&results=3000')
        data= json.loads(url.text)
        global df
        df = pd.json_normalize(data['feeds'])
        df[df.columns[2:8]]=df[df.columns[2:8]].astype(float)
        
        df[df.columns[0]] = pd.to_datetime(df[df.columns[0]])
        i=0
        for i in range(6):
            df.columns.values[i+2]=data['channel'][df.columns[i+2]]
        df.columns=df.columns.astype(str)
        df.airT=df.airT*1.8 +32
        
        
        for i in range(6):
            df.iloc[:,i+2]=round(df.iloc[:,i+2],1)
            
        self.airQ.setText(str(df.airQ[len(df)-1]))
        self.airTemp.setText(str(df.airT[len(df)-1]))
        self.volt.setText(str(df.sysV[len(df)-1]))
        self.airHum.setText(str(df.airH[len(df)-1]))
        self.press.setText(str(df.press[len(df)-1]))
        self.watt.setText(str(df.sysW[len(df)-1]))
        
        now = datetime.now()
        
        current_time = now.strftime("%H:%M:%S")
        self.refreshTime.setText(current_time)
        

    def updatePlot(self, item):
    
        nrec = self.spinBox.value()
        listVar = item.text()
        val = self.getVar(listVar)
        
        tempDF=df.loc[len(df)-nrec:len(df)-1,:]
        date=tempDF.created_at.astype('O')
        
        self.plotWidget.canvas.axes.clear()
        self.plotWidget.canvas.axes.plot_date(date,tempDF.iloc[:,val],xdate=True,tz='US/Pacific',linestyle='dashed',color = 'blue')
        self.plotWidget.canvas.axes.set_ylabel(listVar,fontsize=16)
        
        self.plotWidget.canvas.draw()

    def getVar(self,argument):
        
        
        switcher = {
            "Air Temperature": 5,
            "Air Humidity": 6,
            "Pressure": 7,
            "Air Quality": 2,
            "Voltage": 3,
            "Power": 4,
     
        }
        return switcher.get(argument,-1)
        
        
        
        
app = QApplication([])
window = WeatherStationWidget()
window.show()
app.exec_()
