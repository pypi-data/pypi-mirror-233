from escpos.printer import Usb
from escpos.exceptions import USBNotFoundError

from printer_zhanat.apps.config.settings import settings


def get_usb_object() -> Usb:
    try:
        printer = Usb(idVendor=settings.VENDOR_ID,
                      idProduct=settings.PRODUCT_ID, out_ep=0x2)
    except USBNotFoundError as e:
        print(e)
        exit()
    else:
        return printer

