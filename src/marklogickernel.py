from ipykernel.kernelbase import Kernel

from connection import MLRESTConnection

class MarkLogicKernel(Kernel):
    implementation = 'MarkLogic'
    implementation_version = '1.0'
    language = 'xquery'  # will be used for
                         # syntax highlighting
    language_version = '3.6'
    language_info = {'name': 'marklogic',
                     'mimetype': 'application/xquery',
                     'extension': '.xqy',
                     'codemirror_mode':  { "name": "xquery" },
                     'pygments_lexer' : 'xquery'}
    banner = "MarkLogic Kernel"
    
 
    
    def __init__(self, **kwargs):
        super(MarkLogicKernel, self).__init__(**kwargs)
        self._con = MLRESTConnection()
       
    def do_execute(self, code, silent,
                   store_history=True,
                   user_expressions=None,
                   allow_stdin=False):

        #TODO Process magics
        #magics all start with %
        #find them and remove from code
        code_lines = code.splitlines()
        magic_lines = []
        for i, line in enumerate(code_lines):
            if line.startswith("%"):
                magic_lines.append(line )
                del code_lines[i]
                
        #could do this in code above
        for line in magic_lines:
            self._con.magics(line) 
        
        #Call REST with code
        txt = self._con.call_rest("\n".join(code_lines))
        #txt += str(self.session.session) + "\n"
        #txt += str(self.shell_streams) + "\n"
   
        # Send data to front-end 
        if txt is not None:
            if not silent:
                self._send(txt)
        
        # We return the execution results.
        return {'status': 'ok',
                'execution_count':
                    self.execution_count,
                'payload': [],
                'user_expressions': {},
               }
    
    #Send data - text for now 
    def _send( self, txt):
        content = {
            'execution_count': self.execution_count, 
            'data': {'text/plain' : txt ,
             'application/xml': txt},
              'metadata' : {} }
        self.send_response(self.iopub_socket,'execute_result', content)
    
    
if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(
        kernel_class=MarkLogicKernel)