from datetime import datetime
import time
import os
import shutil
import pytest

from pony.orm import *
import xml.etree.ElementTree as et

try:
    from notaFiscal import *
except:
    raise ModuleNotFoundError("Não foi possível immportar módulo 'notaFiscal.py'")


#busca arquivos no diretório de entrada
def buscaArquivo():
    try:
        if os.listdir('./in') != 0:
            return os.listdir('./in')
        else:      
            time.sleep(1)
    except:
        raise NotADirectoryError("Erro ao acessar a pasta de entrada") 


if __name__ == '__main__':

    set_sql_debug(True)

    db = Database()
    #db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
    db.bind(provider='sqlite', filename=':memory:', create_db=True)
    
    db_entidades = entidades_para_db(db)

    db.generate_mapping(create_tables=True)

    while True:
        for nota in buscaArquivo():
            try:
                with db_session:
                    if db_entidades.get(nome_nota = nota):
                        raise FileExistsError("Arquivo: " + nota + " já existe no banco")
                    else:
                        #Cria entrada no db para arquivo
                        n = db_entidades(nome_nota = nota, status_nota = 1,data_recebimento = str(datetime.now()))
            
            except FileExistsError as err:
                print(err)
            
            except:
                raise ConnectionAbortedError("Conexão com o banco abortada")

            
            #abre arquivo xml e realiza operações
            try:
                nota_proc = et.parse('./in/' + nota)
            except:
                raise FileNotFoundError("Não foi possível encontrar o arquivo")
            
            raiz = nota_proc.getroot()
            
            for det in raiz.iter('{http://www.portalfiscal.inf.br/nfe}det'):
                qtdCompra = det.find('{http://www.portalfiscal.inf.br/nfe}prod').find('{http://www.portalfiscal.inf.br/nfe}qCom').text
                valUnCompra = det.find('{http://www.portalfiscal.inf.br/nfe}prod').find('{http://www.portalfiscal.inf.br/nfe}vUnCom').text
                valProduto = det.find('{http://www.portalfiscal.inf.br/nfe}prod').find('{http://www.portalfiscal.inf.br/nfe}vProd').text
                qtdTributada = det.find('{http://www.portalfiscal.inf.br/nfe}prod').find('{http://www.portalfiscal.inf.br/nfe}qTrib').text
                valUnTributada = det.find('{http://www.portalfiscal.inf.br/nfe}prod').find('{http://www.portalfiscal.inf.br/nfe}vUnTrib').text
                print(qtdCompra, valUnCompra, valProduto, qtdTributada, valUnTributada)
            
            #atualiza status e data de processamento do arquivo no banco
            try:
                with db_session:
                    n = db_entidades.get(nome_nota = nota)
                    n.status_nota = 2
                    n.data_processamento = str(datetime.now())
            except:
                raise ConnectionAbortedError("Conexão com o banco abortada")
            
            #envia arquivo para diretório de saída
            try:
                shutil.copy2("./in/" + nota , "./out/" + nota)
                os.remove("./in/" + nota)
            except:
                raise FileNotFoundError("Arquivo: " + nota + " não pôde ser copiado")

#TODO testar falha banco, disco, conexao, arquivo
#TODO checar banco antes de inserir/atualizar linha

#################################################################################################
#raiz -> [0]NFe -> [0]infNFe -> [3...]det -> [0]prod -> [6]qCom                                 #
#                                                    -> [7]vUnCom                               #
#                                                    -> [8]vProd                                #
#                                                    -> [11]qTrib                               #
#                                                    -> [12]vUnTrib                             #
#                                         -> [1]imposto -> [0]vTotTrib                          #
#                                                       -> [1]ICMS -> [0]ICMS... -> [2]pCred    #
#                                                                                -> [3]vCred    #    
#                                                       -> [2]IPI                               #
#                                                                                               #
#                                                       -> [3]PIS                               #
#                                                                                               #
#                                                       -> [4]COFINS                            #
#                                                                                               #
#                            ->[...]total -> [1]vICMS                                           #
#                                         -> [10]vIPI                                           #
#                                         -> [11]vPIS                                           #   
#                                         -> [12]vCOFINS                                        #
#                                         -> [15]vTotTrib                                       #   
#################################################################################################