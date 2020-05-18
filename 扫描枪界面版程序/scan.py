import tkinter as tk
import tkinter.messagebox
import serial
import time
import tornado.httpclient
import json
import threading

############### funtion #################
# 创建一个函数，修改文字的内容
on = False
def button_on_click():
    global on    # 在函数里面，获取函数外面的变量
    if on == False:
        label_text.set("Python棒棒哒！")
        on = True
    else:
        label_text.set("我学习，我骄傲！")
        on = False

def recv(serial):
    while True:
        data = serial.read_all()
        if data == '':
            continue
        else:
            break
        time.sleep(1)
    return data

def json_post(http_client,host,cmd):
    try:
        print(cmd)
        body = json.dumps(cmd)
        print(body)
        arg = tornado.httpclient.HTTPRequest(
            url=host,
            method="POST",
            headers={'Content-Type': 'application/json'},
            body=body)
        response = http_client.fetch(arg)
        ret = json.loads(response.body)
        print(ret)
        return ret
    except tornado.httpclient.HTTPError as e:
        print("Http Error: " + str(e))
    except Exception as e:
        print("Error: " + str(e))

    return None

def do_post(obj):
    client = tornado.httpclient.HTTPClient()
    info = host_get1()
    host = info[0]
    sta = info[1]
    recv_get = json_post(client,host,{
        sta + "." + sta + ".process":True,
        sta + "." + sta + ".gun": obj
    })
    return recv_get

################# window ################
# 创建窗口
window = tk.Tk()
# 设置标题
window.title(u"智能扫码枪链接系统")
# 设置大小
window.geometry('800x600')

# 设置文字变量
label_text = tk.StringVar()
# 创建标签对象，配置背景色，宽度和高度
label = tk.Label(textvar=label_text, bg="yellow", width=30, height=3)
# 将标签添加到窗口
label.pack()
# 设置文字变量的内容
label_text.set("扫码枪连接")

############### mes info ################
mes_urlinfo = tk.Label(text = u"MES接口地址：",width = 15,height = 2,font = ('Arial',10))
mes_urlinfo.place(relx = 0.03,y = 500)
mes_url = tk.Entry(window,show = None,font =('Arial',13),width=50)
mes_url.place(relx = 0.18, y = 510)

mes_stainfo = tk.Label(text = u"对应工位号：",width = 15,height = 2,font = ('Arial',10))
mes_stainfo.place(relx = 0.58,y = 160)
mes_sta = tk.Entry(window,show = None,font =('Arial',12),width=20)
mes_sta.place(relx = 0.74, y = 165)

mes_stainfo2 = tk.Label(text = u"对应工位号：",width = 15,height = 2,font = ('Arial',10))
mes_stainfo2.place(relx = 0.58,y = 310)
mes_sta2 = tk.Entry(window,show = None,font =('Arial',12),width=20)
mes_sta2.place(relx = 0.74, y = 315)

mes_stainfo3 = tk.Label(text = u"对应工位号：",width = 15,height = 2,font = ('Arial',10))
mes_stainfo3.place(relx = 0.58,y = 450)
mes_sta3 = tk.Entry(window,show = None,font =('Arial',12),width=20)
mes_sta3.place(relx = 0.74, y = 455)


def host_get1():
    mes_urldata = (mes_url.get().replace(" ",""))
    mes_stadata = (mes_sta.get().replace(" ",""))
    print(mes_urldata,mes_stadata)
    if mes_urldata and mes_stadata:
        a = {}
        a["url"]=mes_urldata
        a["sta"]=mes_stadata
        return a
    else:
        tkinter.messagebox.showinfo(title='Error', message=u'存在空值！')

def host_get2():
    mes_urldata = (mes_url.get().replace(" ", ""))
    mes_stadata = (mes_sta2.get().replace(" ", ""))
    print(mes_urldata, mes_stadata)
    if mes_urldata and mes_stadata:
        a = {}
        a["url"] = mes_urldata
        a["sta"] = mes_stadata
        return a
    else:
        tkinter.messagebox.showinfo(title='Error', message=u'存在空值！')

def host_get3():
    mes_urldata = (mes_url.get().replace(" ", ""))
    mes_stadata = (mes_sta3.get().replace(" ", ""))
    print(mes_urldata, mes_stadata)
    if mes_urldata and mes_stadata:
        a = {}
        a["url"] = mes_urldata
        a["sta"] = mes_stadata
        return a
    else:
        tkinter.messagebox.showinfo(title='Error', message=u'存在空值！')

############## use funtion ##################
intv1 = tk.IntVar()
intv2 = tk.IntVar()
intv3 = tk.IntVar()
a = {}
def gun_use():
    if intv1.get() == 1:
        a["1"]=1
    else:
        a["1"]=0
    if intv2.get() == 1:
        a["2"] = 1
    else:
        a["2"] = 0
    if intv3.get() == 1:
        a["3"] = 1
    else:
        a["3"] = 0
    return a
