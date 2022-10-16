from turtle import bgcolor, color
from typing_extensions import runtime
import websocket,json
import numpy as np
from tkinter import *
import tkinter.ttk as ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import tensorflow
from keras.models import load_model
from matplotlib.pyplot import figure
import seaborn as sns
sec1=0
sec2=0
min=0


df=pd.read_csv('stock.csv')
data=df['o']
cdf=data.values
cdf=cdf.reshape(-1,1)
scaler=MinMaxScaler(feature_range=(0,1))
cdf=scaler.fit_transform(cdf)



model = load_model('my_model.h5')


websocket.enableTrace(True)
ws = websocket.WebSocket()
                            
ws.connect("wss://ws.finnhub.io?token=cd2tepaad3ias3n82lq0cd2tepaad3ias3n82lqg")

root=Tk()
root.geometry('520x750')
f=[]
m=[19047.62, 19047.62, 19047.28, 19047.82, 19047.29, 19047.29,
       19047.28, 19047.81, 19047.29, 19047.82, 19047.82, 19047.82,
       19047.3 , 19047.29, 19047.28, 19047.29, 19047.83, 19047.83,
       19047.56, 19047.  , 19046.88, 19046.87, 19046.87, 19047.39,
       19047.29, 19047.29, 19047.29, 19047.94, 19047.94, 19047.3 ,
       19047.99, 19048.  , 19048.  , 19048.03, 19048.03, 19048.05,
       19048.05, 19047.99, 19048.02, 19048.05, 19048.02, 19048.44,
       19048.45, 19048.43, 19048.42, 19048.42, 19048.46, 19048.47,
       19048.48, 19048.51, 19048.51, 19048.51, 19048.54, 19048.62,
       19048.81, 19048.82, 19048.82, 19048.83, 19048.87, 19048.45]
def start():
    global condition,sec1,sec2,min
    if condition==False:
        condition=True
        sec1=0
        sec2=0
        min=0
        loop()
        loop3()
        loop2()

def stop():
    global condition
    condition=False

condition=False
def loop3():
    if condition:
        global sec1,sec2,min
        sec1+=1
        if sec1>=10:
            sec1=0
            sec2+=1
        if sec2>=6:
            sec2=0
            min+=1
            loop2()
        run_time=Label(root,text=f'Run time: {min}:{sec2}{sec1}',font=("Arial", 13)).grid(row=1,column=1)
        loop()
        root.after(1000,loop3)



def loop2():
    if condition:
        ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
        
        m.append( json.loads(ws.recv())["data"][0]['p'])
        lst=np.array(m[len(m)-60:len(m)])
        lst=lst.reshape(-1,1)
        lst=scaler.transform(lst)
        lst=[lst]
        lst=np.array(lst)
        lst=np.reshape(lst,(lst.shape[0],lst.shape[1],1))
        prediction=model.predict(lst)
        prediction=scaler.inverse_transform(prediction)
        s = 100*(prediction[0][0]-m[len(m)-1])/m[len(m)-1]
        display_text.set(f'{"%.2f" %s}%')
        if s<0:
            display.config(font=("Arial", 30),fg='red')
        else: display.config(font=("Arial", 30),fg='green')







def loop():
    if condition:

        ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')


        try:
            for data in json.loads(ws.recv())["data"]:
                f.append( data['p'])
            c=f[len(f)-1]
            b=f[len(f)-2]
            curr.set(f'{"%.2f" %c}')
            if c<b:
                current_value.config(font=("Arial", 15),fg='red')
            else: current_value.config(font=("Arial", 15),fg='green')

            sns.set_style('darkgrid')

            fig = Figure(figsize = (5, 5),
                dpi = 100)

            plot1 = fig.add_subplot(111)
            # plot1.set_xlim([0,1000])
            # plot1.set_ylim([19100,19200])

            plot1.plot(f, linestyle='solid',color='blue')

            canvas = FigureCanvasTkAgg(fig,
                                    master = frame1)  
            canvas.draw()
            canvas.get_tk_widget().grid(row=2,column=0)
        except: print('failed')
            








display_text =StringVar()
display = Label(root, textvariable=display_text)
display.grid(row=3, column=1)
curr =StringVar()
current_value = Label(root,textvariable=curr)
current_value.grid(row=2, column=0,sticky='n')
empty=Label(root,text='Current value:',font=("Arial", 12)).grid(row=1,column=0)
bitcoin=Label(root,text='BITCOIN',font=("Arial", 30)).grid(row=0,column=0)
prediction=Label(root,text='Prediction in the next minute:',font=("Arial", 12)).grid(row=3,column=0,pady=10)


frame1 = Frame(root,bg="black",width=500,height=500)
frame1.grid(row=4,column=0,columnspan=2,padx=10)
ss= ttk.Style()

ss.configure('start.TButton', font=('Helvetica', 13),foreground='green')
ss.configure('stop.TButton', font=('Helvetica', 13),foreground='red')


stop_button= ttk.Button(root, text= "Stop", command=stop, style='stop.TButton').grid(row=5,column=1,pady=20)

start_button=ttk.Button(root, text= "Start", command=start, style='start.TButton').grid(row=5,column=0,pady=20)





root.mainloop()