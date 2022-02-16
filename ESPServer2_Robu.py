from re import T
import network
import socket
import urequests
import utime
import json
import dht

MAX_CONN = 5 #Costante
dht = dht.DHT11(machine.Pin(4))

def connWifi(ssid, password):
    wlanObj = network.WLAN(network.STA_IF)
    
    if not wlanObj.isconnected():
        print('Connessione alla rete ' + ssid + '...')
        wlanObj.connect(ssid, password) #Connect to an AccessPoint(NomeRete, password)
        while not wlanObj.isconnected():
            pass
        
    parametri = wlanObj.ifconfig() #Parametri è una lista ottenuta dalla rete a cui ci connettiamo
    print('\nParametri di rete: ')
    for p in parametri:
        print(p)
    
    return wlanObj

def creaSocket(porta):
    address = socket.getaddrinfo("0.0.0.0", porta)[0][-1]
    s = socket.socket() #Creo l'oggetto socket
    s.bind(address) #Collego l'oggetto socket s all'indirizzo deulla porta 80 (Mi permette di fare una richiesta da browser)
    s.listen(MAX_CONN) #Mettiti in ascolto sulla porta 80 e accetta massimo MAX_CONN connessioni contemporaneamente
    print("In ascolto su: ", address)
    
    return s

def getTemp():
    #t = dht.read(temp_c) #temperatura in gradi celsius
    t = 43
    return t

def getHum():
    #h = dht.read(humidity)
    h = 30
    return h

def main():
    luceAcc1 = False
    luceAcc2 = False

    connWifi("martino", "12345678")
    sock = creaSocket(80)
        
    while True: #Ciclo in cui il socket si mette in ascolto di una richiesta da parte del client
        client, datiIP = sock.accept() #accept è bloccante, mi blocco in attesa di una richiesta in ingresso
        clFile = client.makefile("rwb", 0)
        print("IP del client connesso: " + str(datiIP[0]))
        print("Porta del client connesso: " + str(datiIP[1]))

        fine = False
        while fine == False:
            line = clFile.readline().decode()
            #print(line)
            #GET /stanza1(stanza2,home)/luce/on(off)
            #Ottengo la QueryString
            if "GET" in line:
                #line = line.split(' ')
                query = line.split('/')

            if not line or line == '\r\n':
                fine = True

        html = ''

        if len(query) == 2:

            if query[1] == 'home':
                html = '<html><head><title> HOME </title></head> <body><h1> Home </h1><a href="/stanza1">Stanza1</a> <br> <a href="/stanza2">Stanza2</a>'
            elif query[1] == 'stanza1':
                html = '<html><head><title> Stanza 1 </title></head> <body><h1> Home </h1><a href="/luce/on">Accendi Luce</a> <br> <a href="/luce/off">Spegni Luce</a>'
            elif query[1] == 'stanza2':
                html = '<html><head><title> Stanza 2 </title></head> <body><h1> Home </h1><a href="/luce/on">Accendi Luce</a> <br> <a href="/luce/off">Spegni Luce</a>'
        
        if len(query) == 4:

            if query[1] == 'stanza1' and query[3] == 'on' and luceAcc1 == True:
                html = '<html><head><title> Stanza 1 </title></head> <body><h1> Home </h1> <p>La luce in stanza 1 è già accesa</p> <a href="/luce/on">Accendi Luce</a> <br> <a href="/luce/off">Spegni Luce</a>'

            if query[1] == 'stanza1' and query[3] == 'on' and luceAcc1 == False:
                html = '<html><head><title> Stanza 1 </title></head> <body><h1> Home </h1> <p>La luce in stanza 1 è stata accesa</p> <a href="/luce/on">Accendi Luce</a> <br> <a href="/luce/off">Spegni Luce</a>'
                luceAcc1 = True

            if query[1] == 'stanza1' and query[3] == 'off' and luceAcc1 == True:
                html = '<html><head><title> Stanza 1 </title></head> <body><h1> Home </h1> <p>La luce in stanza 1 è stata spenta</p> <a href="/luce/on">Accendi Luce</a> <br> <a href="/luce/off">Spegni Luce</a>' 
                luceAcc1 = False

            if query[1] == 'stanza1' and query[3] == 'off' and luceAcc1 == False:
                html = '<html><head><title> Stanza 1 </title></head> <body><h1> Home </h1> <p>La luce in stanza 1 è già spenta</p> <a href="/luce/on">Accendi Luce</a> <br> <a href="/luce/off">Spegni Luce</a>' 

#*********************************************************************************************************************************************************************

            if query[1] == 'stanza2' and query[3] == 'on' and luceAcc2 == True:
                html = '<html><head><title> Stanza 2 </title></head> <body><h1> Home </h1> <p>La luce in stanza 2 è già accesa</p> <a href="/luce/on">Accendi Luce</a> <br> <a href="/luce/off">Spegni Luce</a>'

            if query[1] == 'stanza2' and query[3] == 'on' and luceAcc2 == False:
                html = '<html><head><title> Stanza 2 </title></head> <body><h1> Home </h1> <p>La luce in stanza 2 è stata accesa</p> <a href="/luce/on">Accendi Luce</a> <br> <a href="/luce/off">Spegni Luce</a>'
                luceAcc2 = True

            if query[1] == 'stanza2' and query[3] == 'off' and luceAcc2 == True:
                html = '<html><head><title> Stanza 2 </title></head> <body><h1> Home </h1> <p>La luce in stanza 2 è stata spenta</p> <a href="/luce/on">Accendi Luce</a> <br> <a href="/luce/off">Spegni Luce</a>'
                luceAcc2 = False 

            if query[1] == 'stanza2' and query[3] == 'off' and luceAcc2 == False:
                html = '<html><head><title> Stanza 2 </title></head> <body><h1> Home </h1> <p>La luce in stanza 2 è già spenta</p> <a href="/luce/on">Accendi Luce</a> <br> <a href="/luce/off">Spegni Luce</a>' 

            
        html = html + '</body></html>' 
        #print(html)
        response = bytes(html, "utf-8")
        client.send(response)
        client.close()


main() 