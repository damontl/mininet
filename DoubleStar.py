#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.util import dumpNodeConnections
from mininet.link import TCLink, Intf
from subprocess import call

class DoubleStarTopo(Topo):
    def build(self):
    
        #Setting parameters for the link speeds and delay
        linkopts = dict(bw=10, delay='5ms') 
    
        #Creating two switches, one for each star.
        print("*** Adding switches\n")
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
    
        #Creating link between switches
        self.addLink(switch1, switch2, **linkopts)
    
        #Creating hosts for switch 1 and adding links to switch 1
        print("*** Adding hosts for switch 1\n")
        for i in range(1, 5):
            hosts = self.addHost(f'h{i}', cls=Host)
            self.addLink(switch1, hosts, **linkopts)

        #Creating hosts for switch 2 and adding links to switch 2
        print("*** Adding hosts for switch 2\n")
        for i in range(5, 9):
            hosts = self.addHost(f'h{i}', cls=Host)
            self.addLink(switch2, hosts, **linkopts)

        
#Initialising the network
def start_network():
    topo =DoubleStarTopo()
    net = Mininet(topo, switch=OVSKernelSwitch, ipBase='10.0.0.0/8', link=TCLink)
    
    #Setting up and configuring controller
    print( "\n*** Adding controller\n" )
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)
    
    #Starting the network
    print("*** Starting network...\n")
    net.start()
    
    #Starting controller
    print( "*** Starting controllers\n")
    for controller in net.controllers:
        controller.start()
    
    #Starting switches
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    
    #Verifying the hosts and IP addresses are correctly configured
    print("\n*** Hosts and their IP addresses:")
    for host in net.hosts:
        print(host.name, host.IP())
    
    #Viewing links between nodes and switches for debugging and verifying links are correct
    print("\n*** Links between nodes and switches")
    for link in net.links:
        print(link)
    
    #Testing network connectivity
    print( "\n*** Dumping host connections" )
    dumpNodeConnections(net.hosts)
    
    #Verifying packet transmission.
    print( "\n*** Testing network connectivity\n" )
    net.pingAll()
    
    #Starting the command line interface
    CLI(net)
    
    
if __name__ == '__main__':
    setLogLevel( 'info' )
    start_network()
