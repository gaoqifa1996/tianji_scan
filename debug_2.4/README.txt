v2.4 尝试解决短时间扫码枪重复扫描，内容重叠问题（需测试可行性） --2020-5-14

v2.3 新增log退出日志，记录退出

v2.2 变动微电阻测试结果读取线程与气密性测试结果线程
	微电阻测试不受控制，测试完成，以post方式如下JSON包发送到【url】节点下的 mes_urladd地址
	{
    	“station.station.process”: True,    	//固定字段
     	 "station.station.resist":  "xxx"    ,        	//微电阻测试结果值
	“station.station.resistover”:1	//测试完成标志
        }
	气密性测试受MES控制，配置【leak】节点
		sleeps字段：设置向mes读取频率，单位秒；
		line字段：设置气密设备读取客户端状态Json包中line内容
		obj：设置气密设备读取客户端状态Json包中obj内容（存在多个obj对象，使用英文逗号隔开）
	配置【stepcode】节点，leak字段 为设置的气密性测试标准字
	配置【useing_list】节点，leak字段 为设置本工位是否启用气密测试
		如使用气密测试，将com bau station 节点配置完成
	新增【url】下leak_urladd字段，为定时提交状态获取地址配置
	定时发送json包至MES，需要回复字段
		{
		"line":"line-one"  ，                 //需要可以配置
		"wsn":"op020" ，                  	//需要可以配置
		"obj":"stepcode,pid"  ，	//需要可以配置
		}
	回复内容：
		{
		"op020":{
			"stepcode":7,
			"pid":2
			}
		}
	
	测试完成json包发送到MES字段如下：
	{
 	"station.station.process":true,  	//固定字段
	 "station.station.leakpressure":"xxxx", 	//测试压力
	 "station.station.leakdate":"xxxx", 	//测试泄露值
 	"station.station.leakover":1  		//测试完成标志
 	 }









注意保持运行程序与配置文件的相对路径，不变动相对路径，否则会造成程序无法运行
相对路径示例：
	--demo
	    --config
	        --config.ini
	    --debug.exe

config.ini中字段均为固定值，配置过程，只需按需更改字段值即可，请勿对字段进行更改

[url]				//固定标签节点
urladd = http://47.96.151.120/machine     //更改为所需地址

[uesing_list]			//固定标签节点（扫码枪清单）
gun1 = 1			//是否启用1号扫码枪（注意 1启用 0不用）
gun2 = 0
gun3 = 0
leak = 0

[com_list]			//固定标签节点（扫码枪使用串口号清单）
gun1_com = COM2		//1号扫码枪串口（注意 启用枪，填写对应串口号 0 不用）
gun2_com = 0			
gun3_com = COM2

[bau_list]			//固定标签节点（扫码枪使用串口对应波特率清单）
gun1_bau = 9600
gun2_bau = 0		//1号扫码枪波特率（注意 启用枪，填写对应波特率 0 不用）
gun3_bau = 9600

[station]		//固定标签节点（本工位工位号）
gun1_sta = op010l	//请填写实际工位工位号即可（如无工位用0替代）
gun2_sta = 0
gun3_sta = op010r




对于com_list清单中值为大写加数字，且3个字段不能出现相同串口号，否则会造成串口占用导致程序崩溃
默认枪1为左、2为中、3为右，发送J送包体时，按对应枪号增加位置l、m、r

