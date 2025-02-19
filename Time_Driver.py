import tkinter as tk
import tkinter.ttk as ttk 
from datetime import datetime
from pythonosc import udp_client
import sv_ttk

ip = "127.0.0.1"
sendPort = 9000
client = udp_client.SimpleUDPClient(ip, sendPort)

root = None
time_label = None

def send_time(root, time_label, var1, var2, varh, varm, vars):
    now = datetime.now()
    time_format = var1.get()
    time_type = var2.get()
    
    if not time_type:
        hour = float(now.hour / 24.0 if time_format else now.hour / 12.0)
    elif time_type:
        hour = int(now.strftime('%H') if time_format else now.strftime('%I'))
    minute = now.minute / 60.0 if not time_type else now.minute
    second = now.second / 60.0 if not time_type else now.second

    client.send_message(f"/avatar/parameters/{varh.get()}", hour)
    client.send_message(f"/avatar/parameters/{varm.get()}", minute)
    client.send_message(f"/avatar/parameters/{vars.get()}", second)

    if time_format:
        time_display = now.strftime("%H:%M:%S")
    elif not time_format:
        time_display = now.strftime("%I:%M:%S")

    time_label.config(text=f"Time: {time_display}")

    root.after(1000, lambda :send_time(root, time_label, var1, var2, varh, varm, vars))

def Main_Window():
    root = tk.Tk()
    root.title("Time Driver")
    root.geometry("250x100")
    root.minsize(300, 210)
    root.maxsize(300, 210)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    sv_ttk.set_theme("dark")
    style = ttk.Style()

    var1 = tk.BooleanVar()
    var2 = tk.BooleanVar()
    varh = tk.StringVar()
    varm = tk.StringVar()
    vars = tk.StringVar()

    varh.set('OSCHour')
    varm.set('OSCMinute')
    vars.set('OSCSecond')


    style = ttk.Style()
    style.configure('TLabel',background ='#1f1f1f',foreground='#ffffff')

    time_label = ttk.Label(root, anchor='n', text="watch time: --:--:--", font=("Arial", 12),padding=10)
    time_label.grid(row=0, column=0, sticky='nsew')

    style.configure('TRadiobutton',background ='#1f1f1f',foreground='#ffffff')

    time_format12 = ttk.Radiobutton(root,variable=var1,value=0,text='12hr')
    time_format24 = ttk.Radiobutton(root,variable=var1,value=1,text='24hr')
    time_format12.grid(row=0,column=0,sticky='se',padx=(0,30),pady=(0,35))
    time_format24.grid(row=0,column=0,sticky='se',padx=(0,30),pady=(0,5))

    time_typef = ttk.Radiobutton(root,variable=var2,value=0,text='float')
    time_typei = ttk.Radiobutton(root,variable=var2,value=1,text='int')
    time_typef.grid(row=0,column=0,sticky='sw',padx=(30,0),pady=(0,35))
    time_typei.grid(row=0,column=0,sticky='sw',padx=(30,0),pady=(0,5))

    style.configure('TLabelframe',background='#1f1f1f',relief='flat',borderwidth=0,bordercolor='#1f1f1f')
    style.configure('TLabelframe.Label',background='#1f1f1f',foreground='#ffffff')

    paramnames = ttk.Labelframe(root,text='Parameter Names',labelanchor='n',padding=2)
    paramnames.grid(row=0,column=0,sticky='new',pady=(35,0),padx=5)
    paramnames.columnconfigure((0,1),weight=1)
    parameterh =ttk.Entry(paramnames,textvariable=varh,justify='center')
    parameterm =ttk.Entry(paramnames,textvariable=varm,justify='center')
    parameters =ttk.Entry(paramnames,textvariable=vars,justify='center')
    parameterh.grid(row=0,column=1,sticky='nse')
    parameterm.grid(row=1,column=1,sticky='nse')
    parameters.grid(row=2,column=1,sticky='nse')
    parameterhL =ttk.Label(paramnames,text='Hour',justify='center')
    parametermL =ttk.Label(paramnames,text='Minute',justify='center')
    parametersL =ttk.Label(paramnames,text='Second',justify='center')
    parameterhL.grid(row=0,column=0,sticky='nsw',padx=15)
    parametermL.grid(row=1,column=0,sticky='nsw',padx=15)
    parametersL.grid(row=2,column=0,sticky='nsw',padx=15)
    
    send_time(root, time_label, var1, var2, varh, varm, vars)
    root.mainloop()
if __name__ == "__main__":
    Main_Window()