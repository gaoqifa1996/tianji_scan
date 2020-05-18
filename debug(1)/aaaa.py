import serial
from time import sleep
import tornado
from tornado import httpclient
import json
import configparser
import os

config_init = configparser.ConfigParser()
path = os.path.split(os.path.realpath(__file__))[0]
print('#### 配置文件读取目录为：' + path + " ####")
config_init.read(os.path.join(path, 'config/config.ini'), encoding='utf-8-sig')



########### 以下内容需要更具实际情况更改  ############
# 上抛接口地址
def host_get():
    host = config_init['url']['urladd']
    return host

#工位扫码枪清单 L M R 分别为左中右 固定不变 更具实情 更改对应位置后的对应值 0 不存在 1存在
list = {
    "L":config_init['gun_list']['gun1'],
    "M":config_init['gun_list']['gun2'],
    "R":config_init['gun_list']['gun3']
}
print(list)
#工位扫码枪串口清单 L M R 分别为左中右 固定不变 更具实情 更改对应位置后的对应值 不存在None 存在以字符串大写形式表示 如 "COM4"
com1 = config_init['com_list']['gun1_com']
com2 = config_init['com_list']['gun2_com']
com3 = config_init['com_list']['gun3_com']
com = {
    "L":com1,
    "M":com2,
    "R":com3
}
print(com)
#工位扫码枪串口波特率清单 L M R 分别为左中右 固定不变 更具实情 更改对应位置后的对应值 不存在None 存在以数字整形形式表示 如 9600
bau1 = config_init['bau_list']['gun1_bau']
bau2 = config_init['bau_list']['gun2_bau']
bau3 = config_init['bau_list']['gun3_bau']
bau = {
    "L": int(bau1),
    "M": int(bau2),
    "R": int(bau3)
}
print(bau)

sta1 = config_init['station']['gun1_sta']
sta2 = config_init['station']['gun2_sta']
sta3 = config_init['station']['gun3_sta']
# print(sta)
cmdpro1 = sta1+"."+sta1+".process"
cmd1 = sta1+"."+sta1+".gun"
cmdpro2 = sta2+"."+sta2+".process"
cmd2 = sta2+"."+sta2+".gun"
cmdpro3 = sta3+"."+sta3+".process"
cmd3 = sta3+"."+sta3+".gun"
print(cmdpro1,cmd1,cmdpro2,cmd2,cmdpro3,cmd3)
# 扫描枪1 json字段 更改以下部分即可
#                   "af10.af10.unmsn":1,
# 	                 "af10.af10.msn"
def do_post1(msn):
    client = tornado.httpclient.HTTPClient()
    host = host_get()
    recv_get = json_post(client,host,{
	        cmdpro1:True,
	        cmd1:msn
    })
    client.close()
    return recv_get
# 扫描枪2 json字段 更改以下部分即可
#                   "af10.af10.unmsn":1,
# 	                 "af10.af10.msn"
def do_post2(msn):
    client = tornado.httpclient.HTTPClient()
    host = host_get()
    recv_get = json_post(client,host,{
	        cmdpro2:True,
	        cmd2:msn
    })
    client.close()
    return recv_get
# 扫描枪3 json字段 更改以下部分即可
#                   "af10.af10.unmsn":1,
# 	                 "af10.af10.msn"
def do_post3(msn):
    client = tornado.httpclient.HTTPClient()
    host = host_get()
    recv_get = json_post(client,host,{
	        cmdpro3:True,
	        cmd3:msn
    })
    client.close()
    return recv_get

########### 以上内容需要更具实际情况更改 ############






def recv(serial):
    while True:
        data = serial.readline()
        if data == '':
            continue
        else:
            break
        sleep(2)
    return data

def json_post(http_client, host, cmd):
    try:
        body = json.dumps(cmd)
        print(body)
        # print(host)
        arg = tornado.httpclient.HTTPRequest(
                url=host,
                method="POST",
                headers={'Content-Type': 'application/json'},
                body=body)

        response = http_client.fetch(arg)
        ret = json.loads(response.body)
        # print(ret)
        return ret
    except tornado.httpclient.HTTPError as e:
        print("Http Error: " + str(e))
    except Exception as e:
        print("Error: " + str(e))

    return None



if __name__ == '__main__':
    if list["L"] != "0":
        serial1 = serial.Serial(com["L"], bau["L"], timeout=0.5)
        if serial1.isOpen() :
            print("你好 串口1打开完成")
        else :
            print("抱歉，串口1打开失败，请确认串口是否存在")

        while True:
            data = recv(serial1)
            if data != b'':
                print("扫码枪1扫码 : ", data)
                str1 = str(data, 'utf-8')
                obj = str1.replace("\r", "")
                # print(obj[0])
                a = do_post1(obj)
                print("扫码枪1回复 : ", a)

    if list["M"] != "0":
        serial2 = serial.Serial(com["M"], bau["M"], timeout=0.5)
        if serial2.isOpen() :
            print("你好 串口2打开完成")
        else :
            print("抱歉，串口2打开失败，请确认串口是否存在")

        while True:
            data2 = recv(serial2)
            if data2 != b'':
                print("扫码枪2扫码 : ", data2)
                str2 = str(data2, 'utf-8')
                b = do_post2(str2)
                print("扫码枪2回复 : ", b)
    if list["R"] != "0":
        serial3 = serial.Serial(com["R"], bau["R"], timeout=0.5)
        if serial3.isOpen():
            print("你好 串口3打开完成")
        else:
            print("抱歉，串口3打开失败，请确认串口是否存在")
        while True:
            data3 = recv(serial3)
            if data3 != b'':
                print("扫码枪3扫码 : ", data3)
                str2 = str(data3, 'utf-8')
                b = do_post3(str2)
                print("扫码枪3回复 : ", b)





