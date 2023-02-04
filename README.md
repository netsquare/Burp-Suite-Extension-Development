# Burp Suite Extension Development
Unleashing the Full Potential of Burp Suite with Extension Development for Enhanced Penetration Testing

> **Presentation URL:** https://www.slideshare.net/NSCONCLAVE/burp-suite-extension-development-255681385

### Burp Suite API documentation 
**Extender API:**
https://github.com/PortSwigger/burp-extender-api

**JavaDoc:** 
https://portswigger.net/burp/extender/api/


## Helpful Snippets

#### Modify data of Full request body
```
# Get Data:
r = self._helpers.analyzeRequest(content)
headers = r.getHeaders()
body = content[r.getBodyOffset():] 

# Your logic code

# Return Data:
self.txtInput.setText(self._helpers.buildHttpMessage(headers, body))
```

#### Modify data of any Parameter
```
# Get Data:
parameter = self._extender._helpers.getRequestParameter(content, "param_name")
data = self._extender._helpers.urlDecode(parameter.getValue())

# Your logic code

# Return Data:
self.txtInput.setText(self._helpers.buildHttpMessage(headers, body))
# or
return self._extender._helpers.updateParameter(self._currentMessage, self._extender._helpers.buildParameter("parameter_name", input, IParameter.PARAM_BODY))
```

#### Modify data of any Header
```
if messageIsRequest:
     request = messageInfo.getRequest()
     headers = request.getHeaders()
     headers = list(headers)
           for i, header in enumerate(headers):
                if header.startswith("Authorization: "):
                    headers[i] = "Authorization: Basic admin:password"
                    break
                else:
                    headers.append("Authorization: Basic admin:password")
     messageInfo.setRequest(self._helpers.buildHttpMessage(headers, request.getRequest()[request.getBodyOffset():]))
```

