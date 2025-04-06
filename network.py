import os
import time
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

def wait_for_interface(host, interface, timeout=10):
    """Aspetta che un'interfaccia venga creata per un host"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        output = host.cmd(f"ip link show {interface}")
        if interface in output:
            return True
        time.sleep(1)
    return False

def generate_traffic():
    """Genera traffico tra gli host in modo strutturato"""
    print("*** Ping tra tutti gli host")
    for h in hosts:
        for target in hosts:
            if h != target:
                print(f"{h.name} ping {target.name}")
                h.cmd(f"ping -c 2 {target.IP()} &")
                time.sleep(1)
    
    print("*** Test Iperf da h2 verso tutti gli altri host")
    for target in hosts:
        if target != hosts[1]:  # Evita che h2 si test da solo
            print(f"h2 -> {target.name} con iperf")
            hosts[1].cmd(f"iperf -c {target.IP()} -t 3 &")
            time.sleep(1)
    
    print("*** Traffico TCP su porte specifiche")
    hosts[2].cmd("nc -l 5001 &")
    time.sleep(1)
    hosts[4].cmd("echo 'Hello TCP!' | nc 10.0.0.3 5001 &")
    time.sleep(2)
    
    print("*** Simulazione HTTP da h5 a h7")
    hosts[4].cmd("wget -O /dev/null http://10.0.0.7 &")
    time.sleep(2)

def setup_network():
    net = Mininet(controller=RemoteController, switch=OVSSwitch)
    
    print("*** Aggiunta del controller")
    c0 = net.addController('c0')
    
    print("*** Aggiunta degli switch")
    s1, s2, s3, s4 = [net.addSwitch(f's{i}') for i in range(1, 5)]
    
    print("*** Aggiunta degli host")
    global hosts
    hosts = [net.addHost(f'h{i}', ip=f'10.0.0.{i}') for i in range(1, 8)]
    
    print("*** Creazione dei collegamenti")
    for h in hosts[:4]:
        net.addLink(h, s1)
    for h in hosts[4:]:
        net.addLink(h, s2)
    
    net.addLink(s1, s3)
    net.addLink(s2, s3)
    net.addLink(s3, s4)
    
    print("*** Avvio della rete")
    net.start()
    time.sleep(5)
    
    print("*** Avvio della cattura pacchetti su host e switch")
    for h in hosts:
        iface = f"{h.name}-eth0"
        if wait_for_interface(h, iface):
            h.cmd(f"tcpdump -i {iface} -w /tmp/{h.name}_traffic.pcap &")
        else:
            print(f"Errore: Interfaccia {iface} non disponibile!")

    # Cattura pacchetti sugli switch OVS
    for sw in [s1, s2, s3, s4]:
        for intf in sw.intfs.values():
            iface = intf.name  # Nome dell'interfaccia dello switch
            if "eth" in iface:  # Evita interfacce di loopback
                print(f"Avvio tcpdump su {iface}")
                os.system(f"sudo tcpdump -i {iface} -w /tmp/{iface}_traffic.pcap &")
        
    print("*** Generazione del traffico")
    generate_traffic()
    time.sleep(10)
    
    print("*** Stop della cattura pacchetti")
    for h in hosts:
        h.cmd("pkill -x tcpdump")
    for sw in [s1, s2, s3, s4]:
        os.system("sudo pkill -x tcpdump")
    
    print("*** CLI di Mininet per test aggiuntivi")
    CLI(net)
    
    print("*** Arresto della rete")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    setup_network()

