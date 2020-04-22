import json
import socket

def recvall(sock, count):
    data = bytearray()
    while len(data) < count:
        pack = sock.recv(count-len(data))
        #print('recieved {0} bytes'.format(len(pack)))
        if  not pack:
            return None
        data.extend(pack)
    return data

def print_cards(json_cards):
    for i in zip(json_cards['cards'],range(len(json_cards['cards']))):
        print('{}.\nstrength:{}\nagility:{}\nintelligence:{}'.format(i[1],i[0]['s'],i[0]['a'],i[0]['i']))
		
def main():
	sock = socket.socket()
	sock.connect(('localhost', 9090))
	print('waiting for game start...')
	ab = recvall(sock,8) #1
	player_id = int.from_bytes(ab, byteorder='big', signed=False)
	print('you player number {}'.format(player_id+1))

	finished=False
	result=0
	round_counter=1

	while not finished:
		json_len = recvall(sock,8) #2
		a = int.from_bytes(json_len, byteorder='big', signed=False )
		raw_data = recvall(sock, a) #3
		cards = json.loads(raw_data.decode('utf-8'))
		print('---round {}---'.format(round_counter))
		print_cards(cards)
		while True:
			d=int(input())
			if d>=0 and d<len(cards['cards']):
				break
		sock.sendall(d.to_bytes(8,byteorder='big')) #4
		result_raw = recvall(sock,8) #5
		result = int.from_bytes(result_raw, byteorder='big', signed=True)
		if result==0:
			print('---round draw---')
		if (result>0 and player_id==0) or (result<0 and player_id==1):
			print('---you win a round---')
		if (result>0 and player_id==1) or (result<0 and player_id==0):
			print('---you loose a hero---')

		ab = recvall(sock,8) #6
		finished = not bool.from_bytes(ab,byteorder='big')
		round_counter+=1
	print('game finished')
	if (result>0 and player_id==0) or (result<0 and player_id==1):
		print('you win a game')
	if (result>0 and player_id==1) or (result<0 and player_id==0):
		print('you loose a game')
		
main()