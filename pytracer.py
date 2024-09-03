import socket
import dns.resolver

class Py_Trace:
    def __init__(self):
        pass
    def trace_route(self, url):
        ip = dns.resolver.resolve(url, 'A')
        print(f'resoving to {url}!')
        ipval = ip[0].to_text()

        print(f'DNS Resolved IP: {ipval}')

        try:
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            icmp_socket.bind(('', 0))
            icmp_socket.settimeout(1)
        except socket.error as e:
            print(f"Socket creation failed: {e}")
            return
        port = 33435
        message = "hello"
        message_bytes = message.encode('utf-8') 
        udp_socket.settimeout(1)
        for ttl in range(1,60):
            udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
            udp_socket.sendto(message_bytes, (ipval, port))
            try:
                recv, addr = icmp_socket.recvfrom(1024)
                if addr == ipval:
                    print(f'{ttl} arrived at {ipval}')
                    break
            except socket.error as s:
                print(f"Socket Error: {s}")
                print(f"{ttl} {addr}")
                if addr == ipval:
                    print(f'arrived at {ipval}')
                    break
    
                