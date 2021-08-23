import time
from flask import Flask, request, render_template
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import serial.tools.list_ports
import webbrowser
import csv

from serial.tools.list_ports_windows import NULL

app = Flask(__name__)

# addr pipe port baudrate timeout modelvalue
setting = [250, 1, 'COM3', 19200, 1, 1]
model = [[0]*15 for _ in range(200)]  # 用來儲存各個型號的各參數使用與否(配合model.csv)
dictionary = {}  # 使用者介面所看到的字(配合interface.csv)
language_select = 1  # 1:預設英文 2:中文
reader = csv.reader(open('interface.csv', 'r'))  # 參數名稱
for row in reader:
    k, v = row
    dictionary[k] = v
i = 0
reader = csv.reader(open('model.csv', "r", encoding="utf-8"))  # 型號設定
for row in reader:
    model[i] = row
    i = i+1
    if i == 1:
        modelsize = len(row)  # 取得csv有幾個型號(用來做for迴圈)
statustest = 0  # status test

@app.errorhandler(500)
def err_handler(e):
    return 'The device not responding'

@app.route('/settings')
def settings():
    port_list = list(serial.tools.list_ports.comports())  # device port
    return render_template('settings.html', modelsize=modelsize, model=model, dictionary=dictionary, addr=setting[0], comd=setting[2], com=port_list, count=len(port_list), baud=setting[3], time=setting[4], modelvalue=setting[5])


@app.route('/settings_submit/', methods=['GET', 'POST'])
def settings_submit():
    a = int(request.form.get('addr'))
    p = request.form.get('port')
    b = int(request.form.get('baud'))
    t = int(request.form.get('time'))
    m = request.form.get('model')
    setting[0] = a
    setting[2] = p
    setting[3] = b
    setting[4] = t
    setting[5] = m
    port_list = list(serial.tools.list_ports.comports())  # device port
    return render_template('settings.html', modelsize=modelsize, model=model, dictionary=dictionary, addr=setting[0], comd=setting[2], com=port_list, count=len(port_list), baud=setting[3], time=setting[4], modelvalue=setting[5])


"""system"""


@app.route('/system')
def system():
    seti = int(setting[5])  # 要將str轉換成int才能做成index
    port_list = list(serial.tools.list_ports.comports())  # device port
    client = None

    i = 10
    d = None
    while d == None:
        # try:
        i = i-1
        # 客户机(通信方式，端口，波特率，超时)
        client = ModbusClient(
            method='rtu', port=setting[2], baudrate=setting[3], timeout=setting[4], strict=False)
        client.connect()
        d = client.socket

        if d != None:
            break
        else:
            print("retry!")
            time.sleep(1)
            if i < 0:
                break

    rr5 = client.read_holding_registers(100, 46, unit=setting[0])
    client.close()  # 連接完後要關掉
    return render_template('system.html', seti=seti, modelsize=modelsize, model=model, dictionary=dictionary, addr=setting[0], comd=setting[2], modelvalue=setting[5], com=port_list, count=len(port_list), addrchange=rr5.registers[0],  year=rr5.registers[1], mont=rr5.registers[2], dayy=rr5.registers[3], hourr=rr5.registers[4], minn=rr5.registers[5], secc=rr5.registers[6], rtcc=rr5.registers[7], deff=rr5.registers[8], rb1=rr5.registers[9], rb2=rr5.registers[10], lb1=rr5.registers[11], lb2=rr5.registers[12], lbu=rr5.registers[13], pbs=rr5.registers[14], pdm=rr5.registers[15], tel=rr5.registers[16], sil=rr5.registers[17], isl=rr5.registers[18], resl=rr5.registers[19], sta=rr5.registers[20], all=rr5.registers[21], fal=rr5.registers[22], fad=rr5.registers[23], rel1=rr5.registers[24], rel2=rr5.registers[25], rel3=rr5.registers[26], rel4=rr5.registers[27], rel5=rr5.registers[28], rel6=rr5.registers[29], rel7=rr5.registers[30], gpi1=rr5.registers[31], rr=rr5)


@app.route('/system_parameter/', methods=['GET', 'POST'])
def system_parameter():
    seti = int(setting[5])  # 要將str轉換成int才能做成index
    port_list = list(serial.tools.list_ports.comports())  # device port
    # 客户机(通信方式，端口，波特率，超时)
    client = ModbusClient(
        method='rtu', port=setting[2], baudrate=setting[3], timeout=setting[4], strict=False)
    client.connect()
    if(model[7][seti] == "1"):
        a = int(request.form.get('select46'))
        if(a != setting[0]):
            setting[0] = a
        client.write_registers(100, a, unit=setting[0])
    if(model[8][seti] == "1"):
        a = int(request.form.get('select1'))
        a = a % 100
        client.write_registers(101, a, unit=setting[0])
    if(model[9][seti] == "1"):
        a = int(request.form.get('select2'))
        client.write_registers(102, a, unit=setting[0])
    if(model[10][seti] == "1"):
        a = int(request.form.get('select3'))
        client.write_registers(103, a, unit=setting[0])
    if(model[11][seti] == "1"):
        a = int(request.form.get('select4'))
        client.write_registers(104, a, unit=setting[0])
    if(model[12][seti] == "1"):
        a = int(request.form.get('select5'))
        client.write_registers(105, a, unit=setting[0])
    if(model[13][seti] == "1"):
        a = int(request.form.get('select6'))
        client.write_registers(106, a, unit=setting[0])
    if(model[14][seti] == "1"):
        a = int(request.form.get('select7'))
        client.write_registers(107, a, unit=setting[0])
    if(model[15][seti] == "1"):
        a = int(request.form.get('select8'))
        client.write_registers(108, a, unit=setting[0])
    if(model[16][seti] == "1"):
        a = int(request.form.get('select9'))
        client.write_registers(109, a, unit=setting[0])
    if(model[17][seti] == "1"):
        a = int(request.form.get('select10'))
        client.write_registers(110, a, unit=setting[0])
    if(model[18][seti] == "1"):
        a = int(request.form.get('select11'))
        client.write_registers(111, a, unit=setting[0])
    if(model[19][seti] == "1"):
        a = int(request.form.get('select12'))
        client.write_registers(112, a, unit=setting[0])
    if(model[20][seti] == "1"):
        a = int(request.form.get('select13'))
        client.write_registers(113, a, unit=setting[0])
    if(model[21][seti] == "1"):
        a = int(request.form.get('select14'))
        client.write_registers(114, a, unit=setting[0])
    if(model[22][seti] == "1"):
        a = int(request.form.get('select15'))
        client.write_registers(115, a, unit=setting[0])
    if(model[23][seti] == "1"):
        a = int(request.form.get('select16'))
        client.write_registers(116, a, unit=setting[0])
    if(model[24][seti] == "1"):
        a = int(request.form.get('select17'))
        client.write_registers(117, a, unit=setting[0])
    if(model[25][seti] == "1"):
        a = int(request.form.get('select18'))
        client.write_registers(118, a, unit=setting[0])
    if(model[26][seti] == "1"):
        a = int(request.form.get('select19'))
        client.write_registers(119, a, unit=setting[0])
    if(model[27][seti] == "1"):
        a = int(request.form.get('select20'))
        client.write_registers(120, a, unit=setting[0])
    if(model[28][seti] == "1"):
        a = int(request.form.get('select21'))
        client.write_registers(121, a, unit=setting[0])
    if(model[29][seti] == "1"):
        a = int(request.form.get('select22'))
        client.write_registers(122, a, unit=setting[0])
    if(model[30][seti] == "1"):
        a = int(request.form.get('select23'))
        client.write_registers(123, a, unit=setting[0])
    if(model[31][seti] == "1"):
        a = int(request.form.get('select24'))
        client.write_registers(124, a, unit=setting[0])
    if(model[32][seti] == "1"):
        a = int(request.form.get('select25'))
        client.write_registers(125, a, unit=setting[0])
    if(model[33][seti] == "1"):
        a = int(request.form.get('select26'))
        client.write_registers(126, a, unit=setting[0])
    if(model[34][seti] == "1"):
        a = int(request.form.get('select27'))
        client.write_registers(127, a, unit=setting[0])
    if(model[35][seti] == "1"):
        a = int(request.form.get('select28'))
        client.write_registers(128, a, unit=setting[0])
    if(model[36][seti] == "1"):
        a = int(request.form.get('select29'))
        client.write_registers(129, a, unit=setting[0])
    if(model[37][seti] == "1"):
        a = int(request.form.get('select30'))
        client.write_registers(130, a, unit=setting[0])
    if(model[38][seti] == "1"):  # gpi1
        a = int(request.form.get('select31'))
        client.write_registers(131, a, unit=setting[0])
    if (model[39][seti] == "1"):  # gpi2
        a = int(request.form.get('select32'))
        client.write_registers(132, a, unit=setting[0])
    if (model[40][seti] == "1"):  # gpi3
        a = int(request.form.get('select33'))
        client.write_registers(133, a, unit=setting[0])
    if (model[41][seti] == "1"):  # gpi4
        a = int(request.form.get('select34'))
        client.write_registers(134, a, unit=setting[0])
    if (model[42][seti] == "1"):  # gpi5
        a = int(request.form.get('select35'))
        client.write_registers(135, a, unit=setting[0])
    if (model[43][seti] == "1"):  # gpi6
        a = int(request.form.get('select36'))
        client.write_registers(136, a, unit=setting[0])
    if (model[44][seti] == "1"):  # gpi7
        a = int(request.form.get('select37'))
        client.write_registers(137, a, unit=setting[0])
    if (model[45][seti] == "1"):  # gpi8
        a = int(request.form.get('select38'))
        client.write_registers(138, a, unit=setting[0])
    if (model[45][seti] == "1"):  # scan enabled
        a = int(request.form.get('select39'))
        client.write_registers(139, a, unit=setting[0])
    if (model[45][seti] == "1"):  # scan level
        a = int(request.form.get('select40'))
        client.write_registers(140, a, unit=setting[0])
    if (model[45][seti] == "1"):  # scan time
        a = int(request.form.get('select41'))
        client.write_registers(141, a, unit=setting[0])
    rr5 = client.read_holding_registers(100, 46, unit=setting[0])
    client.close()  # 連接完後要關掉
    return render_template('system.html', seti=seti, modelvalue=setting[5], modelsize=modelsize, model=model, dictionary=dictionary, addr=setting[0], comd=setting[2], com=port_list, count=len(port_list), addrchange=rr5.registers[0],  year=rr5.registers[1], mont=rr5.registers[2], dayy=rr5.registers[3], hourr=rr5.registers[4], minn=rr5.registers[5], secc=rr5.registers[6], rtcc=rr5.registers[7], deff=rr5.registers[8], rb1=rr5.registers[9], rb2=rr5.registers[10], lb1=rr5.registers[11], lb2=rr5.registers[12], lbu=rr5.registers[13], pbs=rr5.registers[14], pdm=rr5.registers[15], tel=rr5.registers[16], sil=rr5.registers[17], isl=rr5.registers[18], resl=rr5.registers[19], sta=rr5.registers[20], all=rr5.registers[21], fal=rr5.registers[22], fad=rr5.registers[23], rel1=rr5.registers[24], rel2=rr5.registers[25], rel3=rr5.registers[26], rel4=rr5.registers[27], rel5=rr5.registers[28], rel6=rr5.registers[29], rel7=rr5.registers[30], gpi1=rr5.registers[31])


