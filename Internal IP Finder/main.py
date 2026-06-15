from burp import IBurpExtender, IExtensionHelpers, IHttpListener
import re

class BurpExtender(IBurpExtender, IExtensionHelpers, IHttpListener):
  
  def registerExtenderCallbacks(self, callbacks):
    self. callbacks = callbacks
    self. helpers = callbacks.getHelpers()
    callbacks.setExtensionName("Internal IP Detector")
    callbacks.registerHttpListener(self)
    print("Internal IP Detector v1.0 Added!")
    print("")
    print("Following Internal IPs have been detected:")
  
  def processHttpMessage(self, tool, is_request, content):
    if not is_request:
      response = self. helpers.bytesToString(content.getResponse())
      pattern = r"\b(?:10(?:\.(?:25[0-5]|2[0-4][0-9]|1[0-9]{1,2}|[0-9]{1,2})){3}|(?:(?:172\.(?:1[6-9]|2[0-9]|3[01]))|192\.168)(?:\.(?:25[0-5]|2[0-4][0-9]|1[0-9]{1,2}|[0-9]{1,2})){2})\b"
      finding = re.findall(pattern, response)
      if finding:
        for x in finding:
          print(x)