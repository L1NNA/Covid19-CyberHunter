"""
pip install cefpython3==57.0
"""

from cefpython3 import cefpython as cef
import os
import platform
import subprocess
import sys
import time
from threading import Thread
from datetime import datetime



class CEFBrowser:
    def __init__(self):
        self.browser = None
        self.data = {}

    def start(self):
        def run():
            sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
            # Off-screen-rendering requires setting "windowless_rendering_enabled"
            # option, so that RenderHandler callbacks are called.
            cef.Initialize(settings={"windowless_rendering_enabled": True, "downloads_enabled": False})
            self._create_browser()
            cef.MessageLoop()
            cef.Shutdown()
        t = Thread(target=run)
        t.start()
        time.sleep(3)
        
    
    def ceff_callback(self, tms, val):
        self.data[tms] = val
        
    def _rebind(self):
        bindings = cef.JavascriptBindings(
            bindToFrames=True, bindToPopups=True)
        bindings.SetObject('cefcontroller', self)
        self.browser.SetJavascriptBindings(bindings)
        time.sleep(1)
    
    def _create_browser(self):
        # Create browser in off-screen-rendering mode (windowless mode)
        # by calling SetAsOffscreen method. In such mode parent window
        # handle can be NULL (0).
        parent_window_handle = 0
        window_info = cef.WindowInfo()
        # window_info.SetAsOffscreen(parent_window_handle)
        browser = cef.CreateBrowserSync(window_info=window_info,
                                        url='https://www.google.com')
        
        # browser.SetClientHandler(LoadHandler())
        # browser.SetClientHandler(RenderHandler())
        browser.SendFocusEvent(True)
        # You must call WasResized at least once to let know CEF that
        # viewport size is available and that OnPaint may be called.
        browser.WasResized()
        self.browser = browser
        self._rebind()

    def goto(self, url):
        self.browser.LoadUrl(url)
        

    def dump(self):
        self._rebind()
        tms = time.time()
        self.browser.ExecuteJavascript("function ceff_dump(tms){cefcontroller.ceff_callback(tms, new XMLSerializer().serializeToString(document))}")
        self.browser.ExecuteFunction("ceff_dump", tms)
        qstart = datetime.now()
        while tms not in self.data:
            continue
        val = self.data[tms]
        del self.data[tms]
        return val

    def exit(self):
        self.browser.CloseBrowser()
        cef.QuitMessageLoop()




if __name__ == '__main__':
    brw = CEFBrowser()
    brw.start()
    #brw.goto('https://www.hybrid-analysis.com/recent-submissions?filter=file&sort=^timestamp&page=1')
    #time.sleep(10)
    #print(brw.dump())
    #brw.exit()
    
    