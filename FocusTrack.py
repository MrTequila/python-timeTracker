import sys
import datetime
import ctypes
import ctypes.wintypes
from sqlalchemy import Column, Interval, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import timedelta
from SqlInterface import Program


# Initiating sqlite db in sqlalchemy
Base = declarative_base()
engine = create_engine('sqlite:///focustracker.db')
Base.metadata.create_all(engine)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#EVENT_SYSTEM_DIALOGSTART = 0x0010
EVENT_OBJECT_FOCUS = 0x8005
WINEVENT_OUTOFCONTEXT = 0x0000

user32 = ctypes.windll.user32
ole32 = ctypes.windll.ole32

ole32.CoInitialize(0)

WinEventProcType = ctypes.WINFUNCTYPE(
    None,
    ctypes.wintypes.HANDLE,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.HWND,
    ctypes.wintypes.LONG,
    ctypes.wintypes.LONG,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.DWORD
)

currentName = 0
then = datetime.datetime.now()
activityList = {}


# Function that handles window focus - here add time tracking and adding new programs.
def callback(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
    global currentName, then, activityList

    length = user32.GetWindowTextLengthA(hwnd)
    buff = ctypes.create_string_buffer(length + 1)
    user32.GetWindowTextA(hwnd, buff, length + 1)

    if currentName != buff.value:
        now = datetime.datetime.now()
        duration = now - then
        then = now
        # Saving into db
        # print("Current Name: ", currentName)
        # print("Buff.value: ", buff.value)
        # print("Duration: ", duration)
        temp_duration = int(duration.days)*24*60*60 + int(duration.seconds)
        program_check = session.query(Program).filter(Program.name == str(currentName)).one_or_none()
        if program_check is None:
            new_program = Program(name=str(currentName), duration=int(temp_duration))
            session.add(new_program)
            session.commit()
        else:
            session.query(Program).filter(Program.name == str(currentName)).\
                update({"duration": (Program.duration + int(temp_duration))})
            session.commit()
        if currentName in activityList:
            activityList[currentName] += duration
        else:
            activityList[currentName] = duration
        currentName = buff.value

    # for k, v in activityList.items():
    #    print(k, v)
    for prog in session.query(Program):
        print(str(prog.name), prog.duration)
    # print(buff.value)

currentName = 0
WinEventProc = WinEventProcType(callback)

user32.SetWinEventHook.restype = ctypes.wintypes.HANDLE
hook = user32.SetWinEventHook(
    EVENT_OBJECT_FOCUS,
    EVENT_OBJECT_FOCUS,
    0,
    WinEventProc,
    0,
    0,
    WINEVENT_OUTOFCONTEXT
)
if hook == 0:
    print('SetWinEventHook failed')
    sys.exit(1)

msg = ctypes.wintypes.MSG()
while user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) != 0:
    user32.TranslateMessageW(msg)
    user32.DispatchMessageW(msg)

user32.UnhookWinEvent(hook)
ole32.CoUninitialize()