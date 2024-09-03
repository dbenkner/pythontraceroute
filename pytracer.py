import socket
import dns.exception
import dns.resolver
import time
import math
class Py_Trace:
    def __init__(self):
        pass
    def trace_route(self, url):
        try:
            ip = dns.resolver.resolve(url, 'A')
        except:
            print(f'invalid url entry')
            return
        ipval = ip[0].to_text()
        print(f'trace route to {url} ({ipval}), 64 hops max, 32 byte packet')
        try:
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            icmp_socket.bind(('', 0))
            icmp_socket.settimeout(1)
        except socket.error as e:
            print(f"Socket creation failed: {e}")
            return
        port = 33435
        message = "aaaa"
        message_bytes = message.encode('utf-8') 
        udp_socket.settimeout(1)
        for ttl in range(1,60):
            st = time.time()
            udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
            udp_socket.sendto(message_bytes, (ipval, port))
            try:
                recv, addr = icmp_socket.recvfrom(1024)
                et = time.time()
                total_time = round((et - st) * 1000, 3)
                try:
                    hopurl = socket.gethostbyaddr(addr[0])
                except:
                    hopurl = addr
                print(f'{ttl} {addr[0]} ({hopurl[0]}) {total_time}ms')
                if addr[0] == ipval:
                    break
            except socket.timeout as t:
                print(f'{ttl} * * * Request Timed Out!')
            except socket.error as s:
                print(f"Socket Error: {s}")
                print(f"{ttl} {addr[0]}")
        
    
                