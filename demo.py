from fonAPI import FonApi

fon = FonApi('24875e2d23e5583dab960129306139fb60db0c3b6f01144c')

device = '3210'
phones = fon.getdevice(device)
try:
    for phone in phones:
        print phone['DeviceName']
        print phone['weight']
        print phone['resolution']
except:
    print phones