@app.route('/system_addr/', methods=['GET', 'POST'])
def system_addr():
    a = int(request.form.get('addr'))
    setting[0] = a
    return system()


@app.route('/system_model/', methods=['GET', 'POST'])
def system_model():
    m = request.form.get('model')
    setting[5] = m
    return system()


"""smoke"""


@app.route('/smoke')
def smoke():
    seti = int(setting[5])  # 要將str轉換成int才能做成index
    port_list = list(serial.tools.list_ports.comports())  # device port
    client = None

    i = 10
    d = None
    while d == None:

        # try:
        i = i-1
        # 客户机(通信方式，端口，波特率，超时)
        client = ModbusClient(
            method='rtu', port=setting[2], baudrate=setting[3], timeout=setting[4], strict=False)
        client.connect()
        d = client.socket

        if d != None:
            break
        else:
            print("retry!")
            time.sleep(1)
            if i < 0:
                break

        # except:
        #     print("retry")
        #     time.sleep(1)

    if model[2][seti] == "1":  # 如果這個型號只有一個smoke管
        setting[1] = 1

    pipe = setting[1]
    if (pipe == 1):  # 如果是第一管

        rr5 = client.read_holding_registers(1100, 20, unit=setting[0])
    if (pipe == 2):  # 如果是第二管
        rr5 = client.read_holding_registers(2100, 20, unit=setting[0])
    if (pipe == 3):  # 如果是第三管
        rr5 = client.read_holding_registers(3100, 20, unit=setting[0])
    if (pipe == 4):  # 如果是第四管
        rr5 = client.read_holding_registers(4100, 20, unit=setting[0])

    fss = ('%.2f' % (rr5.registers[1]/1000))  # 小數點 三位 smoke full scale
    f2l = ('%.2f' % (rr5.registers[5]/1000))  # 小數點 三位 smoke fire 2 alarm value
    client.close()  # 連接完後要關掉
    return render_template('smoke.html', seti=seti, modelvalue=setting[5], pipe=pipe, modelsize=modelsize, model=model, dictionary=dictionary, addr=setting[0], comd=setting[2], com=port_list, count=len(port_list), f2l=f2l, fss=fss, sm1=(rr5.registers[12]/10), sm2=(rr5.registers[13]/10), rr=rr5)
    # except Exception as e:
    #     print("!", e)
    #     return "OK"


