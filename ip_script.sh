#!/usr/bin/bash
ipset create ips hash:net
while read line; do
 ipset add ips $line
  echo "$line"
done < iran_ips.txt
iptables -A INPUT -m set --match-set ips src -j ACCEPT

iptables -A INPUT -p tcp -s 192.168.0.0/16 -j ACCEPT
iptables -A INPUT -p tcp -s 127.0.0.0/8 -j ACCEPT

iptables -A INPUT -p all -j DROP
