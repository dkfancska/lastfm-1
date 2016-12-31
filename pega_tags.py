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


def crawler_tags():
	arq = open("bandas_tags_crawleadas.txt","wb")

	# dado o vetor de bandas
	#arq_bandas = open("bandas_crawleadas.txt", "rb").readlines()
	arq_bandas = ["Coldplay", "David Bowie", "Red Hot Chili Peppers", "Adele", "Queen", "Radiohead", "Nirvana", "Major Lazer", "Sia", "Ed Sheeran", "Foo Fighters", "Rihanna", "The Beatles", "The Rolling Stones", "Daft Punk", "Robin Schulz", "Linkin Park", "Calvin Harris", "Muse", "Metallica", "The Weeknd", "Johnny Cash", "Florence + the Machine", "Michael Jackson", "Green Day", "Eminem", "Bob Dylan", "Pink Floyd", "Ellie Goulding", "Kings of Leon", "Lana Del Rey", "David Guetta", "Drake", "Avicii", "The Cure", "Kygo", "Moby", "System of a Down", "Bon Iver", "K.I.Z.", "Imagine Dragons", "Mumford & Sons", "AnnenMayKantereit", "Deichkind", "The Killers", "Felix Jaehn", "The White Stripes", "Sido", "Depeche Mode", "Justin Bieber"]
	vet_bandas = set()
	for banda in arq_bandas :
		vet_bandas.add( banda )
	#arq_bandas.close()

	banda_tag = {}
	for banda in vet_bandas :
		# http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist=rammstein&api_key=3cfbe52ae6a18a925c18e50940817b58&format=json
		resultado = executa_requisicao({"method": "artist.gettoptags", "artist": banda, "format": "json"})
		try:
			tag_vet = []
			for tag in resultado["toptags"]["tag"]:
				tag_vet.append(tag['name'])
			#print( banda )
			#print( tag_vet )
		except TypeError:
			print(resultado)
			continue
		banda_tag[banda] = tag_vet
	
	
	for banda,tags in banda_tag.items():
		try:
			arq.write(bytearray( banda + "  ","UTF-8"))
			for tag in tags:
				arq.write(bytearray( tag + "\t","UTF-8"))
			arq.write( bytearray( "\n","UTF-8") )
		except UnicodeEncodeError:
			arq.write(banda.encode("UTF-8") + "  ".encode("UTF-8"))
			for tag in tags:
				arq.write(tag.encode("UTF-8") + "\t".encode("UTF-8"))
			arq.write( "\n".encode("UTF-8") )
	arq.close()
	


def crawler_bandas():
	arq = open("bandas_crawleadas.txt","wb")
	#http://ws.audioscrobbler.com/2.0/?method=geo.gettopartists&country=germany&api_key=3cfbe52ae6a18a925c18e50940817b58&format=json
	resultado = executa_requisicao({"method": "geo.gettopartists", "country": "germany", "format": "json"})
	vet = resultado["topartists"]["artist"]
	try:
		for itens in vet:
			try:
				arq.write(bytearray( itens['name'] +"\n","UTF-8"))
			except UnicodeEncodeError:
				arq.write(itens['name'].encode("UTF-8")+"\n".encode("UTF-8"))
	except TypeError:
		print(resultado)
		
	arq.close()

def pega_bandas():
	read_arq = open("usuarios_crawleados.txt","rb")
	write_arq = open("usuario_banda.txt","wb")
	read_arq.close()
	write_arq.close()


def main():
	#crawler_bandas()
	#pega_bandas()
	crawler_tags()

if __name__ == "__main__":
	main()



# Top Artistas de um usuário
# http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user=Babs_05&api_key=3cfbe52ae6a18a925c18e50940817b58&format=json

# Pegar Amigos de um usuário
# http://ws.audioscrobbler.com/2.0/?method=user.getfriends&user=rj&api_key=3cfbe52ae6a18a925c18e50940817b58&format=json

# Pegar as TopTags de uma banda
# http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist=rammstein&api_key=3cfbe52ae6a18a925c18e50940817b58&format=json