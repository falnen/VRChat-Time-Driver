from Persistence import savePnamesToFile, loadPNamesFromFile
import tkinter as tk
import tkinter.ttk as ttk 
from datetime import datetime
from pythonosc import udp_client
import sv_ttk
from tinyoscquery.queryservice import OSCQueryService
from tinyoscquery.utility import get_open_tcp_port, get_open_udp_port

OSCqs = OSCQueryService('VRCTimeDriver',get_open_tcp_port(),get_open_udp_port())

ip = "127.0.0.1"
sendPort = 9000
client = udp_client.SimpleUDPClient(OSCqs.oscIp, OSCqs.oscPort)

Root = tk.Tk()
Root.title("Time Driver")
Root.geometry("300x210")
Root.minsize(300, 210)
Root.maxsize(300, 210)
Root.columnconfigure(0, weight=1)
Root.rowconfigure(0, weight=1)

sv_ttk.set_theme("dark")

PNames = loadPNamesFromFile()
PHour = tk.StringVar(value=PNames["Hour"] if PNames else "OSCHour")
PMinute = tk.StringVar(value=PNames["Minute"] if PNames else "OSCMinute")
PSecond = tk.StringVar(value=PNames["Second"] if PNames else "OSCSecond")

varf = tk.BooleanVar()
vart = tk.BooleanVar()

time_label = ttk.Label(Root, anchor='n', text="watch time: --:--:--", font=("Arial", 12), padding=10)
time_label.grid(row=0, column=0, sticky='nsew')

time_format12 = ttk.Radiobutton(Root, variable=varf, value=0, text='12hr')
time_format24 = ttk.Radiobutton(Root, variable=varf, value=1, text='24hr')
time_format12.grid(row=0, column=0, sticky='se', padx=(0,30), pady=(0,35))
time_format24.grid(row=0, column=0, sticky='se', padx=(0,30), pady=(0,5))

time_typef = ttk.Radiobutton(Root, variable=vart, value=0, text='float')
time_typei = ttk.Radiobutton(Root, variable=vart, value=1, text='int')
time_typef.grid(row=0, column=0, sticky='sw', padx=(30,0), pady=(0,35))
time_typei.grid(row=0, column=0, sticky='sw', padx=(30,0), pady=(0,5))

ParamFrame = ttk.Labelframe(Root, text='Parameter Names', labelanchor='n', padding=2)
ParamFrame.grid(row=0,column=0, sticky='new', pady=(35,0), padx=5)
ParamFrame.columnconfigure((0,1), weight=1)

HourEntry =ttk.Entry(ParamFrame, textvariable=PHour, justify='center')
MinuteEntry =ttk.Entry(ParamFrame, textvariable=PMinute, justify='center')
SecondEntry =ttk.Entry(ParamFrame, textvariable=PSecond, justify='center')
HourEntry.grid(row=0, column=1, sticky='nse')
MinuteEntry.grid(row=1, column=1, sticky='nse')
SecondEntry.grid(row=2, column=1, sticky='nse')

HourLabel =ttk.Label(ParamFrame, text='Hour',justify='center')
MinuteLabel =ttk.Label(ParamFrame, text='Minute',justify='center')
SecondLabel =ttk.Label(ParamFrame, text='Second',justify='center')
HourLabel.grid(row=0, column=0, sticky='nsw', padx=15)
MinuteLabel.grid(row=1, column=0, sticky='nsw', padx=15)
SecondLabel.grid(row=2, column=0, sticky='nsw', padx=15)

def send_time():
    now = datetime.now()
    time_format = varf.get()
    time_type = vart.get()
    
    if not time_type:
        hour = float(now.hour / 24.0 if time_format else now.hour / 12.0)
    elif time_type:
        hour = int(now.strftime('%H') if time_format else now.strftime('%I'))
    minute = now.minute / 60.0 if not time_type else now.minute
    second = now.second / 60.0 if not time_type else now.second

    client.send_message(f"/avatar/parameters/{HourEntry.get()}", hour)
    client.send_message(f"/avatar/parameters/{MinuteEntry.get()}", minute)
    client.send_message(f"/avatar/parameters/{SecondEntry.get()}", second)

    time_display = now.strftime("%H:%M:%S") if time_format else now.strftime("%I:%M:%S")

    time_label.config(text=f"Time: {time_display}")
    delay = 1000 - now.microsecond // 1000
    Root.after(delay, send_time)

def onCLose():
    savePnamesToFile(PHour.get(),PMinute.get(),PSecond.get())
    OSCqs.http_server.shutdown()
    OSCqs.http_server.server_close()
    OSCqs.http_thread.join()
    OSCqs._zeroconf.unregister_all_services()
    OSCqs._zeroconf.close()
    OSCqs._zeroconf.unregister_all_services = lambda: None
    Root.destroy()

send_time()
Root.protocol("WM_DELETE_WINDOW", onCLose)
Root.mainloop()