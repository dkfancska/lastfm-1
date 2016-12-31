#-*-encoding: utf-8 -*-

from graph_tool.all import *

def le_grafo(path):
	g = Graph(directed=False)
	nome_v = g.new_vertex_property("string")
	peso_v = g.new_vertex_property("int")
	peso_e = g.new_edge_property("int")
	arq = open(path,"rb")
	verts = {}
	i = 0
	CONST = -1
	for linha in arq.readlines():
		u,pu,v,pv,pe = linha.decode("UTF-8").strip().split("\t@\t")
		pu = int(pu)
		pv = int(pv)
		pe = int(pe)
		if not u in verts.keys() and pu >= CONST:
			verts[u] = g.add_vertex()
			nome_v[verts[u]] = u
			peso_v[verts[u]] = pu
		if not v in verts.keys() and pv >= CONST:
			verts[v] = g.add_vertex()
			nome_v[verts[v]] = v
			peso_v[verts[v]] = pv

		if pu >= CONST and pv >= CONST:
			peso_e[g.add_edge(verts[u],verts[v])] = 1./float(pe)
		if i % 1000000 == 0: print(i)
		i += 1
	arq.close()
	return g,nome_v,peso_v,peso_e

def diametro(g,peso_e):
	maior = -10**9
	mapa = shortest_distance(g,weights=peso_e)
	for v in g.vertices():
		for d in mapa[v]:
			if d > maior:
				maior = d
	return maior

def grau(g):
	menor = 10**9
	maior = -10**9
	for v in g.vertices():
		d = v.out_degree() 
		if d > maior:
			maior = d
		if d < menor:
			menor = d
	return menor,maior
			
def perfil(g,nome_v,peso_v,peso_e):
	print("Número de vértices: %d | Número de Arestas: %d" % (g.num_vertices(),g.num_edges()))
	print("Diâmetro: %d" % (diametro(g,peso_e)))
	print("Menor Grau: %d || Maior Grau: %d" % grau(g))
	

def histo_verts(g,nome_v,peso_v,path):
	arq = open(path,"wb")
	for v in g.vertices():
		arq.write(nome_v[v].encode("UTF-8")+"\t@\t"+str(peso_v[v]).encode("UTF-8")+"\n".encode("UTF-8"))
	arq.close()

def main():
	g,nome_v,peso_v,peso_e = le_grafo("dataset_seed10mil.txt")
	perfil(g,nome_v,peso_v,peso_e)
	#histo_verts(g,nome_v,peso_v,"histo_verts_seed100.txt")
	#graph_draw(g,vertex_text=nome_v,vertex_font_size=13, output_size=(8000,8000),output="dataset_seed100.png")
	#graph_draw(g,vertex_text=nome_v,vertex_font_size=13, output_size=(8000,8000),output="dataset_seed100.pdf")

if __name__ == "__main__":
	main()
	
