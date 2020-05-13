import logging
import requests
from requests.auth import HTTPDigestAuth
from requests_toolbelt.multipart import decoder

# ----------------------------------------------------------------------

class ConfigStruct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)


# ----------------------------------------------------------------------

class MLRESTConnection( object ):

    def __init__( self):
        self.cfg = ConfigStruct( host='localhost', port='8000', user='admin', password='admin', scheme='xquery', action='eval', param=None)

    def call_rest(self,code):
        
        if self.cfg.action == 'eval':
            txt = self._eval_code(code) 
        if self.cfg.action == 'install':
            txt = self._install_rest_ext(code)
        if self.cfg.action == 'module':
            txt = self._install_module(code)      
        return txt
    
    
    def _eval_code(self,code):
        session = requests.session()
        session.auth = HTTPDigestAuth(self.cfg.user,self.cfg.password)
        payload = {self.cfg.scheme: code}
        logging.info(code)

        uri = 'http://%s:%s/v1/eval' % (self.cfg.host,self.cfg.port)

        r = session.post(uri, data=payload)

        txt = u''
        txt += str(r.status_code) + "\n"
        if r.status_code == 200:
            multipart_data = decoder.MultipartDecoder.from_response(r)
            for part in multipart_data.parts:               
                ctype = part.headers[b'content-type'].decode('utf-8')
                raw = part.content.decode('utf-8') 
                txt += raw + "\n"
        else:
            txt += r.json()["errorResponse"]["message"]
        return txt
  
    def _install_rest_ext(self,code):
        session = requests.session()
        session.auth = HTTPDigestAuth(self.cfg.user,self.cfg.password)
        payload = code
        #install the code as a REST ext 
        uri = 'http://%s:%s/v1/config/resources/%s' % (self.cfg.host,self.cfg.port,self.cfg.param)
        headers = {'Content-type': 'application/xquery'}
        r = session.put(uri, data=payload, headers=headers)
 
        txt = u''
        txt += str(r.status_code) + "\n"
        if r.status_code == 204:
            txt += 'Installed' + "\n"
            #reset to eval 
            self.cfg.action = 'eval'
        else:
            txt += r.json()["errorResponse"]["message"]
        return txt
    
    def _install_module(self,code):
        session = requests.session()
        session.auth = HTTPDigestAuth(self.cfg.user,self.cfg.password)
        payload = code
        #install the code as a REST ext 
        uri = 'http://%s:%s/v1/ext/%s' % (self.cfg.host,self.cfg.port,self.cfg.param)
        headers = {'Content-type': 'application/xquery'}
        r = session.put(uri, data=payload, headers=headers)
 
        txt = u''
        txt += str(r.status_code) + "\n"
        self.cfg.action = 'eval'
        if r.status_code == 201:
            txt += 'Installed' + "\n"
        elif r.status_code == 204:
            txt += 'Updated' + "\n"   
        else:
            txt += r.json()["errorResponse"]["message"]
        return txt
  
    
    def magics(self,line):
        cmd, param = line.split(None, 1)
        cmd = cmd[1:].lower()
        # TODO Just endppoint at the mo
        if cmd == 'endpoint':
            r = requests.utils.urlparse(param)
            self.cfg = ConfigStruct( host=r.hostname, port=r.port, user=r.username, password=r.password, scheme=r.scheme, action='eval', param=None)
            #return ['Endpoint set to: {}', param], 'magic'
        if cmd == 'install':
            self.cfg.action= 'install'
            self.cfg.param= param
        if cmd == 'module':
            self.cfg.action= 'module'
            self.cfg.param= param    
        return None


    