@app.route('/smoke_parameter/', methods=['GET', 'POST'])
def smoke_parameter():
    seti = int(setting[5])  # 要將str轉換成int才能做成index
    port_list = list(serial.tools.list_ports.comports())  # device port
    # 客户机(通信方式，端口，波特率，超时)
    client = ModbusClient(
        method='rtu', port=setting[2], baudrate=setting[3], timeout=setting[4], strict=False)
    client.connect()
    pipe = setting[1]
    if (pipe == 1):  # 如果是第一管
        if(model[53][seti] == "1"):  # zone used
            a = int(request.form.get('select1'))
            client.write_registers(1100, a, unit=setting[0])
        if(model[54][seti] == "1"):  # full scale sensitivity
            a = int(float(request.form.get('select2'))*1000)
            client.write_registers(1101, a, unit=setting[0])
        if(model[55][seti] == "1"):  # alert bargraph level
            a = int(request.form.get('select3'))
            client.write_registers(1102, a, unit=setting[0])
        if(model[56][seti] == "1"):  # action bargraph level
            a = int(request.form.get('select4'))
            client.write_registers(1103, a, unit=setting[0])
        if(model[57][seti] == "1"):  # fire 1 bargraph level
            a = int(request.form.get('select5'))
            client.write_registers(1104, a, unit=setting[0])
        if(model[58][seti] == "1"):  # fire 2 level
            a = int(float(request.form.get('select6'))*1000)  # fire2level
            client.write_registers(1105, a, unit=setting[0])
        if(model[59][seti] == "1"):  # alert delay
            a = int(request.form.get('select7'))
            client.write_registers(1106, a, unit=setting[0])
        if(model[60][seti] == "1"):  # action delay
            a = int(request.form.get('select8'))
            client.write_registers(1107, a, unit=setting[0])
        if(model[61][seti] == "1"):  # fire 1 delay
            a = int(request.form.get('select9'))
            client.write_registers(1108, a, unit=setting[0])
        if(model[62][seti] == "1"):  # fire 2 delay
            a = int(request.form.get('select10'))
            client.write_registers(1109, a, unit=setting[0])

        if(model[64][seti] == "1"):  # SSL Mean Period
            a = int(request.form.get('select12'))
            client.write_registers(1111, a, unit=setting[0])
        if(model[65][seti] == "1"):  # Sensitivity Mode 1
            a = int(float(request.form.get('select13'))*10)
            client.write_registers(1112, a, unit=setting[0])
        if(model[66][seti] == "1"):  # Sensitivity Mode 2
            a = int(float(request.form.get('select14'))*10)
            client.write_registers(1113, a, unit=setting[0])
        if(model[67][seti] == "1"):  # Smoke Log Enable
            a = int(request.form.get('select15'))
            client.write_registers(1114, a, unit=setting[0])
        if(model[68][seti] == "1"):  # Smoke Log Mode
            a = int(request.form.get('select16'))
            client.write_registers(1115, a, unit=setting[0])
        if(model[69][seti] == "1"):  # Smoke Log Change/Rate
            a = int(request.form.get('select17'))
            client.write_registers(1116, a, unit=setting[0])
        if(model[70][seti] == "1"):  # Smoke ABS Log Enable
            a = int(request.form.get('select18'))
            client.write_registers(1117, a, unit=setting[0])
        if(model[71][seti] == "1"):  # Smoke ABS Log Mode
            a = int(request.form.get('select19'))
            client.write_registers(1118, a, unit=setting[0])
        if(model[72][seti] == "1"):  # Smoke ABS Log Change/Rate
            a = int(request.form.get('select20'))
            client.write_registers(1119, a, unit=setting[0])
    if (pipe == 2):  # 如果是第2管
        if (model[53][seti] == "1"):  # zone used
            a = int(request.form.get('select1'))
            client.write_registers(2100, a, unit=setting[0])
        if (model[54][seti] == "1"):  # full scale sensitivity
            a = int(float(request.form.get('select2')) * 1000)
            client.write_registers(2101, a, unit=setting[0])
        if (model[55][seti] == "1"):  # alert bargraph level
            a = int(request.form.get('select3'))
            client.write_registers(2102, a, unit=setting[0])
        if (model[56][seti] == "1"):  # action bargraph level
            a = int(request.form.get('select4'))
            client.write_registers(2103, a, unit=setting[0])
        if (model[57][seti] == "1"):  # fire 1 bargraph level
            a = int(request.form.get('select5'))
            client.write_registers(2104, a, unit=setting[0])
        if (model[58][seti] == "1"):  # fire 2 level
            a = int(float(request.form.get('select6')) * 1000)  # fire2level
            client.write_registers(2105, a, unit=setting[0])
        if (model[59][seti] == "1"):  # alert delay
            a = int(request.form.get('select7'))
            client.write_registers(2106, a, unit=setting[0])
        if (model[60][seti] == "1"):  # action delay
            a = int(request.form.get('select8'))
            client.write_registers(2107, a, unit=setting[0])
        if (model[61][seti] == "1"):  # fire 1 delay
            a = int(request.form.get('select9'))
            client.write_registers(2108, a, unit=setting[0])
        if (model[62][seti] == "1"):  # fire 2 delay
            a = int(request.form.get('select10'))
            client.write_registers(2109, a, unit=setting[0])

        if (model[64][seti] == "1"):  # SSL Mean Period
            a = int(request.form.get('select12'))
            client.write_registers(2111, a, unit=setting[0])
        if (model[65][seti] == "1"):  # Sensitivity Mode 1
            a = int(float(request.form.get('select13')) * 10)
            client.write_registers(2112, a, unit=setting[0])
        if (model[66][seti] == "1"):  # Sensitivity Mode 2
            a = int(float(request.form.get('select14')) * 10)
            client.write_registers(2113, a, unit=setting[0])
        if (model[67][seti] == "1"):  # Smoke Log Enable
            a = int(request.form.get('select15'))
            client.write_registers(2114, a, unit=setting[0])
        if (model[68][seti] == "1"):  # Smoke Log Mode
            a = int(request.form.get('select16'))
            client.write_registers(2115, a, unit=setting[0])
        if (model[69][seti] == "1"):  # Smoke Log Change/Rate
            a = int(request.form.get('select17'))
            client.write_registers(2116, a, unit=setting[0])
        if (model[70][seti] == "1"):  # Smoke ABS Log Enable
            a = int(request.form.get('select18'))
            client.write_registers(2117, a, unit=setting[0])
        if (model[71][seti] == "1"):  # Smoke ABS Log Mode
            a = int(request.form.get('select19'))
            client.write_registers(2118, a, unit=setting[0])
        if (model[72][seti] == "1"):  # Smoke ABS Log Change/Rate
            a = int(request.form.get('select20'))
            client.write_registers(2119, a, unit=setting[0])
    if (pipe == 3):  # 如果是第3管
        if (model[53][seti] == "1"):  # zone used
            a = int(request.form.get('select1'))
            client.write_registers(3100, a, unit=setting[0])
        if (model[54][seti] == "1"):  # full scale sensitivity
            a = int(float(request.form.get('select2')) * 1000)
            client.write_registers(3101, a, unit=setting[0])
        if (model[55][seti] == "1"):  # alert bargraph level
            a = int(request.form.get('select3'))
            client.write_registers(3102, a, unit=setting[0])
        if (model[56][seti] == "1"):  # action bargraph level
            a = int(request.form.get('select4'))
            client.write_registers(3103, a, unit=setting[0])
        if (model[57][seti] == "1"):  # fire 1 bargraph level
            a = int(request.form.get('select5'))
            client.write_registers(3104, a, unit=setting[0])
        if (model[58][seti] == "1"):  # fire 2 level
            a = int(float(request.form.get('select6')) * 1000)  # fire2level
            client.write_registers(3105, a, unit=setting[0])
        if (model[59][seti] == "1"):  # alert delay
            a = int(request.form.get('select7'))
            client.write_registers(3106, a, unit=setting[0])
        if (model[60][seti] == "1"):  # action delay
            a = int(request.form.get('select8'))
            client.write_registers(3107, a, unit=setting[0])
        if (model[61][seti] == "1"):  # fire 1 delay
            a = int(request.form.get('select9'))
            client.write_registers(3108, a, unit=setting[0])
        if (model[62][seti] == "1"):  # fire 2 delay
            a = int(request.form.get('select10'))
            client.write_registers(3109, a, unit=setting[0])

        if (model[64][seti] == "1"):  # SSL Mean Period
            a = int(request.form.get('select12'))
            client.write_registers(3111, a, unit=setting[0])
        if (model[65][seti] == "1"):  # Sensitivity Mode 1
            a = int(float(request.form.get('select13')) * 10)
            client.write_registers(3112, a, unit=setting[0])
        if (model[66][seti] == "1"):  # Sensitivity Mode 2
            a = int(float(request.form.get('select14')) * 10)
            client.write_registers(3113, a, unit=setting[0])
        if (model[67][seti] == "1"):  # Smoke Log Enable
            a = int(request.form.get('select15'))
            client.write_registers(3114, a, unit=setting[0])
        if (model[68][seti] == "1"):  # Smoke Log Mode
            a = int(request.form.get('select16'))
            client.write_registers(3115, a, unit=setting[0])
        if (model[69][seti] == "1"):  # Smoke Log Change/Rate
            a = int(request.form.get('select17'))
            client.write_registers(3116, a, unit=setting[0])
        if (model[70][seti] == "1"):  # Smoke ABS Log Enable
            a = int(request.form.get('select18'))
            client.write_registers(3117, a, unit=setting[0])
        if (model[71][seti] == "1"):  # Smoke ABS Log Mode
            a = int(request.form.get('select19'))
            client.write_registers(3118, a, unit=setting[0])
        if (model[72][seti] == "1"):  # Smoke ABS Log Change/Rate
            a = int(request.form.get('select20'))
            client.write_registers(3119, a, unit=setting[0])
    if (pipe == 4):  # 如果是第4管
        if (model[53][seti] == "1"):  # zone used
            a = int(request.form.get('select1'))
            client.write_registers(4100, a, unit=setting[0])
        if (model[54][seti] == "1"):  # full scale sensitivity
            a = int(float(request.form.get('select2')) * 1000)
            client.write_registers(4101, a, unit=setting[0])
        if (model[55][seti] == "1"):  # alert bargraph level
            a = int(request.form.get('select3'))
            client.write_registers(4102, a, unit=setting[0])
        if (model[56][seti] == "1"):  # action bargraph level
            a = int(request.form.get('select4'))
            client.write_registers(4103, a, unit=setting[0])
        if (model[57][seti] == "1"):  # fire 1 bargraph level
            a = int(request.form.get('select5'))
            client.write_registers(4104, a, unit=setting[0])
        if (model[58][seti] == "1"):  # fire 2 level
            a = int(float(request.form.get('select6')) * 1000)  # fire2level
            client.write_registers(4105, a, unit=setting[0])
        if (model[59][seti] == "1"):  # alert delay
            a = int(request.form.get('select7'))
            client.write_registers(4106, a, unit=setting[0])
        if (model[60][seti] == "1"):  # action delay
            a = int(request.form.get('select8'))
            client.write_registers(4107, a, unit=setting[0])
        if (model[61][seti] == "1"):  # fire 1 delay
            a = int(request.form.get('select9'))
            client.write_registers(4108, a, unit=setting[0])
        if (model[62][seti] == "1"):  # fire 2 delay
            a = int(request.form.get('select10'))
            client.write_registers(4109, a, unit=setting[0])

        if (model[64][seti] == "1"):  # SSL Mean Period
            a = int(request.form.get('select12'))
            client.write_registers(4111, a, unit=setting[0])
        if (model[65][seti] == "1"):  # Sensitivity Mode 1
            a = int(float(request.form.get('select13')) * 10)
            client.write_registers(4112, a, unit=setting[0])
        if (model[66][seti] == "1"):  # Sensitivity Mode 2
            a = int(float(request.form.get('select14')) * 10)
            client.write_registers(4113, a, unit=setting[0])
        if (model[67][seti] == "1"):  # Smoke Log Enable
            a = int(request.form.get('select15'))
            client.write_registers(4114, a, unit=setting[0])
        if (model[68][seti] == "1"):  # Smoke Log Mode
            a = int(request.form.get('select16'))
            client.write_registers(4115, a, unit=setting[0])
        if (model[69][seti] == "1"):  # Smoke Log Change/Rate
            a = int(request.form.get('select17'))
            client.write_registers(4116, a, unit=setting[0])
        if (model[70][seti] == "1"):  # Smoke ABS Log Enable
            a = int(request.form.get('select18'))
            client.write_registers(4117, a, unit=setting[0])
        if (model[71][seti] == "1"):  # Smoke ABS Log Mode
            a = int(request.form.get('select19'))
            client.write_registers(4118, a, unit=setting[0])
        if (model[72][seti] == "1"):  # Smoke ABS Log Change/Rate
            a = int(request.form.get('select20'))
            client.write_registers(4119, a, unit=setting[0])
    client.close()  # 連接完後要關掉
    return smoke()


@app.route('/smoke_addr/', methods=['GET', 'POST'])
def smoke_addr():
    a = int(request.form.get('addr'))
    setting[0] = a
    return smoke()


@app.route('/smoke_model/', methods=['GET', 'POST'])
def smoke_model():
    m = request.form.get('model')
    setting[5] = m
    return smoke()


@app.route('/smoke_pipe/', methods=['GET', 'POST'])
def smoke_pipe():
    a = int(request.form.get('pipe'))
    setting[1] = a
    return smoke()


"""flow"""


@app.route('/flow')  # 顯示數值
def flow():
    seti = int(setting[5])  # 要將str轉換成int才能做成index
    port_list = list(serial.tools.list_ports.comports())  # device port
    client = None

    i = 10
    d = None
    while d == None:

        # try:
        i = i-1
        # 客户机(通信方式，端口，波特率，超时)
        client = ModbusClient(
            method='rtu', port=setting[2], baudrate=setting[3], timeout=setting[4], strict=False)
        client.connect()
        d = client.socket

        if d != None:
            break
        else:
            print("retry!")
            time.sleep(1)
            if i < 0:
                break

    if model[3][seti] == "1":  # 如果這個型號只有一個flow管
        setting[1] = 1

    pipe = setting[1]
    if (pipe == 1):  # 如果是第一管
        rr5 = client.read_holding_registers(1120, 14, unit=setting[0])  # flow
    if (pipe == 2):  # 如果是第二管
        rr5 = client.read_holding_registers(2120, 14, unit=setting[0])
    if (pipe == 3):  # 如果是第三管
        rr5 = client.read_holding_registers(3120, 14, unit=setting[0])
    if (pipe == 4):  # 如果是第四管
        rr5 = client.read_holding_registers(4120, 14, unit=setting[0])
    client.close()  # 連接完後要關掉

    return render_template('flow.html', seti=seti, modelvalue=setting[5], modelsize=modelsize, model=model, dictionary=dictionary, pipe=pipe, addr=setting[0], comd=setting[2], com=port_list, count=len(port_list), pu=rr5.registers[0], pfh=rr5.registers[1], pfl=rr5.registers[2], pfs=rr5.registers[3], fs=rr5.registers[4], an=rr5.registers[5], fn=rr5.registers[6], fle=rr5.registers[7], flm=rr5.registers[8], flcr=rr5.registers[9], frle=rr5.registers[10], frlm=rr5.registers[11], frlcr=rr5.registers[12])


