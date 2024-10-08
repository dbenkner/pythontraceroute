import socket
import dns.exception
import dns.resolver
import time
import math
import struct
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
        print(f'trace route to {url} ({ipval}), 60 hops max, 32 byte packet')
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
        for ttl in range(1,61):
            total_time = ['','','']
            for i in range(0,3):
                st = time.time()
                addr = ('','')
                hopurl = ''
                udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
                udp_socket.sendto(message_bytes, (ipval, port))
                try:
                    recv, addr = icmp_socket.recvfrom(1024)
                    # check for icmp header
                    icmp_header = recv[20:28]
                    type,code,checkcum,packetID,sequence = struct.unpack('bbHHh',icmp_header)
                    udp_payload = recv[44:48]
                    dest_ip = socket.inet_ntoa(struct.unpack('!4s',udp_payload)[0])
                    if self.verify_packet(type,code,ipval,dest_ip):
                        et = time.time()
                        total_time[i] = f'{round((et-st) *1000, 3)} ms'
                        try:
                            hopurl = f'({socket.gethostbyaddr(addr[0])[0]})'
                        except:
                            hopurl = f'({addr[0]})'
                except socket.timeout as t:
                    total_time[i] = "*"
                    
                except socket.error as s:
                    print(f"Socket Error: {s}")
                    print(f"{ttl} {addr[0]}")
            ttl_str = f'{ttl}'
            print(f'{ttl_str.rjust(2)} {addr[0]} {hopurl} {total_time[0]} {total_time[1]} {total_time[2]}')
            if addr[0] == ipval:
                break
        icmp_socket.close()
        udp_socket.close()
    @staticmethod
    def verify_packet(type,code,dest_ip,dest_ip_from_udp):
        if type == 11 and code == 0 and dest_ip_from_udp == dest_ip:
            return True
        if dest_ip == dest_ip_from_udp:
            return True
        return False
                