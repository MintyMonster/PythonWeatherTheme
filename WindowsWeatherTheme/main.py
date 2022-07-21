import yaml
import geopy
from geopy.geocoders import Nominatim
import pyowm
import wx
import wx.adv
import pystray
from PIL import Image, ImageDraw
import sched
import time

with open("config.yml", "r") as yml:
    config = yaml.safe_load(yml)

TRAY_TOOLTIP = 'Weathery Backgrounds'
TRAY_ICON = "sun.png"

owm = pyowm.OWM(config["OWM_key"])
mgr = owm.weather_manager()
loc = Nominatim(user_agent="GetLoc")
getLoc = loc.geocode(config["location"])

def checkWeather():
    observation = mgr.weather_at_coords(lat=getLoc.latitude, lon=getLoc.longitude)
    weather = observation.weather
    print(weather.status)

def checkLoop():
    s = sched.scheduler(time.time, time.sleep)
    s.enter(30, 1, checkWeather())
    s.run()

def createMenuItem(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item

class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.setIcon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.onLeftDown)

    def createMenu(self):
        menu = wx.Menu()
        createMenuItem(menu, 'Site', self.onHello)
        menu.AppendSeparator()
        createMenuItem(menu, 'Exit', self.onExit)
        return menu

    def setIcon(self, path):
        icon = wx.Icon(path)
        self.SetIcon(icon, TRAY_TOOLTIP)

    def onLeftDown(self, event):
        print('Left-Clicked')

    def onHello(self, event):
        print('Hello, world!')

    def onExit(self, event):
        wx.CallAfter(self.Destroy())
        self.frame.Close()

class App(wx.App):
    def onInit(self):
        frame = wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True

def main():
    app = App(False)
    app.MainLoop()

if __name__ == '__main__':
    main()
    checkLoop()