@app.route('/flow_parameter/', methods=['GET', 'POST'])
def flow_parameter():
    seti = int(setting[5])  # 要將str轉換成int才能做成index
    port_list = list(serial.tools.list_ports.comports())  # device port
    # 客户机(通信方式，端口，波特率，超时)
    client = ModbusClient(
        method='rtu', port=setting[2], baudrate=setting[3], timeout=setting[4], strict=False)
    client.connect()
    pipe = setting[1]
    if (pipe == 1):  # 如果是第一管
        if(model[73][seti] == "1"):
            a = int(request.form.get('select1'))
            client.write_registers(1120, a, unit=setting[0])
        if(model[74][seti] == "1"):
            a = int(request.form.get('select2'))
            client.write_registers(1121, a, unit=setting[0])
        if(model[75][seti] == "1"):
            a = int(request.form.get('select3'))
            client.write_registers(1122, a, unit=setting[0])
        if(model[76][seti] == "1"):
            a = int(request.form.get('select4'))
            client.write_registers(1123, a, unit=setting[0])
        if(model[77][seti] == "1"):
            a = int(request.form.get('select5'))
            client.write_registers(1124, a, unit=setting[0])
        if(model[78][seti] == "1"):
            a = int(request.form.get('select6'))
            client.write_registers(1125, a, unit=setting[0])
        if(model[79][seti] == "1"):
            a = int(request.form.get('select7'))
            client.write_registers(1126, a, unit=setting[0])
        if(model[80][seti] == "1"):
            a = int(request.form.get('select8'))
            client.write_registers(1127, a, unit=setting[0])
        if(model[81][seti] == "1"):
            a = int(request.form.get('select9'))
            client.write_registers(1128, a, unit=setting[0])
        if(model[82][seti] == "1"):
            a = int(request.form.get('select10'))
            client.write_registers(1129, a, unit=setting[0])
        if(model[83][seti] == "1"):
            a = int(request.form.get('select11'))
            client.write_registers(1130, a, unit=setting[0])
        if(model[84][seti] == "1"):
            a = int(request.form.get('select12'))
            client.write_registers(1131, a, unit=setting[0])
        if(model[85][seti] == "1"):
            a = int(request.form.get('select13'))
            client.write_registers(1132, a, unit=setting[0])
    if (pipe == 2):  # 如果是第二管
        if(model[73][seti] == "1"):
            a = int(request.form.get('select1'))
            client.write_registers(2120, a, unit=setting[0])
        if(model[74][seti] == "1"):
            a = int(request.form.get('select2'))
            client.write_registers(2121, a, unit=setting[0])
        if(model[75][seti] == "1"):
            a = int(request.form.get('select3'))
            client.write_registers(2122, a, unit=setting[0])
        if(model[76][seti] == "1"):
            a = int(request.form.get('select4'))
            client.write_registers(2123, a, unit=setting[0])
        if(model[77][seti] == "1"):
            a = int(request.form.get('select5'))
            client.write_registers(2124, a, unit=setting[0])
        if(model[78][seti] == "1"):
            a = int(request.form.get('select6'))
            client.write_registers(2125, a, unit=setting[0])
        if(model[79][seti] == "1"):
            a = int(request.form.get('select7'))
            client.write_registers(2126, a, unit=setting[0])
        if(model[80][seti] == "1"):
            a = int(request.form.get('select8'))
            client.write_registers(2127, a, unit=setting[0])
        if(model[81][seti] == "1"):
            a = int(request.form.get('select9'))
            client.write_registers(2128, a, unit=setting[0])
        if(model[82][seti] == "1"):
            a = int(request.form.get('select10'))
            client.write_registers(2129, a, unit=setting[0])
        if(model[83][seti] == "1"):
            a = int(request.form.get('select11'))
            client.write_registers(2130, a, unit=setting[0])
        if(model[84][seti] == "1"):
            a = int(request.form.get('select12'))
            client.write_registers(2131, a, unit=setting[0])
        if(model[85][seti] == "1"):
            a = int(request.form.get('select13'))
            client.write_registers(2132, a, unit=setting[0])
    if (pipe == 3):  # 如果是第三管
        if(model[73][seti] == "1"):
            a = int(request.form.get('select1'))
            client.write_registers(3120, a, unit=setting[0])
        if(model[74][seti] == "1"):
            a = int(request.form.get('select2'))
            client.write_registers(3121, a, unit=setting[0])
        if(model[75][seti] == "1"):
            a = int(request.form.get('select3'))
            client.write_registers(3122, a, unit=setting[0])
        if(model[76][seti] == "1"):
            a = int(request.form.get('select4'))
            client.write_registers(3123, a, unit=setting[0])
        if(model[77][seti] == "1"):
            a = int(request.form.get('select5'))
            client.write_registers(3124, a, unit=setting[0])
        if(model[78][seti] == "1"):
            a = int(request.form.get('select6'))
            client.write_registers(3125, a, unit=setting[0])
        if(model[79][seti] == "1"):
            a = int(request.form.get('select7'))
            client.write_registers(3126, a, unit=setting[0])
        if(model[80][seti] == "1"):
            a = int(request.form.get('select8'))
            client.write_registers(3127, a, unit=setting[0])
        if(model[81][seti] == "1"):
            a = int(request.form.get('select9'))
            client.write_registers(3128, a, unit=setting[0])
        if(model[82][seti] == "1"):
            a = int(request.form.get('select10'))
            client.write_registers(3129, a, unit=setting[0])
        if(model[83][seti] == "1"):
            a = int(request.form.get('select11'))
            client.write_registers(3130, a, unit=setting[0])
        if(model[84][seti] == "1"):
            a = int(request.form.get('select12'))
            client.write_registers(3131, a, unit=setting[0])
        if(model[85][seti] == "1"):
            a = int(request.form.get('select13'))
            client.write_registers(3132, a, unit=setting[0])
    if (pipe == 4):  # 如果是第四管
        if(model[73][seti] == "1"):
            a = int(request.form.get('select1'))
            client.write_registers(4120, a, unit=setting[0])
        if(model[74][seti] == "1"):
            a = int(request.form.get('select2'))
            client.write_registers(4121, a, unit=setting[0])
        if(model[75][seti] == "1"):
            a = int(request.form.get('select3'))
            client.write_registers(4122, a, unit=setting[0])
        if(model[76][seti] == "1"):
            a = int(request.form.get('select4'))
            client.write_registers(4123, a, unit=setting[0])
        if(model[77][seti] == "1"):
            a = int(request.form.get('select5'))
            client.write_registers(4124, a, unit=setting[0])
        if(model[78][seti] == "1"):
            a = int(request.form.get('select6'))
            client.write_registers(4125, a, unit=setting[0])
        if(model[79][seti] == "1"):
            a = int(request.form.get('select7'))
            client.write_registers(4126, a, unit=setting[0])
        if(model[80][seti] == "1"):
            a = int(request.form.get('select8'))
            client.write_registers(4127, a, unit=setting[0])
        if(model[81][seti] == "1"):
            a = int(request.form.get('select9'))
            client.write_registers(4128, a, unit=setting[0])
        if(model[82][seti] == "1"):
            a = int(request.form.get('select10'))
            client.write_registers(4129, a, unit=setting[0])
        if(model[83][seti] == "1"):
            a = int(request.form.get('select11'))
            client.write_registers(4130, a, unit=setting[0])
        if(model[84][seti] == "1"):
            a = int(request.form.get('select12'))
            client.write_registers(4131, a, unit=setting[0])
        if(model[85][seti] == "1"):
            a = int(request.form.get('select13'))
            client.write_registers(4132, a, unit=setting[0])
    client.close()  # 連接完後要關掉
    return flow()


@app.route('/flow_addr/', methods=['GET', 'POST'])
def flow_addr():
    a = int(request.form.get('addr'))
    setting[0] = a
    return flow()


@app.route('/flow_model/', methods=['GET', 'POST'])
def flow_model():
    m = request.form.get('model')
    setting[5] = m
    return flow()


@app.route('/flow_pipe/', methods=['GET', 'POST'])
def flow_pipe():
    a = int(request.form.get('pipe'))
    setting[1] = a
    return flow()


"""filter"""


@app.route('/filter')  # 顯示數值
def filter():
    seti = int(setting[5])  # 要將str轉換成int才能做成index
    port_list = list(serial.tools.list_ports.comports())  # device port
    client = None

    i = 10
    d = None
    while d == None:

        # try:
        i = i-1
        # 客户机(通信方式，端口，波特率，超时)
        client = ModbusClient(
            method='rtu', port=setting[2], baudrate=setting[3], timeout=setting[4], strict=False)
        client.connect()
        d = client.socket

        if d != None:
            break
        else:
            print("retry!")
            time.sleep(1)
            if i < 0:
                break

    rr5 = client.read_holding_registers(1133, 2, unit=setting[0])
    rr6 = client.read_holding_registers(1007, 3, unit=setting[0])
    client.close()  # 連接完後要關掉
    return render_template('filter.html', seti=seti, modelvalue=setting[5], modelsize=modelsize, model=model, dictionary=dictionary, addr=setting[0], comd=setting[2], com=port_list, count=len(port_list), fu=rr5.registers[0], nf=rr5.registers[1], year=rr6.registers[0], month=rr6.registers[1], day=rr6.registers[2])


