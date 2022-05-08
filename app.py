from flask import Flask
from flask_restful import Api
from resources.BuscaArtista import TopDezMusicasArtista

app = Flask(__name__)
api = Api(app)

api.add_resource(TopDezMusicasArtista, '/musicas/<string:nome_artista>')

if __name__=='__main__':
    app.run(debug=True)