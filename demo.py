from fonAPI import FonApi

fon = FonApi()

device = 'lenovo'

for phone in fon.getdevice(device):
    print phone['DeviceName']