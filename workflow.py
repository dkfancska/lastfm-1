#-*-encoding: utf-8 -*- 
from json import *
import requests
from requests import get
from urllib.request import urlopen
from hashlib import md5
from login import usuario
from networkx import Graph, set_node_attributes, get_node_attributes,generate_gml
from os import listdir

HOST = "http://ws.audioscrobbler.com/2.0/?api_key="+usuario['api_key']

# cada vez que uma banda que está no cache é usada ela é removida e inserida na fila novamente
# quando o cache está cheio, ao inserir um novo elemento o primeiro é removido
# BUGS: diferencia maiusculas de minusculas :'(
cache_bandas = {} 	# formato: { banda : [tags] , ... }
cache_fila = []	
cache_cont = 0
CACHE_MAX = 7000

cache_access = 0
cache_miss = 0

debug_count = 0

def executa_requisicao(params):
	if type(params) is dict:
		params = params.items()
	url = HOST
	for (key,value) in params:
		try:
			value = value.replace("&","%26")
			url += "&"+key+"="+value
		except TypeError:
			print("ERRO: ", key.encode("UTF-8"), value.encode("UTF-8"))
			return (False,"Erro nos params")

	raw_response = get(url)
	try:
		response = loads(raw_response.content.decode("utf-8"))
	except Exception as er:
		log_erros = open("log_erros.txt","ab")
		try:
			log_erros.write(bytearray("ERRO ENCONTRADO\nURL:"+url+"\nMENSAGEM:"+str(type(er))+" "+str(er)+"\n","UTF-8"))
		except UnicodeEncodeError:
			arq.write("ERRO ENCONTRADO\nURL:"+url.encode("UTF-8")+"\nMENSAGEM: "+str(type(er))+" "+str(er).encode("UTF-8")+"\n".encode("UTF-8"))
		log_erros.close()

	try:
		if "error" in response.keys():
			print(url.encode("UTF-8"))
			return (False, response["message"])
	except Exception as er:
		return (False, "Erro no load -> Linha 40")

	return response

def crawler_usuarios():
	arq = open("usuarios_crawleados2.txt","wb")
	max_users = 10**2
	usuarios_pilha = ["rkaustchr"]
	usuarios_set = set(["rkaustchr"])
	while usuarios_set and len(usuarios_set) <= max_users:
		usuario = usuarios_pilha.pop()
		if len(usuarios_set) % 10 == 0: print(len(usuarios_set),max_users)
		resultado = executa_requisicao({"method": "user.getFriends", "user": usuario, "limit": "100", "page": "1", "format": "json"})
		if resultado is tuple and not resultado[0]:
			print(resultado[1])
			continue
		try:
			for amigo in resultado['friends']['user']:
				if amigo['name'] not in usuarios_set and amigo['name'] not in usuarios_pilha:
					usuarios_set.add(amigo['name'])
					usuarios_pilha.append(amigo['name'])
		except TypeError:
			print(resultado)
			continue

	for x in usuarios_set:
		try:
			arq.write(bytearray(x+"\n","UTF-8"))
		except UnicodeEncodeError:
			arq.write(x.encode("UTF-8")+"\n".encode("UTF-8"))
	arq.close()

def pega_tags( bandas ):
	
	global cache_cont

	global cache_access
	global cache_miss

	tags_global = set()
	#arq_banda = open("workflow_detail.txt", "wb")
	for banda in bandas :
		'''
		try:
			arq_banda.write(bytearray( banda +"\n\n","UTF-8"))
		except UnicodeEncodeError:
			arq_banda.write(banda.encode("UTF-8")+"\n\n".encode("UTF-8"))
		'''
		tags_banda = set()

		# Teste cache
		cache = cache_bandas.get(banda)
		cache_access = cache_access + 1
		if ( cache != None ):
			tags_banda = cache #set(cache)

			cache_fila.remove(banda)
			cache_fila.append(banda)

		# se não está no cahce
		else:
			cache_miss = cache_miss + 1

			# http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist=rammstein&api_key=3cfbe52ae6a18a925c18e50940817b58&format=json
			resultado = executa_requisicao({"method": "artist.gettoptags", "artist": banda, "format": "json"})
			try:
				cont = 1;
				for tag in resultado["toptags"]["tag"]:
					#print(" Tags > ", tag["name"], "\n")
					tags_banda.add( tag['name'] )

					'''
					try:
						arq_banda.write(bytearray( "\t"+ tag['name'] +"\n","UTF-8"))
					except UnicodeEncodeError:
						arq_banda.write("\t".encode("UTF-8")+ tag['name'].encode("UTF-8")+"\n".encode("UTF-8"))
					'''

					cont = cont + 1
					if cont > 5:
						break
				
			except TypeError:
				print(resultado)
				continue

			# se o cache está cheio
			if ( cache_cont > CACHE_MAX ):
				cache = cache_fila.pop(0)
				del cache_bandas[cache]
				cache_cont = cache_cont - 1
			
			cache_bandas[banda] = tags_banda
			cache_fila.append(banda)

			cache_cont = cache_cont + 1

		tags_global = tags_global.union( tags_banda )

	'''
	arq_banda.close()
	'''

	global debug_count
	debug_count += 1
	arq_debug = open("debug/cache_all.txt", "wb")
	for i,j in cache_bandas.items():
		
		try:
			arq_debug.write(bytearray("\n["+i+"]\n", "UTF-8"))
		except UnicodeEncodeError:
			arq_debug.write("\n[".encode("UTF-8")+ i.encode("UTF-8")+ "]\n".encode("UTF-8") )

		for k in j:
			try:
				arq_debug.write(bytearray("\t\t" + k + "\n", "UTF-8") )
			except:
				arq_debug.write("\t\t".encode("UTF-8") + k.encode("UTF-8") + "\n".encode("UTF-8"))
	arq_debug.close()

	return tags_global

