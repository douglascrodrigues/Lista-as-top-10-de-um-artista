import os
from redis import Redis


class Cache:
    def __init__(self):
        try:
            self.cliente_conectado = Redis( 
                host='localhost',
                port='6379'
            )

            self.limite_de_dias_armazenamento = 60 * 60 * 24 * 7
        except Exception as e:
            print(e)

    def mostra_item(self, nome):
        try:
            if self.cliente_conectado.exists(nome):
                return self.cliente_conectado.get(nome)
        except Exception as e:
            print(e)

        return None

    def salva_item(self, nome, item_data):
        try:
            if self.cliente_conectado.exists(nome):
                self.cliente_conectado.delete(nome)

            self.cliente_conectado.set(nome, str(item_data))

            self.cliente_conectado.expire(nome, self.limite_de_dias_armazenamento)
        except Exception as e:
            print(e)
