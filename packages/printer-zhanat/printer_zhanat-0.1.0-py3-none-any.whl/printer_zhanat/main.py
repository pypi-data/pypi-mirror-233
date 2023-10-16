from xmlrpc.client import ProtocolError, Error

from escpos.printer import Usb
from usb.backend.libusb1 import get_backend
from usb.core import find
# import serial
# import pyshtrih


def discovery_callback(port, baudrate):
    # print(port, baudrate)
    pass


def print_shtrih(unique_code: int) -> None:
    print('Printend shtrih')


def main():
    vendor_id = 0x0403
    product_id = 0x6001

    # backend = get_backend(find_library=lambda x: "/opt/homebrew/lib/libusb-1.0.0.dylib")
    # dev = find(idVendor=vendor_id, idProduct=product_id, backend=backend)
    # print(dev)

    # Create a USB printer_zhanat instance
    printer = Usb(vendor_id, product_id, in_ep=0x81, out_ep=0x2)

    # Print text
    printer.text("Hello, Thermal Printer!\n")
    printer.cut()  # Cut the paper (if supported by the printer_zhanat)

    # # Close the printer_zhanat client
    # printer_zhanat.close()

    # # Configure the serial client
    # serial_port = '/dev/tty.usbserial-AI0543YE'  # Replace with the actual serial port name
    # baud_rate = 9600  # Set according to your printer_zhanat's specifications
    #
    # printer_zhanat = serial.Serial(serial_port, baud_rate)
    # print(printer_zhanat)
    #
    # # Send commands to the printer_zhanat
    # command = b'\x1B\x40'  # Hypothetical command to initialize the printer_zhanat
    # printer_zhanat.write(command)
    #
    # text_to_print = "Hello, ШТРИХ-М-ПТК!"
    # encoded_text = text_to_print.encode(
    #     'cp1251')  # Convert text to the appropriate encoding
    # printer_zhanat.write(encoded_text)
    #
    # # Close the printer_zhanat client
    # printer_zhanat.close()

    # Create an instance of the ShtrihFR class
    # printer_zhanat = ShtrihM01F(port='/dev/tty.usbserial-AI0543YE')  # Replace with your actual port and password
    # print(printer_zhanat)

    # devices = pyshtrih.discovery(discovery_callback)
    # device = devices[0]
    # device.connect()
    # device.open_check(0)
    # device.cancel_check()
    # device.print_string('che tam')
    # device.print_string('che tam')
    # device.print_string('che tam')
    # device.print_string('che tam')
    # device.print_string('che tam')
    # device.print_string('che tam')
    # device.print_string('che tam')
    # device.wait_printing()
    # device.close_check()
    # device.cut()
    # device.sale(
    #     (u'Позиция 1', 1000, 1000), tax1=1
    # )
    # device.sale(
    #     (u'Позиция 2', 1000, 2000), tax1=2
    # )
    # device.sale(
    #     (u'Позиция 3', 1000, 3000), tax1=3
    # )
    # device.sale(
    #     (u'Позиция 4', 1000, 4000), tax1=4
    # )
    # device.close_check(10000)
    # device.cut(True)

    while True:
        command = input('Command: ')
        try:
            method = device.__getattribute__(command)
        except AttributeError:
            continue

        arg = input('arg: ').split(', ')

        args = []
        for a in arg:
            if a.isdigit():
                a = int(a)
            args.append(a)

        try:
            if args[0] != '':
                a = method(*args)
                print(a)
            else:
                a = method()
                print(a)
        except Exception as e:
            print(e)
            continue

    device.disconnect()


if __name__ == '__main__':
    # import collections
    # from collections import abc
    # from pyshtrih.misc import CAST_SIZE
    # import qrcode
    # qr = qrcode.QRCode(
    #     version=1,
    #     error_correction=qrcode.constants.ERROR_CORRECT_L,
    #     box_size=10,
    #     border=4,
    # )

    # data_to_encode = "https://www.youtube.com/"  # Замените на свои данные
    # qr.add_data(data_to_encode)
    # qr.make(fit=True)
    # qr_img = qr.make_image(fill_color="black", back_color="white")
    # qr_byte_array = qr_img.tobytes()
    # print(qr_byte_array)
    # print(qr_img.height)

    # devices = pyshtrih.discovery(discovery_callback)
    # device = devices[0]
    # device.connect()
    # device.load_graphics(1, qr_byte_array)
    # device.disconnect()

    #
    # for i, j in CAST_SIZE.items():
    #     print(i, j.funcs)
    #
    # collections.Mapping = abc.Mapping
    #
    # main()
    id_vendor = 0x0dd4
    id_device = 0x015d
    job = Usb(id_vendor, id_device, 0)
    job.text('hello! world\n')
    job.cut()
