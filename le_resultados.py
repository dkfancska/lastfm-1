#!/usr/bin/env python3
#-*- encoding: utf-8

from operator import itemgetter


def le_resultados(nome_arq_metrica):
	arq = open("metricas/"+nome_arq_metrica+".txt","rb")
	
	resultados = []
	soma = 0
	for linha in arq.readlines():
		nome,valor = linha.decode("UTF-8").strip().split("\t")
		resultados.append((nome,float(valor)))
		soma += float(valor)

	n = len(resultados)
	media = soma / n
	soma = 0
	for nome,valor in resultados:
		soma += (valor - media)**2
	desvio = (soma/(n-1))**0.5

	return media,desvio,sorted(resultados, key = itemgetter(1))

def printa_resultados(metrica,media,desvio,resultados):
	print(metrica+"\nMédia: ",media, "Desvio:",desvio)

	print("Menores:")
	for nome,valor in resultados[:5]:
		print(nome+"\t"+str(valor))
	print("\nMaiores:")
	for nome,valor in resultados[-5:]:
		print(nome+"\t"+str(valor))
	print("\n\n")

def main():
	metrica = "between_centrality"
	media,desvio,resultados = le_resultados(metrica)
	printa_resultados(metrica,media,desvio,resultados)
	metrica = "closeness"
	media,desvio,resultados = le_resultados(metrica)
	printa_resultados(metrica,media,desvio,resultados)
	metrica = "degree_centrality"
	media,desvio,resultados = le_resultados(metrica)
	printa_resultados(metrica,media,desvio,resultados)
	#metrica = "excentricidade"
	#media,desvio,resultados = le_resultados(metrica)
	#printa_resultados(metrica,media,desvio,resultados)
	metrica = "rich"
	media,desvio,resultados = le_resultados(metrica)
	printa_resultados(metrica,media,desvio,resultados)
	metrica = "pagerank"
	media,desvio,resultados = le_resultados(metrica)
	printa_resultados(metrica,media,desvio,resultados)
	metrica = "clusterizacao"
	media,desvio,resultados = le_resultados(metrica)
	printa_resultados(metrica,media,desvio,resultados)
	metrica = "clusterizacao_peso"
	media,desvio,resultados = le_resultados(metrica)
	printa_resultados(metrica,media,desvio,resultados)


if __name__ == "__main__":
	main()