@app.route('/filter_parameter/', methods=['GET', 'POST'])
def filter_parameter():
    seti = int(setting[5])  # 要將str轉換成int才能做成index
    port_list = list(serial.tools.list_ports.comports())  # device port
    # 客户机(通信方式，端口，波特率，超时)
    client = ModbusClient(
        method='rtu', port=setting[2], baudrate=setting[3], timeout=setting[4], strict=False)
    client.connect()
    if(model[86][seti] == "1"):
        a = int(request.form.get('select1'))
        client.write_registers(1133, a, unit=setting[0])
    if(model[87][seti] == "1"):
        a = int(request.form.get('select2'))
        client.write_registers(1134, a, unit=setting[0])
    rr5 = client.read_holding_registers(1133, 2, unit=setting[0])  # filter
    client.close()  # 連接完後要關掉
    return render_template('filter.html', seti=seti, modelvalue=setting[5], modelsize=modelsize, model=model, dictionary=dictionary, addr=setting[0], comd=setting[2], com=port_list, count=len(port_list), fu=rr5.registers[0], nf=rr5.registers[1])


@app.route('/filter_addr/', methods=['GET', 'POST'])
def filter_addr():
    a = int(request.form.get('addr'))
    setting[0] = a
    return filter()


@app.route('/filter_model/', methods=['GET', 'POST'])
def filter_model():
    m = request.form.get('model')
    setting[5] = m
    return filter()


"""status"""


