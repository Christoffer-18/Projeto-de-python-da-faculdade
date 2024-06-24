#adicinar um limite de tempo
from pacotes import conectando_ao_banco as db
import PySimpleGUI as sg 
from pacotes import front as ft

con = db.conecta_db(1)
cursor = db.meu_cursor(con)

t = True
while t:
# Todas as coisas dentro da sua janela
    layout =[
        [sg.Text("O que deseja fazer?")],
        [sg.Button("Criar vaquinha"), sg.Button("Ver vaquinha"), sg.Button("Criar gasto"),sg.Button("Ver gasto")],
        [sg.Text('',size=(4,0))],
        [sg.Button("Cancelar")]
    ]
    #Crie a janela 
    janela = sg.Window("Tela inicial",layout)
#evento loop para processae "eventos" e obter "valores" das entradas 
    event, values = janela.read()
    #if event != None:
    t = ft.fechar(event)

    if event == "Criar vaquinha":
        janela.close()
        t = ft.criar_vq()

    if event == "Ver vaquinha":
        janela.close()
        t = ft.ver_vq()

    if event == "Criar gasto":
        janela.close()
        t = ft.criar_gt()
    
    if event == "Ver gasto":
        janela.close()
        t = ft.ver_gasto()
        
janela.close()
cursor.close()
db.desconecta_db(con)