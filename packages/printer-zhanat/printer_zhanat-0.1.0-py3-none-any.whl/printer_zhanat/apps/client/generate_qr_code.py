import qrcode

data = 'http://192.168.88.96:8000/client/payment/123'
img = qrcode.make(data)
img.save('MyQRCode1.png')
