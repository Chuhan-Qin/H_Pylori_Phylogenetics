import telnetlib

mac_list = []

file = open("mac.txt","r+")
mac_list_temp = file.readlines()
for mac in mac_list_temp:
    mac_list.append(mac.strip('\n'))

tn = telnetlib.Telnet("172.17.51.130")

print("正在清除限速...")

line = bytes.decode(tn.read_until(b'Password:'))
tn.write(b'ruijie' + b'\n')

line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205>'))
tn.write(b'en' + b'\n')

line = bytes.decode(tn.read_until(b'Password:'))
tn.write(b'apdebug' + b'\n')

line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205#'))
tn.write(b'con' + b'\n')

for mac in mac_list:
    line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205(config)#'))
    no_speed = "no wlan-qos netuser " + mac + " inbound"
    no_speed_bytes = bytes(no_speed, encoding='utf-8')
    tn.write(no_speed_bytes + b'\n')

line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205(config)#'))
tn.write(b'en' + b'\n')

line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205#'))
tn.write(b'wr' + b'\n')

line = bytes.decode(tn.read_until(b'xiqu-1-1-201-205#'))

print('完毕。')

tn.close()
