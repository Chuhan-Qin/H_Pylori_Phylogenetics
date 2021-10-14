import telnetlib
import random
import time

print("**************欢迎使用雷恩TM速率干扰系统！**************","\n")
min = input("请输入随机速率最小值（kbps）：")
max = input("请输入随机速率最大值（kbps）：")
mac_str = input("请输入想要调控速率的mac地址库，以'/'分隔，若需要默认mac地址，请输入1，若需要从txt文件导入mac地址库，请输入0：")
if mac_str == '0':
    f = input("请输入mac地址库的文件路径（txt文件格式应为每行一个mac地址），若使用默认路径（默认为本程序路径下的mac.txt），请输入0：")
if mac_str != '1':
    sep = input('是否对不同用户进行不同的速度限制？y/n: ')
freq = input('请输入命令发送间隔，0为不停顿发送，60大约一分钟，以此类推：')
mac_list = []
list_average = 0

if mac_str != '1':
    if mac_str == '0':
        if f == '0':
            file = open("./mac.txt","r+")
            mac_list_temp = file.readlines()
            for mac in mac_list_temp:
                mac_list.append(mac.strip('\n'))
        else:
            file = open(f, "r+")
            mac_list_temp = file.readlines()
            for mac in mac_list_temp:
                mac_list.append(mac.strip('\n'))
    else:
        mac_list = mac_str.split('/')

    print('\n' + '-------------------------------------------------')
    print("您指定的mac地址列表如下：")
    for i in mac_list:
        print('>' + i + '<')
    print('\n'+"您指定的速度区间如下：")
    print(min,'-',max,'kbps')
    print('-------------------------------------------------' + '\n')
    print("限速程序正在运行...")


    if sep == 'n':
        tn = telnetlib.Telnet("172.17.51.130")
        line = bytes.decode(tn.read_until(b'Password:', timeout=None))
        tn.write(b'ruijie' + b'\n')

        line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205>'))
        tn.write(b'en' + b'\n')

        line = bytes.decode(tn.read_until(b'Password:'))
        tn.write(b'apdebug' + b'\n')

        line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205#'))

        while True:
            speed_random = random.randint(int(min), int(max))

            tn.write(b'con' + b'\n')

            for mac in mac_list:
                line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205(config)#'))
                speed = "wlan-qos netuser " + mac + " inbound average-data-rate " + str(speed_random) + ' burst-data-rate ' + str(speed_random)
                speed_bytes = bytes(speed, encoding='utf-8')
                tn.write(speed_bytes + b'\n')

            line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205(config)#'))
            print('\r','共', len(mac_list), '个用户当前限速值统一为：', speed_random, 'kbps', end='', flush=True)
            tn.write(b'en' + b'\n')

            line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205#'))
            tn.write(b'wr' + b'\n')

            line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205#'))

            time.sleep(int(freq))
        tn.close()

    else:
        tn = telnetlib.Telnet("172.17.51.130")
        line = bytes.decode(tn.read_until(b'Password:', timeout=None))
        tn.write(b'ruijie' + b'\n')

        line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205>'))
        tn.write(b'en' + b'\n')

        line = bytes.decode(tn.read_until(b'Password:'))
        tn.write(b'apdebug' + b'\n')

        line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205#'))

        while True:

            tn.write(b'con' + b'\n')
            list_temp = []
            for mac in mac_list:
                speed_random = random.randint(int(min), int(max))
                list_temp.append([mac,speed_random])
                line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205(config)#'))
                speed = "wlan-qos netuser " + mac + " inbound average-data-rate " + str(
                    speed_random) + ' burst-data-rate ' + str(speed_random)
                speed_bytes = bytes(speed, encoding='utf-8')
                tn.write(speed_bytes + b'\n')

            line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205(config)#'))
            for i in list_temp:
                list_average += i[1]
            list_average = list_average/len(mac_list)
            print('\r', '共', len(mac_list), '个用户当前限速均值为：', format(list_average,'.2f'), 'kbps', end='', flush=True)
            tn.write(b'en' + b'\n')

            line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205#'))
            tn.write(b'wr' + b'\n')

            line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205#'))

            time.sleep(int(freq))

        tn.close()



else:
    mac_list = mac_str.split('/')
    print('\n'+ '-------------------------------------------------')
    print("您指定的mac地址列表如下：")
    print('5c61.9925.7d83')
    print("您指定的速度区间如下：")
    print(min, '-', max, 'kbps')
    print('-------------------------------------------------'+'\n')
    print("限速程序正在运行...")

    tn = telnetlib.Telnet("172.17.51.130")
    line = bytes.decode(tn.read_until(b'Password:'))
    tn.write(b'ruijie' + b'\n')

    line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205>'))
    tn.write(b'en' + b'\n')

    line = bytes.decode(tn.read_until(b'Password:'))
    tn.write(b'apdebug' + b'\n')

    line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205#'))

    while True:
        speed_random = random.randint(int(min), int(max))

        tn.write(b'con' + b'\n')

        line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205(config)#'))
        speed = "wlan-qos netuser 5c61.9925.7d83 inbound average-data-rate " + str(speed_random) + ' burst-data-rate ' + str(speed_random)
        speed_bytes = bytes(speed, encoding='utf-8')
        tn.write(speed_bytes + b'\n')

        line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205(config)#'))
        print('\r', '用户：5c61.9925.7d83 当前限速值为：', speed_random, 'kbps', end='', flush=True)
        tn.write(b'en' + b'\n')

        line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205#'))
        tn.write(b'wr' + b'\n')

        line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205#'))

        time.sleep(int(freq))

    tn.close()

