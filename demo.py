from fonAPI import FonApi

fon = FonApi('yourKey')

device = '3210'
phones = fon.getdevice(device)
try:
    for phone in phones:
        print phone['DeviceName']
        print phone['weight']
        print phone['resolution']
except:
    print phones