checkb = tk.Checkbutton(variable=intv1, onvalue=1, offvalue=0, command=gun_use)
checkb.place(relx = 0.68 , y = 114)
checkb2 = tk.Checkbutton(variable=intv2, onvalue=1, offvalue=0, command=gun_use)
checkb2.place(relx = 0.68 , y = 264)
checkb3 = tk.Checkbutton(variable=intv3, onvalue=1, offvalue=0, command=gun_use)
checkb3.place(relx = 0.68 , y = 414)

############## supple show ##############
showinfo = tk.Label(text = u"扫码内容显示",width = 10,height = 2,font = ('Arial',12))
showinfo.place(relx = 0.24,y = 70)

use_mes = tk.Label(text = u"上抛系统",width = 6,height = 2,font = ('Arial',10))
use_mes.place(relx = 0.58,y = 70)

useing = tk.Label(text = u"确定使用",width = 6,height = 2,font = ('Arial',10))
useing.place(relx = 0.666,y = 70)

############## choose com ###############
com_list = ["COM1","COM2","COM3","COM4","COM5","COM6","COM7","COM8"]
v = tk.StringVar(window)
v.set(u"请选择串口")
v2 = tk.StringVar(window)
v2.set(u"请选择串口")
v3 = tk.StringVar(window)
v3.set(u"请选择串口")

com = {}

def choose_com(event):
    chose = v.get()
    chose2 = v2.get()
    chose3 = v3.get()
    com["1"]=chose
    com["2"] = chose2
    com["3"] = chose3
    return com


listb = tk.OptionMenu(window,v,*tuple(com_list))
listb.bind('<Button-1>', choose_com)
listb.place(relx = 0.73 , y = 110)

listb2 = tk.OptionMenu(window,v2,*tuple(com_list))
listb2.bind('<Button-1>', choose_com)
listb2.place(relx = 0.72 , y = 260)

listb3 = tk.OptionMenu(window,v3,*tuple(com_list))
listb3.bind('<Button-1>', choose_com)
listb3.place(relx = 0.72 , y = 410)


############## show gun 1 ###############
gun = tk.Label(text = u"扫码枪1:",width = 10,height = 2,font = ('Arial',12))
gun.place(relx = 0.02 , y = 110)
gun1_info = tk.StringVar()
showdata = tk.Label(textvar = gun1_info,height = 2,width = 50,bg= "white")
showdata.place(relx = 0.13 , y = 110)
checkb_mes = tk.Checkbutton()
checkb_mes.place(relx = 0.61 , y = 114)

def txt_show(s):
    gun1_info.set(s)
    return s

button = tk.Button(text=u'测试', width=10, height=2, command=host_get2)
button.place(relx = 0.88, y = 100)


############## show gun 2 ###############
gun2 = tk.Label(text = u"扫码枪2:",width = 10,height = 2,font = ('Arial',12))
gun2.place(relx = 0.02 , y = 260)
gun2_info = tk.StringVar()
showdata2 = tk.Label(textvar = gun2_info,height = 2,width = 50,bg= "white")
showdata2.place(relx = 0.13 , y = 260)
checkb_mes2 = tk.Checkbutton()
checkb_mes2.place(relx = 0.61 , y = 264)


button2 = tk.Button(text=u'测试', width=10, height=2, command=host_get2)
button2.place(relx = 0.88 , y = 250)


############## show gun 3 ###############
gun3 = tk.Label(text = u"扫码枪3:",width = 10,height = 2,font = ('Arial',12))
gun3.place(relx = 0.02 , y = 410)
gun3_info = tk.StringVar()
showdata3 = tk.Label(textvar = gun3_info,height = 2,width = 50,bg= "white")
showdata3.place(relx = 0.13 , y = 410)
checkb_mes3 = tk.Checkbutton()
checkb_mes3.place(relx = 0.61 , y = 414)


button3 = tk.Button(text=u'测试', width=10, height=2, command=host_get3)
button3.place(relx = 0.88 , y = 400)

# window.mainloop()
def appstart():
    print("运行")
    gun_use()
    # com = choose_com()
    if a["1"]==1 and com["1"]:
        serial1 = serial.Serial(com["1"],9600,timeout=0.5)
        if not serial1.isOpen():
            tkinter.messagebox.showinfo(title='Error', message=u'串口打开错误，请检查配置！')
        while True:
            data = recv(serial1)
            if data != b'':
                str1 = str(data,'utf-8')
                obj = str1.replace("\r","")
                x = txt_show(obj)
                print(x)
                rec = do_post(obj)
                print(rec)
    elif a["1"]==0:
        tkinter.messagebox.showinfo(title='Warning', message=u'未选择任何扫码枪')
    elif com["1"]:
        tkinter.messagebox.showinfo(title='Warning', message=u'未选择串口号，请确认！')
    if a["2"]==1 and com["2"]:
        print(22)

    if a["3"]==1 and com["3"]:
        print(22)


start = tk.Button(text=u'启动', width=10, height=2, command=appstart)
start.place(relx = 0.88 , y = 500)




window.mainloop()