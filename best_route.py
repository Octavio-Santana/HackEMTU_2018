import googlemaps
import numpy as np
import pandas as pd

a = pd.read_csv("Rotas.csv") #Arquivo para se ler, com as rotas, de preferencia com 1 coluna: Origens, sendo a ultima linha o destino final. Já clusterizado

gmaps = googlemaps.Client(key = "AIzaSyCevRj56piNzlLOjc0A0MpF2Lj9ENEKzvk")

a = np.array(a['0'])

r = gmaps.distance_matrix(a,a, mode= 'driving')

r_pd = pd.DataFrame(r)

#print(r_pd)

aux = []

for i in range(0,len(a)):
    for j in range(0,len(a)):
        if(i!=j):
            origem = a[i]
            destin = a[j]
            distancia = r['rows'][i]['elements'][j]['distance']['value']
            duracao = r['rows'][i]['elements'][j]['duration']['value']

            infos = [origem, destin, distancia, duracao]
            aux.append(infos)

pandas_index = ['Origem','Destino','Distância', 'Duração']
aux = pd.DataFrame(aux, columns = pandas_index)

def greedypath_un(v):
    verif = True
    begin = v.loc[0,'Origem']
    greedy = [begin]
    while(verif):

        if(len(greedy)>= len(a)):
            return greedy
            verif = False

        range = v.loc[v['Origem']==begin,'Distância']
        index = range.loc[range==range.min()].index
        new_begin = v.loc[index[0],'Destino']
        if(new_begin not in [x for x in greedy]):
            greedy.append(new_begin)
            begin = new_begin
        else:
            v = v.drop(v.index[index]).reset_index(drop = True)
            #v.reset_index(drop = True)

def greedypath(v):
    streets = greedypath_un(v)
    return streets

results = greedypath(aux)

lat = []
lng = []

for i in range(len(results)):
    geocode_result = gmaps.geocode(results[i])
    lat.append(geocode_result[0]["geometry"]["location"]["lat"])
    lng.append(geocode_result[0]["geometry"]["location"]["lng"])

results = pd.DataFrame({"lat": lat, "lng": lng})
results.to_csv("rota_final.csv", index= False)
