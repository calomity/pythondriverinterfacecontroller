import os
from ctypes import *
from ctypes.wintypes import *

name = "\\\\.\\mousehooker"
FILE_ANY_ACCESS                 = 0
FILE_SPECIAL_ACCESS             = FILE_ANY_ACCESS
METHOD_BUFFERED                 = 0
OPEN_EXISTING = 3
INVALID_HANDLE_VALUE = -1
GENERIC_READ            = 0x80000000
GENERIC_WRITE           = 0x40000000
FILE_SHARE_READ         = 1 
FILE_SHARE_WRITE        = 2 
FILE_ATTRIBUTE_SYSTEM   = 4
FILE_FLAG_OVERLAPPED    = 0x40000000
hDll = ctypes.WinDLL ("kernel32.dll")
SIOCTL_TYPE = 40000
def _CTL_CODE(device_type, function, method, access):
    return (device_type << 16) | (access << 14) | (function << 2) | method
IO_MOUSE_LEFT_CLICK = _CTL_CODE(SIOCTL_TYPE, 0x12850 , METHOD_BUFFERED, FILE_SPECIAL_ACCESS)

class MOUSE_REQUEST(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_long),
        ("y", ctypes.c_long),
        ("button_flags", ctypes.c_ushort)
    ]

    @classmethod
    def Input_Informations(cls,flags):
        mouse_req = MOUSE_REQUEST()
        mouse_req.x = 0
        mouse_req.y = 0
        mouse_req.button_flags = flags
        return mouse_req

handle = ctypes.windll.kernel32.CreateFileA(
            name.encode(),
            GENERIC_READ | GENERIC_WRITE, 
            0,
            None, OPEN_EXISTING, 
            FILE_ATTRIBUTE_SYSTEM | FILE_FLAG_OVERLAPPED,
            None
        )  
if handle == INVALID_HANDLE_VALUE:
    print("hata driver kurulu degil.\n")
def ioctl(flags):
    mouse_req = MOUSE_REQUEST.Input_Informations(flags)
    res = DWORD()
    ctypes.windll.kernel32.DeviceIoControl(handle,IO_MOUSE_LEFT_CLICK,ctypes.byref(mouse_req),ctypes.sizeof(mouse_req),ctypes.byref(mouse_req),ctypes.sizeof(mouse_req),res,None)

def send_click():
    ioctl(0x1)
    ioctl(0x2)

send_click()    