@app.route('/status')
def status():  # 連接裝置 + 讀&寫檔

    try:
        seti = int(setting[5])  # 要將str轉換成int才能做成index
        port_list = list(serial.tools.list_ports.comports())  # device port
        client = None

        i = 10
        d = None
        while d == None:
            i = i-1
            # 客户机(通信方式，端口，波特率，超时)
            client = ModbusClient(
                method='rtu', port=setting[2], baudrate=setting[3], timeout=setting[4], strict=False)
            client.connect()
            d = client.socket

            if d != None:
                break
            else:
                print("retry!")
                time.sleep(1)
                if i < 0:
                    break

        rr1 = client.read_holding_registers(1000, 18, unit=setting[0])
        rr2 = client.read_holding_registers(2000, 18, unit=setting[0])
        rr3 = client.read_holding_registers(3000, 18, unit=setting[0])
        rr4 = client.read_holding_registers(4000, 18, unit=setting[0])
        rr5 = client.read_holding_registers(17, 22, unit=setting[0])
        zu = [0] * 4  # smoke
        pu = [0] * 4  # flow
        # zone used (smoke) 判斷此zone是否有使用，無就將值歸0
        pipe1zu = client.read_holding_registers(1100, 1, unit=setting[0])
        zu[0] = pipe1zu.registers[0]
        pipe1pu = client.read_holding_registers(
            1120, 1, unit=setting[0])  # pipe used (flow)
        pu[0] = pipe1pu.registers[0]
        if model[2][seti] == "4":  # smoke四管
            pipe2zu = client.read_holding_registers(
                2100, 1, unit=setting[0])  # zone used (smoke)
            zu[1] = pipe2zu.registers[0]
            pipe3zu = client.read_holding_registers(
                3100, 1, unit=setting[0])  # zone used (smoke)
            zu[2] = pipe3zu.registers[0]
            pipe4zu = client.read_holding_registers(
                4100, 1, unit=setting[0])  # zone used (smoke)
            zu[3] = pipe4zu.registers[0]
        if model[3][seti] == "4":  # flow四管
            pipe2pu = client.read_holding_registers(
                2120, 1, unit=setting[0])  # pipe used (flow)
            pu[1] = pipe2pu.registers[0]
            pipe3pu = client.read_holding_registers(
                3120, 1, unit=setting[0])  # pipe used (flow)
            pu[2] = pipe3pu.registers[0]
            pipe4pu = client.read_holding_registers(
                4120, 1, unit=setting[0])  # pipe used (flow)
            pu[3] = pipe4pu.registers[0]

        devi = [0]*16
        # q2000讀取錯誤的位置跟其他型號不一樣 要讀協定17(這裡的放在device condition格子)
        if rr5.registers[0] != 0:
            a = bin(rr5.registers[0] & 1)  # detection
            if a == bin(1):  # FIRE2
                devi[0] = 1
            a = bin(rr5.registers[0] & 2)
            if a == bin(2):  # FIRE1
                devi[1] = 1
            a = bin(rr5.registers[0] & 4)
            if a == bin(4):  # ACTION
                devi[2] = 1
            a = bin(rr5.registers[0] & 8)
            if a == bin(8):  # ALERT
                devi[3] = 1
            a = bin(rr5.registers[0] & 16)
            if a == bin(16):  # Aux. Sensor Alarm 1
                devi[4] = 1
            a = bin(rr5.registers[0] & 32)
            if a == bin(32):  # Aux. Sensor Alarm 2
                devi[5] = 1
            a = bin(rr5.registers[0] & 64)
            if a == bin(64):  # Isolate
                devi[6] = 1
            a = bin(rr5.registers[0] & 128)
            if a == bin(128):  # General Fault.
                devi[7] = 1
            a = bin(rr5.registers[0] & 256)
            if a == bin(256):  # Detection Fault.
                devi[8] = 1
            a = bin(rr5.registers[0] & 512)
            if a == bin(512):  # Flow Fault.
                devi[9] = 1
            a = bin(rr5.registers[0] & 1024)
            if a == bin(1024):  # System Fault.
                devi[10] = 1
            a = bin(rr5.registers[0] & 2048)
            if a == bin(2048):  # Aux. Sensor Fault.
                devi[11] = 1
            a = bin(rr5.registers[0] & 4096)
            if a == bin(4096):  # reserved
                devi[12] = 1
            a = bin(rr5.registers[0] & 8192)
            if a == bin(8192):  # reserved
                devi[13] = 1
            a = bin(rr5.registers[0] & 16384)
            if a == bin(16384):  # Smoke Learn in progress...
                devi[14] = 1
            a = bin(rr5.registers[0] & 32768)
            if a == bin(32768):  # Flow Normalization in progress...
                devi[15] = 1

        bi = [0]*64
        # DetectCondition的各個狀態是由二進位數字儲存 所以要用陣列判斷各個狀態是否有被開啟 1000
        a = bin(rr1.registers[0] & 1)
        if a == bin(1):  # FIRE2
            bi[0] = 1
        a = bin(rr1.registers[0] & 2)
        if a == bin(2):  # FIRE1
            bi[1] = 1
        a = bin(rr1.registers[0] & 4)
        if a == bin(4):  # ACTION
            bi[2] = 1
        a = bin(rr1.registers[0] & 8)
        if a == bin(8):  # ALERT
            bi[3] = 1
        a = bin(rr1.registers[0] & 16)
        if a == bin(16):  # Aux. Sensor Alarm 1
            bi[4] = 1
        a = bin(rr1.registers[0] & 32)
        if a == bin(32):  # Aux. Sensor Alarm 2
            bi[5] = 1
        a = bin(rr1.registers[0] & 64)
        if a == bin(64):  # Isolate
            bi[6] = 1
        a = bin(rr1.registers[0] & 128)
        if a == bin(128):
            bi[7] = 1
        a = bin(rr1.registers[0] & 256)
        if a == bin(256):
            bi[8] = 1
        a = bin(rr1.registers[0] & 512)
        if a == bin(512):
            bi[9] = 1
        a = bin(rr1.registers[0] & 1024)
        if a == bin(1024):  # System Fault.
            bi[10] = 1
        a = bin(rr1.registers[0] & 2048)
        if a == bin(2048):  # Aux. Sensor Fault.
            bi[11] = 1
        # a = bin(rr1.registers[0] & 4096)
        # if a == bin(4096): #reserved
            # bi[12] = 1
        # a = bin(rr1.registers[0] & 8192)
        # if a == bin(8192): #reserved
            # bi[13] = 1
        a = bin(rr1.registers[0] & 16384)
        if a == bin(16384):  # Smoke Learn in progress...
            bi[14] = 1
        a = bin(rr1.registers[0] & 32768)
        if a == bin(32768):  # Flow Normalization in progress...
            bi[15] = 1

        if model[3][seti] == "4":  # flow四管(有七個不用分管)
            if pu[1] == 1:  # 如果管2有開啟
                # a = bin(rr2.registers[0] & 1)
                # if a == bin(1):  # FIRE2
                # bi[16] = 1
                # a = bin(rr2.registers[0] & 2)
                # if a == bin(2):  # FIRE1
                # bi[17] = 1
                # a = bin(rr2.registers[0] & 4)
                # if a == bin(4):  # ACTION
                # bi[18] = 1
                # a = bin(rr2.registers[0] & 8)
                # if a == bin(8): #ALERT
                # bi[19] = 1
                a = bin(rr2.registers[0] & 16)
                if a == bin(16):  # Aux. Sensor Alarm 1
                    bi[20] = 1
                a = bin(rr2.registers[0] & 32)
                if a == bin(32):  # Aux. Sensor Alarm 2
                    bi[21] = 1
                # a = bin(rr2.registers[0] & 64)
                # if a == bin(64): #Isolate
                    # bi[22] = 1
                a = bin(rr2.registers[0] & 128)
                if a == bin(128):
                    bi[23] = 1
                a = bin(rr2.registers[0] & 256)
                if a == bin(256):
                    bi[24] = 1
                a = bin(rr2.registers[0] & 512)
                if a == bin(512):
                    bi[25] = 1
                # a = bin(rr2.registers[0] & 1024)
                # if a == bin(1024): #System Fault.
                    # bi[26] = 1
                a = bin(rr2.registers[0] & 2048)
                if a == bin(2048):  # Aux. Sensor Fault.
                    bi[27] = 1
                # a = bin(rr2.registers[0] & 4096)
                # if a == bin(4096): #reserved
                    # bi[28] = 1
                # a = bin(rr2.registers[0] & 8192)
                # if a == bin(8192): #reserved
                    # bi[29] = 1
                # a = bin(rr2.registers[0] & 16384)
                # if a == bin(16384): #Smoke Learn in progress...
                    # bi[30] = 1
                a = bin(rr2.registers[0] & 32768)
                if a == bin(32768):  # Flow Normalization in progress...
                    bi[31] = 1
            if pu[2] == 1:  # 如果管3有開啟
                # a = bin(rr3.registers[0] & 1)
                # if a == bin(1):  # FIRE2
                # bi[32] = 1
                # a = bin(rr3.registers[0] & 2)
                # if a == bin(2):  # FIRE1
                # bi[33] = 1
                # a = bin(rr3.registers[0] & 4)
                # if a == bin(4):  # ACTION
                # bi[34] = 1
                # a = bin(rr3.registers[0] & 8)
                # if a == bin(8): #ALERT
                # bi[35] = 1
                a = bin(rr3.registers[0] & 16)
                if a == bin(16):  # Aux. Sensor Alarm 1
                    bi[36] = 1
                a = bin(rr3.registers[0] & 32)
                if a == bin(32):  # Aux. Sensor Alarm 2
                    bi[37] = 1
                # a = bin(rr3.registers[0] & 64)
                # if a == bin(64): #Isolate
                    # bi[38] = 1
                a = bin(rr3.registers[0] & 128)
                if a == bin(128):
                    bi[39] = 1
                a = bin(rr3.registers[0] & 256)
                if a == bin(256):
                    bi[40] = 1
                a = bin(rr3.registers[0] & 512)
                if a == bin(512):
                    bi[41] = 1
                a = bin(rr3.registers[0] & 1024)
                if a == bin(1024):  # System Fault.
                    bi[42] = 1
                a = bin(rr3.registers[0] & 2048)
                if a == bin(2048):  # Aux. Sensor Fault.
                    bi[43] = 1
                # a = bin(rr3.registers[0] & 4096)
                # if a == bin(4096): #reserved
                    # bi[44] = 1
                # a = bin(rr3.registers[0] & 8192)
                # if a == bin(8192): #reserved
                    # bi[45] = 1
                # a = bin(rr3.registers[0] & 16384)
                # if a == bin(16384): #Smoke Learn in progress...
                    # bi[46] = 1
                a = bin(rr3.registers[0] & 32768)
                if a == bin(32768):  # Flow Normalization in progress...
                    bi[47] = 1
            if pu[3] == 1:  # 如果管4有開啟
                # a = bin(rr4.registers[0] & 1)
                # if a == bin(1):  # FIRE2
                # bi[48] = 1
                # a = bin(rr4.registers[0] & 2)
                # if a == bin(2):  # FIRE1
                # bi[49] = 1
                # a = bin(rr4.registers[0] & 4)
                # if a == bin(4):  # ACTION
                # bi[50] = 1
                # a = bin(rr4.registers[0] & 8)
                # if a == bin(8): #ALERT
                # bi[51] = 1
                a = bin(rr4.registers[0] & 16)
                if a == bin(16):  # Aux. Sensor Alarm 1
                    bi[52] = 1
                a = bin(rr4.registers[0] & 32)
                if a == bin(32):  # Aux. Sensor Alarm 2
                    bi[53] = 1
                # a = bin(rr4.registers[0] & 64)
                # if a == bin(64): #Isolate
                    # bi[54] = 1
                a = bin(rr4.registers[0] & 128)
                if a == bin(128):
                    bi[55] = 1
                a = bin(rr4.registers[0] & 256)
                if a == bin(256):
                    bi[56] = 1
                a = bin(rr4.registers[0] & 512)
                if a == bin(512):
                    bi[57] = 1
                # a = bin(rr4.registers[0] & 1024)
                # if a == bin(1024): #System Fault.
                    # bi[58] = 1
                a = bin(rr4.registers[0] & 2048)
                if a == bin(2048):  # Aux. Sensor Fault.
                    bi[59] = 1
                # a = bin(rr4.registers[0] & 4096)
                # if a == bin(4096): #reserved
                    # bi[60] = 1
                # a = bin(rr4.registers[0] & 8192)
                # if a == bin(8192): #reserved
                    # bi[61] = 1
                # a = bin(rr4.registers[0] & 16384)
                # if a == bin(16384): #Smoke Learn in progress...
                    # bi[62] = 1
                a = bin(rr4.registers[0] & 32768)
                if a == bin(32768):  # Flow Normalization in progress...
                    bi[63] = 1

        be = [0]*64
        if pu[0] == 1:  # 如果管1有開啟
            a = bin(rr1.registers[5] & 1)  # faultcondition  1005
            if a == bin(1):
                be[0] = 1  # 如果有這個錯誤
            a = bin(rr1.registers[5] & 2)
            if a == bin(2):
                be[1] = 1
            a = bin(rr1.registers[5] & 4)
            if a == bin(4):
                be[2] = 1
            a = bin(rr1.registers[5] & 8)
            if a == bin(8):
                be[3] = 1
            a = bin(rr1.registers[5] & 16)
            if a == bin(16):
                be[4] = 1
            a = bin(rr1.registers[5] & 32)
            if a == bin(32):
                be[5] = 1
            a = bin(rr1.registers[5] & 64)
            if a == bin(64):
                be[6] = 1
            a = bin(rr1.registers[5] & 128)
            if a == bin(128):
                be[7] = 1
            a = bin(rr1.registers[5] & 256)
            if a == bin(256):
                be[8] = 1
            a = bin(rr1.registers[5] & 512)
            if a == bin(512):
                be[9] = 1
            a = bin(rr1.registers[5] & 1024)
            if a == bin(1024):
                be[10] = 1
            a = bin(rr1.registers[5] & 2048)
            if a == bin(2048):
                be[11] = 1
            a = bin(rr1.registers[5] & 4096)
            if a == bin(4096):
                be[12] = 1
            a = bin(rr1.registers[5] & 8192)
            if a == bin(8192):
                be[13] = 1
            a = bin(rr1.registers[5] & 16384)
            if a == bin(16384):
                be[14] = 1
            a = bin(rr1.registers[5] & 32768)
            if a == bin(32768):
                be[15] = 1

        if model[3][seti] == "4":  # flow四管
            if pu[1] == 1:  # 如果管2有開啟
                # a = bin(rr2.registers[5] & 1) #防區2
                # if a == bin(1):
                # be[16] = 1
                # a = bin(rr2.registers[5] & 2)
                # if a == bin(2):
                # be[17] = 1
                # a = bin(rr2.registers[5] & 4)
                # if a == bin(4):
                # be[18] = 1
                # a = bin(rr2.registers[5] & 8)
                # if a == bin(8):
                # be[19] = 1
                a = bin(rr2.registers[5] & 16)
                if a == bin(16):
                    be[20] = 1
                a = bin(rr2.registers[5] & 32)
                if a == bin(32):
                    be[21] = 1
                a = bin(rr2.registers[5] & 64)
                if a == bin(64):
                    be[22] = 1
                a = bin(rr2.registers[5] & 128)
                if a == bin(128):
                    be[23] = 1
                a = bin(rr2.registers[5] & 256)
                if a == bin(256):
                    be[24] = 1
                a = bin(rr2.registers[5] & 512)
                if a == bin(512):
                    be[25] = 1
                a = bin(rr2.registers[5] & 1024)
                if a == bin(1024):
                    be[26] = 1
                a = bin(rr2.registers[5] & 2048)
                if a == bin(2048):
                    be[27] = 1
                a = bin(rr2.registers[5] & 4096)
                if a == bin(4096):
                    be[28] = 1
                a = bin(rr2.registers[5] & 8192)
                if a == bin(8192):
                    be[29] = 1
                # a = bin(rr2.registers[5] & 16384)
                # if a == bin(16384):
                    # be[30] = 1
                a = bin(rr2.registers[5] & 32768)
                if a == bin(32768):
                    be[31] = 1

            if pu[2] == 1:
                # a = bin(rr3.registers[5] & 1) #防區3
                # if a == bin(1):
                # be[32] = 1
                # a = bin(rr3.registers[5] & 2)
                # if a == bin(2):
                # be[33] = 1
                # a = bin(rr3.registers[5] & 4)
                # if a == bin(4):
                # be[34] = 1
                # a = bin(rr3.registers[5] & 8)
                # if a == bin(8):
                # be[35] = 1
                a = bin(rr3.registers[5] & 16)
                if a == bin(16):
                    be[36] = 1
                a = bin(rr3.registers[5] & 32)
                if a == bin(32):
                    be[37] = 1
                a = bin(rr3.registers[5] & 64)
                if a == bin(64):
                    be[38] = 1
                a = bin(rr3.registers[5] & 128)
                if a == bin(128):
                    be[39] = 1
                a = bin(rr3.registers[5] & 256)
                if a == bin(256):
                    be[40] = 1
                a = bin(rr3.registers[5] & 512)
                if a == bin(512):
                    be[41] = 1
                a = bin(rr3.registers[5] & 1024)
                if a == bin(1024):
                    be[42] = 1
                a = bin(rr3.registers[5] & 2048)
                if a == bin(2048):
                    be[43] = 1
                a = bin(rr3.registers[5] & 4096)
                if a == bin(4096):
                    be[44] = 1
                a = bin(rr3.registers[5] & 8192)
                if a == bin(8192):
                    be[45] = 1
                # a = bin(rr3.registers[5] & 16384)
                # if a == bin(16384):
                    # be[46] = 1
                a = bin(rr3.registers[5] & 32768)
                if a == bin(32768):
                    be[47] = 1

            if pu[3] == 1:
                # a = bin(rr4.registers[5] & 1) #防區4
                # if a == bin(1):
                # be[48] = 1
                # a = bin(rr4.registers[5] & 2)
                # if a == bin(2):
                # be[49] = 1
                # a = bin(rr4.registers[5] & 4)
                # if a == bin(4):
                # be[50] = 1
                # a = bin(rr4.registers[5] & 8)
                # if a == bin(8):
                # be[51] = 1
                a = bin(rr4.registers[5] & 16)
                if a == bin(16):
                    be[52] = 1
                a = bin(rr4.registers[5] & 32)
                if a == bin(32):
                    be[53] = 1
                a = bin(rr4.registers[5] & 64)
                if a == bin(64):
                    be[54] = 1
                a = bin(rr4.registers[5] & 128)
                if a == bin(128):
                    be[55] = 1
                a = bin(rr4.registers[5] & 256)
                if a == bin(256):
                    be[56] = 1
                a = bin(rr4.registers[5] & 512)
                if a == bin(512):
                    be[57] = 1
                a = bin(rr4.registers[5] & 1024)
                if a == bin(1024):
                    be[58] = 1
                a = bin(rr4.registers[5] & 2048)
                if a == bin(2048):
                    be[59] = 1
                a = bin(rr4.registers[5] & 4096)
                if a == bin(4096):
                    be[60] = 1
                a = bin(rr4.registers[5] & 8192)
                if a == bin(8192):
                    be[61] = 1
                # a = bin(rr4.registers[5] & 16384)
                # if a == bin(16384):
                    # be[62] = 1
                a = bin(rr4.registers[5] & 32768)
                if a == bin(32768):
                    be[63] = 1

        smoke1 = ('%.3f' % (rr1.registers[1]/1000))  # 小數點 三位
        smoke2 = ('%.3f' % (rr2.registers[1]/1000))  # 小數點 三位
        smoke3 = ('%.3f' % (rr3.registers[1]/1000))  # 小數點 三位
        smoke4 = ('%.3f' % (rr4.registers[1]/1000))  # 小數點 三位

        # fire 2  #燈泡控制(01號命令)
        lamp = client.read_coils(100, 1, unit=setting[0])
        if lamp.bits[0] == True:
            firetwo = 1
        else:
            firetwo = 0
        lamp = client.read_coils(101, 1, unit=setting[0])  # fire 1
        if lamp.bits[0] == True:
            fireone = 1
        else:
            fireone = 0
        lamp = client.read_coils(102, 1, unit=setting[0])  # action
        if lamp.bits[0] == True:
            action = 1
        else:
            action = 0
        lamp = client.read_coils(103, 1, unit=setting[0])  # alert
        if lamp.bits[0] == True:
            alert = 1
        else:
            alert = 0
        lamp = client.read_coils(106, 1, unit=setting[0])  # isolate
        if lamp.bits[0] == True:
            isolate = 1
        else:
            isolate = 0
        lamp = client.read_coils(107, 1, unit=setting[0])  # 總故障燈(fault)
        if lamp.bits[0] == True:
            allok = 1
        else:
            allok = 0

        device = client.read_holding_registers(
            17, 2, unit=setting[0])  # 確認設備面板狀態、設備故障狀態(協定17、18)
        dev = bin(device.registers[0] & 128)
        b = device.registers[1]
        devicecon = 0
        de = 0
        if dev == bin(128):
            devicecon = 1
            de = [0] * 16
            if dev == bin(128):  # 判斷是否有總故障 有的話就看協定18的故障位元定義
                a = bin(b & 1)
                if a == bin(1):
                    de[0] = 1
                a = bin(b & 2)
                if a == bin(2):
                    de[1] = 1
                a = bin(b & 4)
                if a == bin(4):
                    de[2] = 1
                a = bin(b & 8)
                if a == bin(8):
                    de[3] = 1
                a = bin(b & 16)
                if a == bin(16):
                    de[4] = 1
                a = bin(b & 32)
                if a == bin(32):
                    de[5] = 1
                a = bin(b & 64)
                if a == bin(64):
                    de[6] = 1
                a = bin(b & 128)
                if a == bin(128):
                    de[7] = 1
                a = bin(b & 256)
                if a == bin(256):
                    de[8] = 1
                a = bin(b & 512)
                if a == bin(512):
                    de[9] = 1
                a = bin(b & 1024)
                if a == bin(1024):
                    de[10] = 1
                a = bin(b & 2048)
                if a == bin(2048):
                    de[11] = 1
        client.close()
        return render_template('status.html', seti=seti, modelvalue=setting[5], modelsize=modelsize, model=model, dictionary=dictionary, addr=setting[0], port=setting[2], comd=setting[2], com=port_list, count=len(port_list), smoke1=smoke1, smoke2=smoke2, smoke3=smoke3, smoke4=smoke4, rr1=rr1, rr2=rr2, rr3=rr3, rr4=rr4, rr5=rr5, detncondition=bi, faultcondition=be, devicecondition=de, devicecon=devicecon, firetwo=firetwo, fireone=fireone, action=action, alert=alert, isolate=isolate, allok=allok, zu=zu, pu=pu, devi=devi)
    except Exception as e:
        print("Error!", e)
        return "ok"


