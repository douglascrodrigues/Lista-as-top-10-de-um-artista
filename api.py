import requests
import json
import uuid
import unidecode

from resources.Redis import Cache
from resources.DynamoDatabase import DynamoDatabase


class GeniusApi:
    def __init__(self, nome_artista):
        self.nome_artista = nome_artista
        self.id_artista = ''
        self.url = 'https://api.genius.com/'
        self._token="fmGvL2Rm3i2jDRFHVfYDafLgvMpxvU85lqN06sGDEk4TZzh3eunQfAsbAH2QgTHu"
        self.hed = {'Authorization': 'Bearer ' + self.token}
        
        self.lista_de_pesquisa = {}
        self.dic_som = {}
        self.lista_de_musica = []
        self.dic_artista = {}

        self.redis_cache = Cache()
        self.dynamo_db = DynamoDatabase()

    @property
    def token(self):
        return self._token

    
    def top_musica_artista(self, cache):
        
        if cache:
            cache_artista = self.redis_cache.mostra_item(self.nome_artista)

            if cache_artista is not None:
                cache_artista = cache_artista.decode('utf-8')
                cache_artista = str(cache_artista).replace("'", '"')
                cache_artista = json.loads(cache_artista)

                return True, cache_artista
        
        self.busca_artista()
        song_status, artist_data = self.busca_musica_artista()

        print('\n\nMUSICAS ACHADAS: ',self.lista_de_musica)

        if not song_status:
            return song_status, artist_data

        return song_status, artist_data
    

    def busca_artista(self):
        url = self.url + f'search?q={self.nome_artista}'
        response = requests.get(url, headers=self.hed)
        
        json_data = response.json()

        data = json_data['response']['hits']

        qtd_encontrado = len(data)-1

        if json_data['meta']['status'] != 200:
            return False, self.dic_artista

        for artista in range(qtd_encontrado):
            nome_artista = data[artista]
            if nome_artista['result']['primary_artist']['name'] == self.nome_artista:
                self.id_artista = nome_artista['result']['primary_artist']['id']

                if self.id_artista not in self.lista_de_pesquisa:
                    self.lista_de_pesquisa[self.id_artista] = {
                        'id_artista': self.id_artista,
                        'nome_artista': nome_artista['result']['primary_artist']['name'],
                        'n_ocorrencias': 1
                    }
                else:
                    self.lista_de_pesquisa[self.id_artista]['n_ocorrencias'] += 1

                num_ocorrencias = max(self.lista_de_pesquisa, key=lambda item: self.lista_de_pesquisa[item]['n_ocorrencias'])

                self.dic_artista['id_de_transacao'] = str(uuid.uuid4())
                self.dic_artista['artist_id'] = self.lista_de_pesquisa[num_ocorrencias]['id_artista']
                self.dic_artista['nome_artista'] = self.lista_de_pesquisa[num_ocorrencias]['nome_artista']
                self.dic_artista['pesquisado'] = self.nome_artista
        
        
    def busca_musica_artista(self):
        try:
            url = self.url + f'artists/{self.id_artista}/songs/'
            parametros = {'sort': 'popularity', 'per_page': str(10), 'page': str(1) }
            response = requests.get(url, parametros ,headers=self.hed)
            json_data = response.json()

            if json_data['meta']['status'] != 200:
                return False, self.dic_artista

            musicas = json_data['response']['songs']

            qtd_de_musicas = len(musicas)

            #if qtd_de_musicas > 0 and qtd_de_musicas < 10:
            for x in range(qtd_de_musicas):
                id_musica = musicas[x]['id']
                nome_musica = musicas[x]['full_title']

                if id_musica not in self.dic_som:
                    self.dic_som[id_musica] = {
                        'id_musica': id_musica,
                        'nome_musica':unidecode.unidecode(nome_musica)
                    }

                    self.lista_de_musica.append(unidecode.unidecode(nome_musica))

            self.dic_artista['lista_de_musica'] = self.lista_de_musica 


            self.redis_cache.salva_item(self.nome_artista, self.dic_artista)
            self.dynamo_db.set_item(self.nome_artista, self.dic_artista)
            
            
            return True, self.dic_artista
        except Exception as error:

            return False, self.dic_artista                