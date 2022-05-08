from flask_restful import Resource, reqparse
from flask import jsonify
from api import GeniusApi

class TopDezMusicasArtista(Resource):
    #def get(self, cache=False)

    def get(self, nome_artista):

        artist = GeniusApi(nome_artista)

        try:
            nome_artista = nome_artista.strip()

            if len(nome_artista) < 2 or len(nome_artista) > 30:
                raise Exception('Verifique o nome pesquisado!')

            args = reqparse.RequestParser()
            args.add_argument('cache')

            dados=args.parse_args()
            tem_cache = dados['cache']

            cache = False if tem_cache is not None and tem_cache == 'False' else True

            status, artist_data = artist.top_musica_artista(cache)

            #print('MUSICAS: ',artist_data)

            if not status:
                raise Exception('Nao foi possivel encontrar musicas deste artista!')

            return jsonify(
                {
                    'pesquisado': nome_artista,
                    'nome_artista': artist_data['nome_artista'],
                    'lista_de_musica': artist_data['lista_de_musica']
                }
            )

        except:
            pass