def pega_bandas( usuario ):
	
	resultado = executa_requisicao({"method": "user.getTopArtists", "user": usuario,
								 "limit": "100", "page": "1", "format": "json"})
	
	if resultado is tuple and not resultado[0]:
		print(resultado[1])

	bandas = set()
	for banda in resultado["topartists"]['artist']:
		#print(" banda > ", banda["name"], "\n")
		bandas.add(banda["name"])
		
	
	return bandas

def monta_subgrafo( usuario ):
	
	arq = open("grafos/subgrafo_"+usuario+".txt","wb")
	#arq2 = open("grafos/subgrafo_geral.txt","ab")
	
	tags = pega_tags( pega_bandas( usuario ) )
	i = 0
	while tags:
		tag = tags.pop()
		for x in tags:
			try:
				arq.write(bytearray(tag + "\t@\t" + x + "\n","UTF-8"))
				#arq2.write(bytearray(tag + "\t" + x + "\n","UTF-8"))
			except UnicodeEncodeError:
				arq.write(tag.encode("UTF-8") + "\t@\t".encode("UTF-8") + x.encode("UTF-8") + "\n".encode("UTF-8"))
				#arq2.write(tag.encode("UTF-8") + "\t".encode("UTF-8") + x.encode("UTF-8") + "\n".encode("UTF-8"))
		i += 1
		if i % 30 == 0: print("tags",i)

	#arq2.write(bytearray("\n\n\n","UTF-8"))
	arq.close()

def percorre_usuarios( usuarios ):
	i = 0
	for usuario in usuarios:
		monta_subgrafo( usuario)
		print(cache_cont)
		print(cache_access, cache_miss)
		i += 1
		if i % 10: print("usuarios",i, usuario)

def carrega_grafo(nome_dataset):
	g = Graph()
	#pesos_verts = {}
	n = len(listdir("grafos"))
	i = 0
	for file_name in listdir("grafos"):
		arq = open("grafos/"+file_name,"rb")
		estilos = set()
		for linha in arq.readlines():
			u,v = [x.strip() for x in linha.decode("UTF-8").split("\t@\t")]
			if not u in g.nodes():
				g.add_node(u,weight=0)
			if not v  in g.nodes():
				g.add_node(v,weight=0)
			estilos.add(u)
			estilos.add(v)
			if g.has_edge(u,v):
				g[u][v]["weight"] += 1
			else:
				g.add_edge(u,v,weight=1)
		arq.close()
		for x in estilos:
			g.node[x]["weight"] += 1
		if i % 400 == 0: print(i,n)
		i += 1

	nome_full = "dataset_"+nome_dataset+".txt"
	arq_full = open(nome_full,"wb")

	for u,v,w in g.edges(data=True):
		try:
			arq_full.write(bytearray(u +"\t@\t"+ str(g.node[u]["weight"]) +"\t@\t"+ v +"\t@\t"+ str(g.node[v]["weight"]) +"\t@\t"+ str(w["weight"])+"\n","UTF-8"))
		except UnicodeEncodeError:
			arq_full.write(u.encode("UTF-8") +"\t@\t".encode("UTF-8")+ str(g.node[u]["weight"]).encode("UTF-8") +"\t@\t".encode("UTF-8")+ v.encode("UTF-8") +"\t@\t".encode("UTF-8") + str(g[v]["weight"]).encode("UTF-8") +"\t@\t".encode("UTF-8")+ str(w["weight"])+"\n".encode("UTF-8"))
		except KeyError:
			print(v)
	arq_full.close()
	return g,nome_full


def main():
	#crawler_usuarios()

	#arq_seeds = open("users_crawler_lvl_2_pt3.txt","r")
	#usuarios = [x.strip() for x in arq_seeds.readlines()]
	#percorre_usuarios( usuarios )
	
	g,nome = carrega_grafo("seed7mil")
	print(g.number_of_nodes())
	#write_gml(g,nome.split(".")[0]+".gml")
	#for u,v in g.edges():
	#	print (u.encode("UTF-8"),v.encode("UTF-8"),g[u][v]["weight"])


if __name__ == "__main__":
	main()



# Top Artistas de um usuário
# http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user=Babs_05&api_key=3cfbe52ae6a18a925c18e50940817b58&format=json

# Pegar Amigos de um usuário
# http://ws.audioscrobbler.com/2.0/?method=user.getfriends&user=rj&api_key=3cfbe52ae6a18a925c18e50940817b58&format=json

# Pegar as TopTags de uma banda
# http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist=rammstein&api_key=3cfbe52ae6a18a925c18e50940817b58&format=json
