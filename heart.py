#coding: utf-8
import time
import socket
import select
import threading

class Server(object):
    
    def __init__(self, port=6000):
        self.clientmap = {}
        self.inputs = []
        self.outputs = []      
        self.timeout = 6
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', port))   
        self.sock.listen(20)         
        
    def heart_worker(self, *args, **kwargs):
        print 'Start thread successfull.'              
        while True:
            curtime = time.time()
            for (sock , value) in self.clientmap.items():
                if curtime - value['time'] >= self.timeout:
                    print 'Kill one client.'
                    self.clientmap.pop(sock)
                    self.inputs.remove(sock)                        
                    sock.close()                        
            time.sleep(3)    
    
    def run(self):                       
        thread = threading.Thread(target=self.heart_worker)  
        thread.start() 
        self.inputs = [self.sock]           
                           
        while True:
            try:
                readable, writeable, exceptional = select.select(
                                      self.inputs, self.outputs, self.inputs, 10)
            except select.error, e:                
                break            
            if not(readable or writeable or exceptional):
                continue       
            
            for sock in readable:
                if sock is self.sock:
                    client, addr = self.sock.accept()           
                    client.setblocking(0)
                    self.inputs.append(client)
                    self.clientmap[client] = {'addr': addr}           
                else:
                    try:                        
                        data = sock.recv(1024)                         
                        if data == 'Fuck':
                            self.clientmap[sock]['time'] = time.time()                            
                        print self.clientmap[sock], data
                    except socket.error, e:
                        self.clientmap.pop(sock)
                        self.inputs.remove(sock)                        
                        sock.close()    
            
            for sock in writeable:
                pass            
            for sock in exceptional:
                pass 
        self.sock.close()                           

if __name__ == '__main__':
    server = Server()
    server.run()
