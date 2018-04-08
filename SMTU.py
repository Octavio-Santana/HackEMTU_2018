import requests

class SMTU(object):
    url = 'https://noxxonsat-nxnet.appspot.com'
    session = requests.Session()
    header = {'Accept':'application/json',
    'Authorization':'Basic aGFja2F0b25hMjAxOC0wMjp1bmljYW1wMjAxOC0wMg==','Content-Type':'application/json'}

    def _get(self, path):
        response = self.session.get(self.url+path, headers=self.header)
        return response.json()

    def bus(self, linha):
        """
        Retorna somente os veículos na linha, verificar o campo sentido para determinar se está rodando na ida ou na volta.
        """
        #return self._get('/rest/usuarios/v2?linha=%s' % linha)
        return self._get('/rest/usuarios/v2?linha={}'.format(linha))

    def near_bus(self, lat, lon, distance=None):
        """
        Retorna somente as linhas que estão próximas do ponto (latitude/longitude) fornecido. O parâmetro distancia pode conter os valores:
        """
        if distance:
            p='/rest/usuarios/v2?mode=ponto&distancia={}&latitude={}&longitude={}'.format(distance, lat, lon)
        else:
            p='/rest/usuarios/v2?mode=ponto&distancia=500&latitude={}&longitude={}'.format(lat, lon)
        return self._get(p)

    def positions(self, linha):
        position = self.bus(str(linha))
        return [[position['linhas'][0]['veiculos'][i]['latitude'],position['linhas'][0]['veiculos'][i]['longitude']]       for i in range(len(position['linhas'][0]['veiculos']))]


with open('live_pos.csv', 'w') as pos_file:
    pos_file.write('lat, lng\n')
    smtu = SMTU()
    pos_list = smtu.positions(503)
    for pos in pos_list:
        pos_file.write(str(pos[0]) + ',' + str(pos[1]) + '\n')


