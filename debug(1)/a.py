import serial
from time import sleep
import tornado
from tornado import httpclient
import json

def recv(serial):
    while True:
        data = serial.readline()
        if data == '':
            continue
        else:
            break
        sleep(3)
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

def host_get():
    host = "http://47.96.151.120/machine/dj/line-three"
    return host

def do_post(msn):
    client = tornado.httpclient.HTTPClient()
    host = host_get()
    recv_get = json_post(client,host,{
	        "af10.af10.unmsn":1,
	        "af10.af10.msn":msn
    })
    client.close()
    return recv_get

if __name__ == '__main__':
    serial = serial.Serial('COM3', 9600, timeout=0.5)
    serial.parity = serial.PARITY_EVEN
    if serial.isOpen() :
        print("你好 串口1打开完成")
    else :
        print("抱歉，串口1打开失败，请确认串口是否存在")

    # serial2 = serial.Serial('COM3', 9600, timeout=0.5)
    # if serial2.isOpen() :
    #     print("你好 串口2打开完成")
    # else :
    #     print("抱歉，串口2打开失败，请确认串口是否存在")

    while True:
        s = input("请输入：")
        data =recv(serial)
        # data2 = recv(serial2)
        if data != b'' :
            print("扫码枪1扫码 : ",data)
            str1=str(data,'utf-8')
            obj = str1.replace("\r","")
            # print(obj[0])
            a = do_post(obj)
            print("扫码枪1回复 : ", a)

