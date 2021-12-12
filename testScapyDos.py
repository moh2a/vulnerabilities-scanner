from scapy.all import *
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether

source_IP = "0.0.0.3"
target_IP = "172.20.10.2"
source_port = 80
i = 1

while True:
    # IP1 = IP(src=source_IP, dst=target_IP)
    # TCP1 = TCP(sport=source_port, dport=80)
    # pkt = IP1 / TCP1
    # s=send(pkt, inter=.001)
    a = Ether() / IP(dst="172.20.10.2") / TCP() / "GET /index.html HTTP/1.0 \n\n"
    print("packet sent ", i,a)
    i = i + 1
