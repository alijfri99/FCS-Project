iptables -F
#iptables -P INPUT DROP


ipset create iranset hash:net
ipset -N iranset nethash

while read p; do
  ipset add iranset "$p"
done < iran_ips.txt

iptables -A INPUT -m set ! --match-set iranset src -j DROP
#iptables -I INPUT -m set --match-set myset src -j ACCEPT