#-*-encoding: utf-8 -*- 
from networkx import Graph


def le_grafo(path):
	arq = open(path,"rb")
	g = Graph()
	for linha in arq.readlines():
		u,pu,v,pv,pe = linha.decode("UTF-8").strip().split("\t@\t")
		g.add_node(u,weight=int(pu))
		g.add_node(v,weight=int(pv))
		g.add_edge(u,v,weight=int(pe))
	arq.close()
	return g

def le_grafo_inverso(path):
	arq = open(path,"rb")
	g = Graph()
	for linha in arq.readlines():
		u,pu,v,pv,pe = linha.decode("UTF-8").strip().split("\t@\t")
		g.add_node(u,weight=int(pu))
		g.add_node(v,weight=int(pv))
		g.add_edge(u,v,weight=1/int(pe))
	arq.close()
	return g

def escreve_arquivo(arq, msg):
	try:
		arq.write( bytearray( msg + "\n", "UTF-8") )
	except UnicodeEncodeError:
		arq.write( mgs.encode("UTF-8") + "\n".encode("UTF-8"))


if __name__ == "__main__":
	pass