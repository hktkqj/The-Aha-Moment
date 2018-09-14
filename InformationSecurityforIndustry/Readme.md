Readme.md - description for SCADA data simulation

File structure :
|---EthernetSimulation.py
|---SCADA client.py
|---SCADA server.py

EthernetSimulation.py 
	A basic string simulator for Ethernet data. Used in server&client.
	EthernetData(OriginalAdd, DestinationAdd, TransportData):
		return a binary string of Ethernet data
	EthernetDataDecoder(EthernetData) :
		get data from an EthernetData string
		
SCADA server.py :
	Localhost based server, listening port 10086, receive EthernetData from client.
	Show decoded data.
	***Run "SCADA server.py" first to establish server, select "Accept" if Firewall warned.
	
SCADA client.py :
	A client send data to "SCADA server".
	Generate random integer(from 1 to 500) per second, send to server as simulate data.
