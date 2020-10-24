"""
List of Devices			            MAC ADDRESS		Connection Type     type
                                                                                                              SmartHome    Assist   Camera  Plug    Sensor  Ligth   SmartPhones PC
Smart Things 				        d0:52:a8:00:67:5e 	Wired           SmartHome   ok
Amazon Echo 				        44:65:0d:56:cc:d3 	Wireless        Assist      ok
Netatmo Welcome 			        70:ee:50:18:34:43 	Wireless        Camera      ok
TP-Link Day Night Cloud camera 	    f4:f2:6d:93:51:f1 	Wireless        Camera      ok
Samsung SmartCam 			        00:16:6c:ab:6b:88 	Wireless        Camera      ok
Dropcam 				            30:8c:fb:2f:e4:b2 	Wireless        Camera      ok
Insteon Camera 			            00:62:6e:51:27:2e	Wired           Camera      ok
					                e8:ab:fa:19:de:4f 	Wireless        Camera      ok
Withings Smart Baby Monitor 		00:24:e4:11:18:a8 	Wired           Camera      ok
Belkin Wemo switch 			        ec:1a:59:79:f4:89 	Wireless        Plug        ok
TP-Link Smart plug 			        50:c7:bf:00:56:39 	Wireless        Plug        ok
iHome 					            74:c6:3b:29:d7:1d 	Wireless        SmartHome   ok   
Belkin wemo motion sensor 		    ec:1a:59:83:28:11 	Wireless        Sensor      ok
NEST Protect smoke alarm 		    18:b4:30:25:be:e4	Wireless        Sensor      ok
Netatmo weather station 		    70:ee:50:03:b8:ac 	Wireless        Sensor      ok
Withings Smart scale 			    00:24:e4:1b:6f:96 	Wireless        Sensor      ok
Blipcare Blood Pressure meter 	    74:6a:89:00:2e:25 	Wireless        Sensor      ok
Withings Aura smart sleep sensor 	00:24:e4:20:28:c6 	Wireless        Sensor      ok
Light Bulbs LiFX Smart Bulb 		d0:73:d5:01:83:08 	Wireless        Ligth       ok
Triby Speaker 				        18:b7:9e:02:20:44 	Wireless        SmartHome   ok
PIX-STAR Photo-frame 			    e0:76:d0:33:bb:85 	Wireless        SmartHome   ok
HP Printer 				            70:5a:0f:e4:9b:c0 	Wireless        Printer     ok       
Samsung Galaxy Tab			        08:21:ef:3b:fc:e3	Wireless        SmartPhones ok
Nest Dropcam				        30:8c:fb:b6:ea:45	Wireless        Camera      ok
Android Phone				        40:f3:08:ff:1e:da	Wireless        SmartPhones ok
Laptop					            74:2f:68:81:69:42	Wireless        PC          ok
MacBook				                ac:bc:32:d4:6f:2f	Wireless        PC          ok
Android Phone				        b4:ce:f6:a7:a3:c2	Wireless        SmartPhones ok        
IPhone					            d0:a6:37:df:a1:e1	Wireless        SmartPhones ok


Info about the system --- fisrt try to extrat the info in classes for traning ML

    classes     SmartHome    Assist   Camera  Plug    Sensor  Ligth   SmartPhones PC   Printer
                    ok          ok     ok      ok       ok     ok         ok      ok     ok
"""

import os
import glob

ip_filter = {} #dictionary

#ip_filter['y'] = "'tcp && (eth.src==00:16:6c:ab:6b:88)'" #camara a ser avaliada
#ip_filter['n'] = "'tcp && (eth.src==ec:1a:59:79:f4:89) || (eth.src==50:c7:bf:00:56:39)'"
#ip_filter['TP-LINK_Camera'] = "'tcp && (eth.src==f4:f2:6d:93:51:f1)'"
#ip_filter['Drop_Camera'] = "'tcp && (eth.src==30:8c:fb:2f:e4:b2)'"
ip_filter['y'] = "'tcp && (eth.src==70:ee:50:18:34:43) || (eth.src==f4:f2:6d:93:51:f1)  || (eth.src==30:8c:fb:2f:e4:b2)  || (eth.src==00:62:6e:51:27:2e)  || (eth.src==e8:ab:fa:19:de:4f)  || (eth.src==00:24:e4:11:18:a8)  || (eth.src==30:8c:fb:b6:ea:45)'"      #ok
ip_filter['n'] = "'tcp && (eth.src==74:2f:68:81:69:42) || (eth.src==ac:bc:32:d4:6f:2f)'"  #ok

# eli
#os.system("./start.sh")
#######################################################################################

# creat file lable_feature

lable_feature = open("../pcap_tensor/devices.csv",'a')

lable_feature.writelines("Label,IPLength,IPHeaderLength,TTL,\
           Protocol,SourcePort,DestPort,SequenceNumber,AckNumber\
           ,WindowSize,TCPHeaderLength,TCPLength,TCPStream\
     ,TCPUrgentPointer,IPFlags,IPID,IPchecksum,TCPflags,TCPChecksum\n")


########################################################################################

# separat classes in files pcap

for pcap_original in glob.glob('../../pcap_original/*.pcap'):
    for x in ip_filter.keys():
        os.system("tshark -r" + pcap_original + " -w- -Y " + 
                ip_filter[x] + ">> ../pcap_separado/" + x + ".pcap")

########################################################################################

# convert the pcap files in file to ML

for filtered_file in glob.glob('../pcap_separado/*.pcap'):
    #print(filtered_file)
    file_name = filtered_file.split('/')[-1]
    lable = file_name.replace('.pcap','')
    tshark_command = "tshark -r " + filtered_file + " -T fields \
                    -e ip.len -e ip.hdr_len -e ip.ttl \
                    -e ip.proto -e tcp.srcport -e tcp.dstport -e tcp.seq \
                    -e tcp.ack -e tcp.window_size_value -e tcp.hdr_len -e tcp.len \
                    -e tcp.stream -e tcp.urgent_pointer \
                    -e ip.flags -e ip.id -e ip.checksum -e tcp.flags -e tcp.checksum"

    all_features = str( os.popen(tshark_command).read() )
    all_features = all_features.replace('\t',',')
    all_features_list = all_features.splitlines()
    for features in all_features_list:
        lable_feature.writelines(lable + "," + features + "\n")
    

########################################################################################
########################################################################################
########################################################################################
########################################################################################

print("--------------DONE---------------")
