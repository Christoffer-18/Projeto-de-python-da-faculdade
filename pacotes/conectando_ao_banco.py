import psycopg2
import PySimpleGUI as sg
import time
from pacotes import front as ft

#configurando conexão
def conecta_db(status = 0):
    """
        Por boa prática quando for chamar o banco de dados use con = conecta_db()
        isso vai ajudar quando chamar a função desconecta_db
    """
    connection = psycopg2.connect(
        user ="postgres",
        password = "*****",
        host="localhost",
        port="5432",
        database="vaquinha_online"
    )
    if status == 1:
        if connection.status == 1:
            print("Você está conectado ao banco de dados!")
        else:
            print("Falha ao conectar ao banco de dados")
    return connection

#Criando Cursor
def meu_cursor(x):
    meu_cursor = x.cursor()
    return meu_cursor

#desconecta db
def desconecta_db(x):
    x.close()
    print("Finalizando conexão")
    return x

#Inserir vaquinha no db
def inserir_vq(nome,valor = 0):
    #Abrindo conexão
    con = conecta_db()
    cursor = meu_cursor(con)
    try:
        insert = '''insert into vaquinha(nome, valor_total) values (%s,%s);'''
        dados = (nome,valor)
        cursor.execute(insert,dados)
    except(Exception) as error:
        print(F"Erro ao inserir dados na tabela {error}")
    else:
        con.commit()
        print("Registro inserido com sucesso!")
    finally:
        #fechando conexão
        cursor.close()
        con.close()

#Inserir gasto no db
def inserir_gt(id_,valor,descricao):
    con = conecta_db()
    cursor = meu_cursor(con)
    try:
        insert = '''insert into gastos(id_vaquinha,valor,descricao) values (%s,%s,%s);'''
        dados = (id_,valor,descricao)
        cursor.execute(insert,dados)
    except:
        print("Erro ao inserir dados na tabela!")
    else:
        con.commit()
        print("Registro inserido com sucesso!")
        #select('gastos',1,id_)
    finally:
        cursor.close()
        con.close()

#Verificando str
def verificador_str(plv, msg ='',titulo=''):
    '''
        Sempre usar dentro de um loop
    '''
    if plv[0].isalpha():
        for crt in plv:
            if not(crt.isalpha() or crt.isspace()):
                ft.mensagem(f"{msg}", f"{titulo}")
                return True
        return False
    else:
        ft.mensagem(f"{msg}", f"{titulo}")
        return True

#validando número
def verificando_float(valor, msg = '', titulo=''):
    '''
        Além de validar o valor, também deixamos ele apenas com 2 casas décimais, e não usamos truncamento, apenas arredondamento.
        Volta (false ou true) no [0] e no [1] volta o valor formatdo
    '''
    try:
        n = float(valor)
    except(ValueError):
        ft.mensagem(f"{msg}", f"{titulo}")
        return (True, 0)
    else:
        num_formatado = round(n/1,2)
        return (False ,num_formatado)

#excluir
def excluir(nome, id_):
    """
        Para usar essa função, estamos acreditando que quer pagar apenas uma linha
        Sempre vamos usar o id da linha como base de pârametro 
        e o nome = nome da tabela
    """
    con = conecta_db()
    cursor = meu_cursor(con)
    try:
        cursor.execute(f"delete from {nome} where id = {id_}")
    except(Exception) as erro:
        print(F"O erro foi esse {erro.__class__}")
    else:
        con.commit()
        print("Registro apagado!")
    finally:
        cursor.close()
        con.close()