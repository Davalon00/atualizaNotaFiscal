from pony.orm import *


def entidades_para_db(db):

    #1 Status = "Aguardando processamento"
    #2 Status = "Processamento concluido"
    #-1 Status = "Arquivo com erro ou erro durante processamento"
    class Nota(db.Entity):
        id_nota = PrimaryKey(int, auto=True)
        nome_nota = Required(str)
        status_nota = Required(int)
        data_recebimento = Required(str)
        data_processamento = Optional(str)
        data_disponibilidade = Optional(str)
        """def __init__(self, nome, status, dt_rec, dt_proc = "", dt_disp = ""):
            self.nome_nota = nome
            self.status_nota = status
            self.data_recebimento = dt_rec
            self.data_processamento = dt_proc
            self.data_disponibilidade = dt_disp"""
    return Nota
