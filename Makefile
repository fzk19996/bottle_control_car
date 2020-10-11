all: 
	g++ -Wall -o server server.cpp -I./ ./TCPServer.cpp -std=c++11 -lpthread