#!/usr/bin/python
#-*-encoding: utf-8 -*-
from igraph import *
from time import time

def le_grafo(path):
	g = Graph()
	arq = open(path,"rb")
	verts = {}
	i = 0
	k = 0
	ars = []
	peso_ars = []
	peso_verts = []
	nomes = []
	start = time()
	for linha in arq.readlines():
		u,pu,v,pv,pe = linha.decode("UTF-8").strip().split("\t@\t")
		if not u in verts:
			g.add_vertices(1)
			verts[u] = k
			peso_verts.append(int(pu))
			nomes.append(u)
			k += 1
		if not v in verts:
			g.add_vertices(1)
			verts[v] = k
			peso_verts.append(int(pv))
			nomes.append(v)
			k += 1
		ars.append((verts[u],verts[v]))
		peso_ars.append(int(pe))
		if i % 100000 == 0:
			print i,time()-start
		i += 1
	g.add_edges(ars)
	g.vs["nome"] = nomes
	g.vs["peso"] = peso_verts
	g.es["peso"] = peso_ars

	return g

def detecta_edge_betweenness(g,n):
	print "Separando Communidades:"
	start = time()
	grupos = g.community_edge_betweenness(weights="peso")
	print "Separou em", time() - start,"segundos"
	return grupos

def detecta_fast_greedy(g,n):
	print "Separando Communidades:"
	start = time()
	grupos = g.community_fastgreedy(weights="peso")
	print "Separou em", time() - start,"segundos"
	return grupos

def detecta_info_map(g,n):
	print "Separando Communidades:"
	start = time()
	grupos = g.community_infomap(edge_weights="peso",trials=30)
	print "Separou em", time() - start,"segundos"
	return grupos

def detecta_leading_eigenvector(g,n):
	print "Separando Communidades:"
	start = time()
	grupos = g.community_leading_eigenvector(weights="peso")
	print "Separou em", time() - start,"segundos"
	return grupos


def detecta_label_propagation(g,n):
	print "Separando Communidades:"
	start = time()
	grupos = g.community_label_propagation(weights="peso")
	print "Separou em", time() - start,"segundos"
	return grupos

def detecta_multilevel(g,n):
	print "Separando Communidades:"
	start = time()
	grupos = g.community_multilevel(weights="peso")
	print "Separou em", time() - start,"segundos"
	return grupos

def detecta_spinglass(g,n):
	print "Separando Communidades:"
	start = time()
	grupos = g.community_spinglass(weights="peso")
	print "Separou em", time() - start,"segundos"
	return grupos

def detecta_walktrap(g,n):
	print "Separando Communidades:"
	start = time()
	grupos = g.community_edge_betweenness(weights="peso")
	print "Separou em", time() - start,"segundos"
	return grupos

def ordena_comunidades(g,grupo):
	tuplas = []
	for v in grupo:
		tuplas.append((g.vs[v]["peso"],g.vs[v]["nome"]))
	return sorted(tuplas,reverse=True)

def escreve_comunidades(g,grupos,algoritmo):
	i = 0
	for grupo in grupos:
		print "Comunidade ",i, len(grupo)
		arq = open("comunidades/"+algoritmo+"_"+str(i)+".txt","wb")
		arq.write(str(g.modularity(grupos,weights="peso"))+"\n")
		for u,v in ordena_comunidades(g,grupo):
			try:
				arq.write(bytearray(v+"\t@\t"+str(u)+"\n","UTF-8"))
			except UnicodeEncodeError:
				arq.write(v.encode("UTF-8")+"\t@\t"+str(u)+"\n")
		arq.close()
		i += 1

def main():
	g = le_grafo("dataset_30mil_short.txt")
	n = 5
	print g.vcount(),g.ecount()
	grupos = detecta_leading_eigenvector(g,n)
	if type(grupos) is VertexDendrogram:
		escreve_comunidades(g,grupos.as_clustering(),"leading_eigenvector")
	else:
		escreve_comunidades(g,grupos,"leading_eigenvector")	
	grupos = detecta_fast_greedy(g,n)
	if type(grupos) is VertexDendrogram:
		escreve_comunidades(g,grupos.as_clustering(),"fast_greedy")
	else:
		escreve_comunidades(g,grupos,"fast_greedy")
	grupos = detecta_info_map(g,n)
	if type(grupos) is VertexDendrogram:
		escreve_comunidades(g,grupos.as_clustering(),"info_map")
	else:
		escreve_comunidades(g,grupos,"info_map")

	grupos = detecta_label_propagation(g,n)
	if type(grupos) is VertexDendrogram:
		escreve_comunidades(g,grupos.as_clustering(),"label_propagation")
	else:
		escreve_comunidades(g,grupos,"label_propagation")

	grupos = detecta_multilevel(g,n)
	if type(grupos) is VertexDendrogram:
		escreve_comunidades(g,grupos.as_clustering(),"multilevel")
	else:
		escreve_comunidades(g,grupos,"multilevel")
	
	grupos = detecta_walktrap(g,n)
	if type(grupos) is VertexDendrogram:
		escreve_comunidades(g,grupos.as_clustering(),"walktrap")
	else:
		escreve_comunidades(g,grupos,"walktrap")

	grupos = detecta_spinglass(g,n)
	if type(grupos) is VertexDendrogram:
		escreve_comunidades(g,grupos.as_clustering(),"spinglass")
	else:
		escreve_comunidades(g,grupos,"spinglass")	

if __name__ == "__main__":
	main()