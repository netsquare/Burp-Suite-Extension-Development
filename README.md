# Burp-Suite-Extension-Development
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
