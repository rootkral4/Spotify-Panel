from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import keyboard
import win32gui
import win32con
import win32api

sessionHandle = None
volumeHandle = None
currentVolume = 0

playingEx = None

def findSpotify():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "Spotify.exe":
            return session, volume
    raise Exception("Spotify.exe couldn't found")

def volumeUp(handle, inc):
    global currentVolume
    newVolume = round(currentVolume + inc, 2)
    if currentVolume != 1.0:
        handle.SetMasterVolume(currentVolume + inc, None)
        currentVolume = newVolume
        print("Current volume :", currentVolume)

def volumeDown(handle, dec):
    global currentVolume
    newVolume = round(currentVolume - dec, 2)
    if newVolume >= 0.0:
        handle.SetMasterVolume(newVolume, None)
        currentVolume = newVolume
        print("Current volume :", currentVolume)
        
def setHotkeys(handle):
    keyboard.add_hotkey('shift+up', volumeUp, args=(handle, 0.05))
    keyboard.add_hotkey('shift+down', volumeDown, args=(handle, 0.05))

def click(hWnd, x, y):
    lParam = win32api.MAKELONG(x, y)
    win32gui.SendMessage(hWnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(hWnd, win32con.WM_LBUTTONUP, None, lParam)

def findSpotifyHandle():
    def callback(wnd, data):
        if win32gui.GetClassName(wnd) == "Chrome_WidgetWin_0" and len(win32gui.GetWindowText(wnd)) > 0:
            windows.append(wnd)
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

def playingNow(wnd):
    global playingEx
    while 1:
        titleNow = win32gui.GetWindowText(wnd)
        if playingEx != titleNow:
            print(titleNow)
            playingEx = titleNow


if __name__ == "__main__":
    sessionHandle, volumeHandle = findSpotify()
    currentVolume = volumeHandle.GetMasterVolume()
    print("Current volume :", currentVolume)
    setHotkeys(volumeHandle)
    wnd = findSpotifyHandle()[0]
    playingNow(wnd)