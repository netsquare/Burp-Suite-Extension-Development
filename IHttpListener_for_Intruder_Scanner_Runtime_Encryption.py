##########################################
# NSConclave2023 Presentation: Unleashing the Full Potential of Burp Suite with Extension Development for Enhanced Penetration Testing
# Description: Burp Suite Extension for Create a IHttpListener, which will Encrypt the every request data from Intruders, Scanners or from other extensions and forward the request to server.
# Note: User need to provide Decrypted data into the intruder or scanner (Decrypted data from "Text-editor_Tab_Runtime_Encryption_Decryption.py" Extension), and mark the Positions for attack. If Response is also encrypted then user can analyze it with first Extension(Text-editor_Tab_Runtime_Encryption_Decryption.py).
# Presentation URL: https://www.slideshare.net/NSCONCLAVE/burp-suite-extension-development-255681385
#
# Developed by: J. Jogal (@j_jogal_545)
##########################################


# Burp Imports
from burp import IBurpExtender
from burp import IHttpListener

# Java dependency imports
import java.util.Base64
import java
from array import array

# Python dependency imports
import json
import os 
import sys.path as path
from exceptions_fix import FixBurpExceptions # To show errors prettier
import sys

# Encryption Decryption classes imports (from Java or Python code)
import AesUtil


class BurpExtender(IBurpExtender, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        
        callbacks.setExtensionName("Intruder-Scanner HTTP Listener")
        callbacks.registerHttpListener(self)

        # To show errors prettier
        sys.stdout = callbacks.getStdout()

    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        #get tool flags value from: https://portswigger.net/burp/extender/api/index.html?burp/package-summary.html
        tool_name = self._callbacks.getToolName(toolFlag)

        # Condition: when to execute this extension for encryption
        if tool_name != "Proxy" and tool_name != "Repeater" and messageIsRequest:
        	request = messageInfo.getRequest()

        	# print(self._helpers.bytesToString(request))
        	r = self._helpers.analyzeRequest(request)
        	headers = r.getHeaders()
        	body = request[r.getBodyOffset():]

        	# parameter = self._extender._helpers.getRequestParameter(content, "parameter_name")

        	data = self._helpers.urlDecode(body)

        	string_text = self._helpers.bytesToString(data)

        	s = "7d4b31c653d6d982e713a2005d81a864"
        	iv = "2b7cf239455c50a4032236156d09f177"
        	
        	#Encrypting all the requests
        	aesUtil =  AesUtil(128, 1000)

        	encyptedData = aesUtil.encrypt(s, iv , "1234567891234567", string_text)
        	encryptedData_full_aes = java.util.Base64.getEncoder().encodeToString((iv+"::"+s+"::"+encyptedData))
        	# print("Encrypted data: " + encryptedData_full_aes)
        	# input = self._helpers.urlEncode(encryptedData_full_aes)

        	# self.txtInput.setText(self._helpers.buildHttpMessage(headers, body))

        	new_request = self._helpers.buildHttpMessage(headers, encryptedData_full_aes)
        	messageInfo.setRequest(new_request)

# To show errors prettier
FixBurpExceptions()
