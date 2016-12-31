#-*-encoding: utf-8 -*- 
from json import *
import requests
from requests import get
from urllib.request import urlopen
from hashlib import md5
from login import usuario

HOST = "http://ws.audioscrobbler.com/2.0/?api_key="+usuario['api_key']

def executa_requisicao(params):
	if type(params) is dict:
		params = params.items()
	url = HOST
	for (key,value) in params:
		try:
			url += "&"+key+"="+value
		except TypeError:
			return (False,"Erro nos params")

	raw_response = get(url)
	response = loads(raw_response.content.decode("utf-8"))
	if "error" in response.keys():
		return (False, response["message"])
	return response

def crawler_usuarios():

	print(" << Inicio >> ")

	visitados = set()

	arq = open("seeds.txt","r")
	usuarios_pilha = [x.strip() for x in arq.readlines()]
	arq.close()

	print(" << Leu Arq seed >> ")

	for x in usuarios_pilha:
		visitados.add(x)

	arq = open("users_crawler_lvl_1.txt","r")
	usuarios_pilha = [x.strip() for x in arq.readlines()]
	arq.close()

	print(" << Leu Arq users_crawler_lvl_1 >> ")

	for x in usuarios_pilha:
		visitados.add(x)

	print(" << Iniciar crawler >> len: ", len(usuarios_pilha) ," ")

	usuarios_set = set()
	i = 0
	sem_amigos_set = set()
	no_friends = 0
	for x in usuarios_pilha:

		print("Crawling: ", x)		
		
		resultado = executa_requisicao({"method": "user.getFriends", "user": x, "limit": "500", "page": "1", "format": "json"})

		if resultado is tuple and not resultado[0]:
			print(resultado[1])
			continue
		try:
			for amigo in resultado['friends']['user']:
				#if amigo['name'] not in usuarios_set and amigo['name'] not in usuarios_pilha:
				#	usuarios_set.add(amigo['name'])
				#	usuarios_pilha.append(amigo['name'])
				if amigo["name"] in visitados:
					continue
				visitados.add(amigo["name"])

				usuarios_set.add(amigo['name'])

		except TypeError:
			print(resultado)
			continue
		except KeyError:
			print(" No friends: ",x)
			sem_amigos_set.add(x)
			no_friends += 1

			continue

		i += 1
		print("Itt: ", i, " | Set: ", len(usuarios_set), " | Sem amigos: ", no_friends)

	arq = open("users_crawler.txt", "wb")
	for x in usuarios_set:
		try:
			arq.write(bytearray(x+"\n","UTF-8"))
		except UnicodeEncodeError:
			arq.write(x.encode("UTF-8")+"\n".encode("UTF-8"))
	arq.close()

	arq = open("users_crawler_no_friends.txt", "wb")
	for x in sem_amigos_set:
		try:
			arq.write(bytearray(x+"\n","UTF-8"))
		except UnicodeEncodeError:
			arq.write(x.encode("UTF-8")+"\n".encode("UTF-8"))
	arq.close()


def pega_bandas():
	read_arq = open("seeds.txt","r")
	write_arq = open("usuario_banda.txt","wb")
	i = 0
	for linha in read_arq.readlines():
		if linha:
			resultado = executa_requisicao({"method": "user.getTopArtists", "user": linha.strip(),
										 "limit": "100", "page": "1", "format": "json"})
			if resultado is tuple and not resultado[0]:
				print(resultado[1])
				continue
			registro = linha.strip()+" "
			for banda in resultado["topartists"]['artist']:
				registro += banda['name']+"\t@\t"
			registro += "\n"
			try:
				write_arq.write(bytearray(registro, "UTF-8"))
			except UnicodeEncodeError:
				write_arq.write(registro.encode("UTF-8"))
			i += 1
			if i % 10 == 0: print(i)			
	read_arq.close()
	write_arq.close()


def main():
	#crawler_usuarios()
	#pega_bandas()
	crawler_usuarios()

if __name__ == "__main__":
	main()



# Top Artistas de um usuário
# http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user=Babs_05&api_key=3cfbe52ae6a18a925c18e50940817b58&format=json

# Pegar Amigos de um usuário
# http://ws.audioscrobbler.com/2.0/?method=user.getfriends&user=rj&api_key=3cfbe52ae6a18a925c18e50940817b58&format=json

# Pegar as TopTags de uma banda
# http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist=rammstein&api_key=3cfbe52ae6a18a925c18e50940817b58&format=json
