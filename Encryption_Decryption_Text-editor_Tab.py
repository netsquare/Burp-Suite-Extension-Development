####################################
# NSConclave2023 Presentation: Unleashing the Full Potential of Burp Suite with Extension Development for Enhanced Penetration Testing
# Desc: Burp Suite Extension for Create a Custom Text Editor Tab which will Decrypt the Encrypted data and allow user to modify the data on the Fly. After modification, it will automatically Encrypt the data.
# Developed By: J. Jogal (@j_jogal_545)
##############################


# Burp Imports
from burp import IBurpExtender
from burp import IMessageEditorTabFactory
from burp import IMessageEditorTab
from burp import IParameter

# Java dependency imports
import java.util.Base64
import java
from array import array

# Python dependency imports
import json
import os 
import sys.path as path
from exceptions_fix import FixBurpExceptions  # To show erros prettier
import sys

# Encryption Decryption classes imports (from Java or Python code)
import AesUtil


class BurpExtender(IBurpExtender, IMessageEditorTabFactory):
    
    def	registerExtenderCallbacks(self, callbacks):
        # keep a reference to our callbacks object
        self._callbacks = callbacks
        
        # obtain an extension helpers object
        self._helpers = callbacks.getHelpers()
        
        # set our extension name
        callbacks.setExtensionName("Decryption-Encryption Tab")
        
        # register ourselves as a message editor tab factory
        callbacks.registerMessageEditorTabFactory(self)

        # jj custom for better debugging
        sys.stdout = callbacks.getStdout()

        
    # implement IMessageEditorTabFactory
    def createNewInstance(self, controller, editable):
        # create a new instance of our custom editor tab
        return EncDecTab(self, controller, editable)
        
# 
# class implementing IMessageEditorTab
#

class EncDecTab(IMessageEditorTab):
    def __init__(self, extender, controller, editable):
        self._extender = extender
        self._editable = editable
        
        # create an instance of Burp's text editor, to display our decrypted data
        self._txtInput = extender._callbacks.createTextEditor()
        self._txtInput.setEditable(editable)

        
    #
    # implement IMessageEditorTab
    #

    def getTabCaption(self):
        return "Decryption-Encryption Tab"
        
    def getUiComponent(self):
        return self._txtInput.getComponent()
        
    def isEnabled(self, content, isRequest):
        r = self._extender._helpers.analyzeRequest(content)
        headers = r.getHeaders()
        body = content[r.getBodyOffset():]

        # return isRequest and not body is None
        return not body is None
        
        #setMessage is used for send data to our custom tab.
    def setMessage(self, content, isRequest):
        if content is None:
            # clear our display
            self._txtInput.setText(None)
            self._txtInput.setEditable(False)
        
        else:
			r = self._extender._helpers.analyzeRequest(content)
			headers = r.getHeaders()
			body = content[r.getBodyOffset():]
            
            # retrieve the data parameter
            # parameter = self._extender._helpers.getRequestParameter(content, "parameter_name")
            
            ###### Logic for Decryptoin #######
			data = self._extender._helpers.urlDecode(body)

			aesUtil =  AesUtil(128, 1000)

			decodedData = java.util.Base64.getDecoder().decode(data)
			decodedData = bytearray(decodedData)
			print(decodedData)


			s = str(decodedData.split("::")[1])
			# print("s: "+ s)
			iv = str(decodedData.split("::")[0])
			# print("iv: "+ iv)
			ciphertext = str(decodedData.split("::")[2])

			dataFinal = aesUtil.decrypt(s, iv, "1234567891234567", ciphertext);
			print("decrypted data: " + dataFinal)

			self._txtInput.setText(dataFinal)
			self._txtInput.setEditable(self._editable)
        
        # remember required data to use in other methods
        self._currentMessage = content
        self._headers = headers
        self._s = s
        self._iv = iv
        self._ciphertext = ciphertext
    
        #getMessage is used for retrieve data from custom tab.
    def getMessage(self):
        # determine whether the user modified the deserialized data
        if self._txtInput.isTextModified():
            # reserialize the data
            text = self._txtInput.getText()
            # print "Encrypted from getMessage:"

            string_text = self._extender._helpers.bytesToString(text)
            print "msg in getmsg: "+ string_text

            ##### Logic for Re Encryption ##########
            aesUtil =  AesUtil(128, 1000)

            encyptedData = aesUtil.encrypt(self._s, self._iv , "1234567891234567", string_text)
            encryptedData_full_aes = java.util.Base64.getEncoder().encodeToString((self._iv+"::"+self._s+"::"+encyptedData))
            print("Encrypted data: " + encryptedData_full_aes)

            input = self._extender._helpers.urlEncode(encryptedData_full_aes)
            

            # self.txtInput.setText(self._helpers.buildHttpMessage(headers, body))
            return self._extender._helpers.buildHttpMessage(self._headers, input)
            
            # return self._extender._helpers.updateParameter(self._currentMessage, self._extender._helpers.buildParameter("parameter_name", input, IParameter.PARAM_BODY))
            
        else:
            return self._currentMessage
    
    def isModified(self):
        return self._txtInput.isTextModified()
    
    def getSelectedData(self):
        return self._txtInput.getSelectedText()

#To show erros prettier
FixBurpExceptions()