# control
@app.route('/control_iso/', methods=['GET', 'POST'])  # isolate
def control_iso():
    port_list = list(serial.tools.list_ports.comports())  # device port
    client = None
    i = 10
    d = None
    while d == None:
        # try:
        i = i-1
        # 客户机(通信方式，端口，波特率，超时)
        client = ModbusClient(
            method='rtu', port=setting[2], baudrate=setting[3], timeout=setting[4], strict=False)
        client.connect()
        d = client.socket
        if d != None:
            break
        else:
            print("retry!")
            time.sleep(1)
            if i < 0:
                break
    client.write_coil(2, 1, unit=setting[0])

    client.close()  # 連接完後要關掉
    return status()


@app.route('/control_uniso/', methods=['GET', 'POST'])  # de isolate
def control_uniso():
    port_list = list(serial.tools.list_ports.comports())  # device port
    client = None
    i = 10
    d = None
    while d == None:
        # try:
        i = i-1
        # 客户机(通信方式，端口，波特率，超时)
        client = ModbusClient(
            method='rtu', port=setting[2], baudrate=setting[3], timeout=setting[4], strict=False)
        client.connect()
        d = client.socket
        if d != None:
            break
        else:
            print("retry!")
            time.sleep(1)
            if i < 0:
                break
    client.write_coil(2, 0, unit=setting[0])
    client.close()  # 連接完後要關掉
    return status()


@app.route('/control_sil/', methods=['GET', 'POST'])  # silence
def control_sil():
    port_list = list(serial.tools.list_ports.comports())  # device port
    client = None
    i = 10
    d = None
    while d == None:
        # try:
        i = i-1
        # 客户机(通信方式，端口，波特率，超时)
        client = ModbusClient(
            method='rtu', port=setting[2], baudrate=setting[3], timeout=setting[4], strict=False)
        client.connect()
        d = client.socket
        if d != None:
            break
        else:
            print("retry!")
            time.sleep(1)
            if i < 0:
                break
    client.write_coil(1, 1, unit=setting[0])
    client.close()  # 連接完後要關掉
    return status()


@app.route('/control_test/', methods=['GET', 'POST'])  # test
def control_test():
    client = None
    i = 10
    d = None
    while d == None:
        # try:
        i = i-1
        # 客户机(通信方式，端口，波特率，超时)
        client = ModbusClient(
            method='rtu', port=setting[2], baudrate=setting[3], timeout=setting[4], strict=False)
        client.connect()
        d = client.socket
        if d != None:
            break
        else:
            print("retry!")
            time.sleep(1)
            if i < 0:
                break
    client.write_coil(0, 1, unit=setting[0])
    client.close()  # 連接完後要關掉
    webbrowser.open('http://127.0.0.1:5000/status', 0, False)


@app.route('/control_reset/', methods=['GET', 'POST'])  # reset
def control_reset():
    port_list = list(serial.tools.list_ports.comports())  # device port
    client = None
    i = 10
    d = None
    while d == None:
        # try:
        i = i-1
        # 客户机(通信方式，端口，波特率，超时)
        client = ModbusClient(
            method='rtu', port=setting[2], baudrate=setting[3], timeout=setting[4], strict=False)
        client.connect()
        d = client.socket
        if d != None:
            break
        else:
            print("retry!")
            time.sleep(1)
            if i < 0:
                break
    client.write_coil(3, 1, unit=setting[0])
    client.close()  # 連接完後要關掉
    return status()


