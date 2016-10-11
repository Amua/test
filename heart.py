#coding: utf-8

import socket
import select
import threading

class Server(object):
    
    def __init__(self, port=6000):
        self.clientmap = {}
        self.outputs = []      
        self.timeout = 6
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', port))   
        self.sock.listen(20)         
        
    def heart_worker(self, *args, **kwargs):
        print 'Start thread successfull.'         
    
    
    def run(self):        
        inputs = [self.sock]        
        thread = threading.Thread(target=self.heart_worker, args=(self,))  
        thread.start() 
                              
        while True:
            try:
                readable, writeable, exceptional = select.select(
                                      inputs, self.outputs, inputs, self.timeout)
            except select.error, e:                
                break            
            if not(readable or writeable or exceptional):
                continue       
            
            for sock in readable:
                if sock is self.sock:
                    client, addr = self.sock.accept()           
                    client.setblocking(0)
                    inputs.append(client)
                    self.clientmap[client] = addr           
                else:
                    try:                        
                        data = sock.recv(1024)                         
                        if data == 'Fuck':
                            pass
                        print self.clientmap[sock], data
                    except socket.error, e:
                        self.clientmap.pop(sock)
                        inputs.remove(sock)                        
                        sock.close()    
            
            for sock in writeable:
                pass            
            for sock in exceptional:
                pass 
        self.sock.close()                           

if __name__ == '__main__':
    server = Server()
    server.run()
