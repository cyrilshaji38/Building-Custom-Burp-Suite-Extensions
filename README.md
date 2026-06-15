# Building Custom Burp Suite Extensions
Welcome, ethical hackers and coding enthusiasts! Have you ever wished there was a tool that could save the time and effort you put into doing that one repetitive testcase on Burp Suite. Let me introduce you to the world of Burp Suite extensions in Python!
Burp Suite provides an extensive library of functions that can be used in our python scripts to create our very own custom burp extensions. Join me in coding a simple burp extension that can detect and report the Internal IP addresses disclosed by our web application responses.

## Setting up the environment:
We need to setup Burp Suite with Jython environment, which provides implementations of Python in Java.

1. Download Jython Standalone file: https://repo1.maven.org/maven2/org/python/jython-standalone/2.7.2/jython-standalone-2.7.2.jar 
2. On Burp Suite, go to Settings > Extensions > Python environment > Select file. Browse and upload the Jython Standalone JAR file we downloaded.

## Code the extension:
Now let's make a python file and start writing our program.
First, we must import the basic modules:
```
from burp import IBurpExtender, IExtensionHelpers
```

All Burp extensions must implement the IBurpExtender interface. The IExtensionHelpers interface contains several helper methods, which extensions can use to assist with various common tasks that arise for Burp extensions.
Now we define a class named BurpExtender that inherits from the IBurpExtender and IExtensionHelpers interfaces. This indicates that our class will implement the methods specified by these interfaces.
```
class BurpExtender(IBurpExtender, IExtensionHelpers, IHttpListener):
```

Let's define our first method which will be called by Burp on loading our extension. It's used to set up your extension and register it with Burp Suite's callback objects.
```
def registerExtenderCallbacks(self, callbacks):
  self. callbacks = callbacks
  self. helpers = callbacks.getHelpers()
  callbacks.setExtensionName("Internal IP Detector")
  print("Internal IP Detector v1.0 Added!")
```

We have stored the callbacks and an instance of IExtensionHelpers using the getHelpers() method, in instance variables for future use. The third line sets the name of our extension as "Internal IP Detector", which will be displayed in Burp Suite's UI. The print() statement prints a message to the output console of Burp Suite when the extension is loaded.
For our extension, we want all the internal IP addresses that are found on our web application responses to be reported. So, we need access to the responses falling into Burp's HTTP History tab. Let's make use of one of the functions from Burp's API library for that.
```
def processHttpMessage(self, tool, is_request, content):
```

This method is called by Burp Suite for each HTTP message (request/response) that's intercepted during testing. The tool flag is used to determine which tool sent the request. It could be from the repeater, intruder, scanner, etc. The is request flag helps determine if the current message is a request. The content variable stores the entire message. Don't forget to import the IHttpListener interface and inherit it in the BurpExtender class definition as well.
```
from burp import IBurpExtender, IExtensionHelpers, IHttpListener
class BurpExtender(IBurpExtender, IExtensionHelpers, IHttpListener):
```

Now we can code the main logic of our custom extension!
```
def processHttpMessage(self, tool, is_request, content):
  if not is_request:
    response = self. helpers.bytesToString(content.getResponse())
    pattern = r"\b(?:10(?:\.(?:25[0-5]|2[0-4][0-9]|1[0-9]{1,2}|[0-9]{1,2})){3}|(?:(?:172\.(?:1[6-9]|2[0-9]|3[01]))|192\.168)(?:\.(?:25[0-5]|2[0-4][0-9]|1[0-9]{1,2}|[0-9]{1,2})){2})\b"
    finding = re.findall(pattern, response)
    if finding:
      for x in finding:
        print(x)
```

The first line checks if the current message is a response, since we don't want to be working with requests in our case. Then the response content is converted from bytes to a string. This will make it easier to work with the response content. The pattern we have made use of is a regular expression that detects IP addresses between (10.0.0.0 to 10.255.255.255), (172.16.0.0 to 172.31.255.255) and (192.168.0.0 to 192.168.255.255). Finally, the built-in python re module (Make sure to import that module as well!) is used to find all occurrences of such patterns in the responses and printed out to Burp's output console.

<img width="959" height="562" alt="extension working" src="https://github.com/user-attachments/assets/d362e37b-bbea-411e-9948-18ea57c1b19c" />
