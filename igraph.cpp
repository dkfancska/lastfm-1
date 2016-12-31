#include <stdio.h>
#include <stdlib.h>
#include <igraph.h>
#include <unordered_map>
#include <iostream>
#include <ctime>

using namespace std;

int le_grafo(igraph_t & g, unordered_map<string, int> & verts,const char* path){
    int error;
    FILE* arq = fopen(path,"rb");
    char u[600];
    char v[600];
    string vert;
    int pu,pv,pe;

    error = igraph_empty_attrs(&g, 0, 0, 0); // Não entendi porque tem que adicionar um cara...
    if(error)   return 0;

    int i = 0;
    int k = 0;
    const clock_t start = clock();
    while(!feof(arq)){
        fscanf(arq,"%s\t@\t%d\t@\t%s\t@\t%d\t@\t%d",u,&pu,v,&pv,&pe);
        if(verts.find(u) == verts.end()){
            error = igraph_add_vertices(&g, 1, 0);
            vert.assign(u);
            verts.insert({vert,k});
            ++k;
        }
        if(verts.find(v) == verts.end()){
            error = igraph_add_vertices(&g, 1, 0);
            vert.assign(v);
            verts.insert({vert,k});
            ++k;
        }
        igraph_add_edge(&g,verts[u],verts[v]);
        if(i % 10000 == 0){
            cout << i << "\t\t" << (clock() - start)/(double) CLOCKS_PER_SEC << endl;
        }
        i+=1;
    }
    fclose(arq);
    return i;
}


int main(void){
    int num_edges;
    igraph_t g;
    unordered_map<string, int> verts;
    num_edges = le_grafo(g,verts,"dataset_30mil_short.txt");
    cout << verts.size() << " " << igraph_vcount(&g) << " " << igraph_ecount(&g) << endl;
    igraph_destroy(&g);
}