"""advanced"""


@app.route('/advanced')  # 顯示數值
def advanced():
    seti = int(setting[5])  # 要將str轉換成int才能做成index
    port_list = list(serial.tools.list_ports.comports())  # device port
    client = None

    i = 10
    d = None
    while d == None:

        # try:
        i = i-1
        # 客户机(通信方式，端口，波特率，超时)
        client = ModbusClient(
            method='rtu', port=setting[2], baudrate=setting[3], timeout=setting[4], strict=False)
        client.connect()
        d = client.socket

        if d != None:
            break
        else:
            print("retry!")
            time.sleep(1)
            if i < 0:
                break

    rr5 = client.read_holding_registers(1139, 3, unit=setting[0])
    client.close()  # 連接完後要關掉
    scv = ('%.3f' % rr5.registers[1])  # 小數點 三位  #0
    kv = ('%.3f' % (rr5.registers[2]/1000))  # 小數點 三位  #1000
    return render_template('advanced.html', seti=seti, modelvalue=setting[5], modelsize=modelsize, model=model, dictionary=dictionary, addr=setting[0], comd=setting[2], com=port_list, count=len(port_list), uoasb=rr5.registers[0], scv=scv, kv=kv)


@app.route('/advanced_addr/', methods=['GET', 'POST'])
def advanced_addr():
    a = int(request.form.get('addr'))
    setting[0] = a
    return advanced()


@app.route('/advanced_parameter/', methods=['GET', 'POST'])
def advanced_parameter():
    seti = int(setting[5])  # 要將str轉換成int才能做成index
    port_list = list(serial.tools.list_ports.comports())  # device port
    # 客户机(通信方式，端口，波特率，超时)
    client = ModbusClient(
        method='rtu', port=setting[2], baudrate=setting[3], timeout=setting[4], strict=False)
    client.connect()
    if(model[92][seti] == "1"):
        a = int(request.form.get('select1'))
        client.write_registers(1139, a, unit=setting[0])
    if(model[93][seti] == "1"):
        a = int(float(request.form.get('select2')))
        client.write_registers(1140, a, unit=setting[0])
    if (model[94][seti] == "1"):
        a = int(float(request.form.get('select3'))*1000)
        client.write_registers(1141, a, unit=setting[0])
    rr5 = client.read_holding_registers(1139, 3, unit=setting[0])  # filter
    scv = ('%.3f' % rr5.registers[1])  # 小數點 三位  #0
    kv = ('%.3f' % (rr5.registers[2]/1000))  # 小數點 三位  #1000
    client.close()  # 連接完後要關掉
    return render_template('advanced.html', seti=seti, modelvalue=setting[5], modelsize=modelsize, model=model, dictionary=dictionary, addr=setting[0], comd=setting[2], com=port_list, count=len(port_list), uoasb=rr5.registers[0], scv=scv, kv=kv)


@app.route('/advanced_model/', methods=['GET', 'POST'])
def advanced_model():
    m = request.form.get('model')
    setting[5] = m
    return advanced()


"""zone relay"""


@app.route('/zone_relay')  # 顯示數值
def zone_relay():
    seti = int(setting[5])  # 要將str轉換成int才能做成index
    port_list = list(serial.tools.list_ports.comports())  # device port
    client = None

    i = 10
    d = None
    while d == None:

        # try:
        i = i-1
        # 客户机(通信方式，端口，波特率，超时)
        client = ModbusClient(
            method='rtu', port=setting[2], baudrate=setting[3], timeout=setting[4], strict=False)
        client.connect()
        d = client.socket

        if d != None:
            break
        else:
            print("retry!")
            time.sleep(1)
            if i < 0:
                break

    rr5 = client.read_holding_registers(1135, 4, unit=setting[0])  # pipe1
    rr6 = client.read_holding_registers(2135, 4, unit=setting[0])
    rr7 = client.read_holding_registers(3135, 4, unit=setting[0])
    rr8 = client.read_holding_registers(4135, 4, unit=setting[0])
    print(model[6][seti])
    if(model[6][seti] != 32):
        rr9 = client.read_holding_registers(5135, 4, unit=setting[0])  # pipe5
        rr10 = client.read_holding_registers(6135, 4, unit=setting[0])
        rr11 = client.read_holding_registers(7135, 4, unit=setting[0])
        rr12 = client.read_holding_registers(8135, 4, unit=setting[0])
        client.close()  # 連接完後要關掉
        return render_template('zone_relay.html', seti=seti, modelvalue=setting[5], modelsize=modelsize, model=model, dictionary=dictionary, addr=setting[0], comd=setting[2], pipe=setting[1], com=port_list, count=len(port_list), rr5=rr5, rr6=rr6, rr7=rr7, rr8=rr8, rr9=rr9, rr10=rr10, rr11=rr11, rr12=rr12)
    return render_template('zone_relay.html', seti=seti, modelvalue=setting[5], modelsize=modelsize, model=model, dictionary=dictionary, addr=setting[0], comd=setting[2], pipe=setting[1], com=port_list, count=len(port_list), rr5=rr5, rr6=rr6, rr7=rr7, rr8=rr8)


@app.route('/zone_relay_addr/', methods=['GET', 'POST'])
def zone_relay_addr():
    a = int(request.form.get('addr'))
    setting[0] = a
    return zone_relay()


@app.route('/zone_relay_parameter/', methods=['GET', 'POST'])
def zone_relay_parameter():
    seti = int(setting[5])  # 要將str轉換成int才能做成index
    port_list = list(serial.tools.list_ports.comports())  # device port
    # 客户机(通信方式，端口，波特率，超时)
    client = ModbusClient(
        method='rtu', port=setting[2], baudrate=setting[3], timeout=setting[4], strict=False)
    client.connect()
    a = int(request.form.get('select1'))
    client.write_registers(1135, a, unit=setting[0])
    a = int(request.form.get('select2'))
    client.write_registers(1136, a, unit=setting[0])
    a = int(request.form.get('select3'))
    client.write_registers(1137, a, unit=setting[0])
    a = int(request.form.get('select4'))
    client.write_registers(1138, a, unit=setting[0])
    a = int(request.form.get('select5'))
    client.write_registers(2135, a, unit=setting[0])
    a = int(request.form.get('select6'))
    client.write_registers(2136, a, unit=setting[0])
    a = int(request.form.get('select7'))
    client.write_registers(2137, a, unit=setting[0])
    a = int(request.form.get('select8'))
    client.write_registers(2138, a, unit=setting[0])
    a = int(request.form.get('select9'))
    client.write_registers(3135, a, unit=setting[0])
    a = int(request.form.get('select10'))
    client.write_registers(3136, a, unit=setting[0])
    a = int(request.form.get('select11'))
    client.write_registers(3137, a, unit=setting[0])
    a = int(request.form.get('select12'))
    client.write_registers(3138, a, unit=setting[0])
    a = int(request.form.get('select13'))
    client.write_registers(4135, a, unit=setting[0])
    a = int(request.form.get('select14'))
    client.write_registers(4136, a, unit=setting[0])
    a = int(request.form.get('select15'))
    client.write_registers(4137, a, unit=setting[0])
    a = int(request.form.get('select16'))
    client.write_registers(4138, a, unit=setting[0])

    if (model[6][seti] != "32"):
        a = int(request.form.get('select17'))
        client.write_registers(5135, a, unit=setting[0])
        a = int(request.form.get('select18'))
        client.write_registers(5136, a, unit=setting[0])
        a = int(request.form.get('select19'))
        client.write_registers(5137, a, unit=setting[0])
        a = int(request.form.get('select20'))
        client.write_registers(5138, a, unit=setting[0])
        a = int(request.form.get('select21'))
        client.write_registers(6135, a, unit=setting[0])
        a = int(request.form.get('select22'))
        client.write_registers(6136, a, unit=setting[0])
        a = int(request.form.get('select23'))
        client.write_registers(6137, a, unit=setting[0])
        a = int(request.form.get('select24'))
        client.write_registers(6138, a, unit=setting[0])
        a = int(request.form.get('select25'))
        client.write_registers(7135, a, unit=setting[0])
        a = int(request.form.get('select26'))
        client.write_registers(7136, a, unit=setting[0])
        a = int(request.form.get('select27'))
        client.write_registers(7137, a, unit=setting[0])
        a = int(request.form.get('select28'))
        client.write_registers(7138, a, unit=setting[0])
        a = int(request.form.get('select29'))
        client.write_registers(8135, a, unit=setting[0])
        a = int(request.form.get('select30'))
        client.write_registers(8136, a, unit=setting[0])
        a = int(request.form.get('select31'))
        client.write_registers(8137, a, unit=setting[0])
        a = int(request.form.get('select32'))
        client.write_registers(8138, a, unit=setting[0])
    client.close()  # 連接完後要關掉
    return zone_relay()


@app.route('/zone_relay_model/', methods=['GET', 'POST'])
def zone_relay_model():
    m = request.form.get('model')
    a = int(request.form.get('model'))
    if(model[88][a] != "1"):
        return settings()
    setting[5] = m
    return zone_relay()


@app.route('/zone_relay_pipe/', methods=['GET', 'POST'])
def zone_relay_pipe():
    a = int(request.form.get('pipe'))
    setting[1] = a
    return zone_relay()


if __name__ == '__main__':
    # 函數:初次拜訪網站預設addr=1、tube=1
    # app.debug = False
    webbrowser.open('http://127.0.0.1:5000/settings', 0, False)
    app.run()
