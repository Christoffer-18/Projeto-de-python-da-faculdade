import PySimpleGUI as sg
from pacotes import conectando_ao_banco as db
import time


def criar_vq():
    v1 = True
    while v1:
        # janela "Criar vaquinha"
        layout_cvq = [
            [
                sg.Text("Insira o nome da vaquinha:", size=(19, 1)),
                sg.InputText(key="nome"),
            ],
            [
                sg.Text("Insira o valor da vaquinha:", size=(19, 1)),
                sg.InputText(key="valor"),
            ],
            [
                sg.Text(
                    "Não use vírgula!",
                )
            ],
            [sg.Text(" ", size=(6, 0))],
            [sg.Button("Criar"), sg.Button("Cancelar")],
        ]
        # criando janela
        janela_cvq = sg.Window("Criar vaquinha", layout_cvq)
        event_cvq, values_cvq = janela_cvq.read()
        teste = fechar(event_cvq)
        if teste == False:
            janela_cvq.close()
            return True
        # validando dados
        tx = db.verificador_str(
            values_cvq["nome"], "Na opção nome digite apenas letras!", "Atenção"
        )
        fl = db.verificando_float(
            values_cvq["valor"],
            "Na opção valor use apenas números e ponto para separar, caso necessário!",
            "Atenção",
        )
        x = fl[0]
        if tx == True or x == True:
            janela_cvq.close()
        else:
            values_cvq["valor"] = fl[1]
            v1 = False

    # ler evento
    v2 = True
    while v2:
        # para fechar o evento caso o usúario queira
        v2 = fechar(event_cvq)
        # validando dados
        if event_cvq == "Criar":
            db.inserir_vq(values_cvq["nome"], values_cvq["valor"])
            mensagem("A criação da vaquinha foi concluída com sucesso!")
    janela_cvq.close()
    return True

def ver_vq():
    con = db.conecta_db(0)
    cursor = db.meu_cursor(con)
    # Pesquisando na tabela
    v1 = True
    filtroSql = ""
    tabela = "vaquinha"
    while v1:
        layout_ps = [
            [
                sg.Text("Escolha entre o código ou nome da vaquinha :"),
                sg.Combo(["Cód", "Nome"], size=(8, 0), key="escolha"),
            ],
            [sg.Text("Digite o nome ou o código: "), sg.InputText(key="chave")],
            [sg.Text(" ", size=(6, 0))],
            [sg.Button("Pesquisar"), sg.Button("Cancelar")],
        ]
        # criando janela
        janela_ps = sg.Window("Consulta vaquinha", layout_ps)
        event_ps, values_ps = janela_ps.read()
        x = fechar(event_ps)
        if x == False:
            janela_ps.close()
            return True
        if values_ps["escolha"] == "Cód":
            fl = db.verificando_float(values_ps["chave"])
            if fl[0] == False:
                valor = int(values_ps["chave"])
                filtroSql = f" where id = {valor}"
                v1 = False
        if values_ps["escolha"] == "Nome":
            tx = db.verificador_str(values_ps["chave"])
            if tx == False:
                filtroSql = f" where nome = '{values_ps['chave']}'"
                v1 = False
        janela_ps.close()

    cursor.execute(f"select * from {tabela} {filtroSql};")
    linhas = cursor.fetchall()
    x = len(linhas)
    if x == 0:
        mensagem("Registro não encontrado", "Pesquisa")
    else:
            # Mostrando a tabela
        rows = []
        toprow = ["Cód", "Valor", "Nome"]
        for j in range(0, x):
            rows.append([linhas[j][0], linhas[j][1], linhas[j][2]])

        tabela = sg.Table(
            values=rows,  # Dados da tabela
            headings=toprow,  # Cabeçalhos da tabela
            auto_size_columns=True,  # Ajusta automaticamente o tamanho das colunas
            display_row_numbers=False,  # Não exibe números das linhas
            justification="center", key="-TABLE-",  # Centraliza o texto nas células , # Chave para identificar a tabela
            selected_row_colors="red on yellow",  # Cor de seleção das linhas
            enable_events=True,  # Habilita eventos
            expand_x=True,  # Permite expandir horizontalmente
            expand_y=True,  # Permite expandir verticalmente
            enable_click_events=True)  # Habilita eventos de clique

        layout = [[tabela]]
        janela = sg.Window("Mostrando Vaquinha", layout, size=(715, 200), resizable=True)
        while True:
            event, values = janela.read()
            if event == sg.WIN_CLOSED:
                return True
    cursor.close()
    db.desconecta_db(con)
    return True

def criar_gt():
    v1 = True
    while v1:
        # janela "Criar gasto"
        layout_cgt = [
            [sg.Text("Para inserir gastos, você precisa saber o código da vaquina, se não souber clique aqui:"),sg.Button("Ver vaquinha"),],
            [sg.Text("Digite o código da vaquinha: ", size=(21, 1)),sg.InputText(key="id"),],
            [sg.Text("Digite o valor do gasto: ", size=(21, 1)),sg.InputText(key="valor"),],
            [sg.Text("Digite o nome do gasto: ", size=(21, 1)),sg.InputText(key="nome"),],
            [sg.Text(" ", size=(6, 0))],
            [sg.Button("Criar"), sg.Button("Cancelar")],
        ]
        # Criando janela
        janela_cgt = sg.Window("Criar gasto", layout_cgt)
        event_cgt, values_cgt = janela_cgt.read()
        teste = fechar(event_cgt)

        if event_cgt == "Ver vaquinha":
            janela_cgt.close()
            ver_vq()
            criar_gt()
            return True

        if teste == False:
            janela_cgt.close()
            return True
        # Validando dados
        tx = db.verificador_str(
            values_cgt["nome"], "Na opção nome digite apenas letras!", "Atenção"
        )
        cod = db.verificando_float(
            values_cgt["id"], "Na opção código use apenas número inteiros!", "Atenção"
        )
        valor = db.verificando_float(values_cgt["valor"],"Na opção valor use apenas números e ponto para separar, caso necessário!","Atenção",)
        if tx == True or cod[0] == True or valor[0] == True:
            janela_cgt.close()
            criar_gt()
            return True
        else:
            id_ = int(cod[1])
            valor = valor[1]
            if event_cgt == "Criar":
                db.inserir_gt(id_, valor, values_cgt["nome"])
                mensagem("A criação do gasto foi concluido com sucesso")

        janela_cgt.close()
        return True

def ver_gasto():
    con = db.conecta_db(0)
    cursor = db.meu_cursor(con)
    # Pesquisando na tabela
    v1 = True
    filtroSql = ""
    tabela = "gastos"
    while v1:
        layout_vg = [
            [sg.Text("Para visualizar os gastos, você terá que usar o código da vaquinha, se não souber use o botão ao lado para consultar"),sg.Button("Consultar vaquinha"),],
            [sg.Text("Digite o código: "), sg.InputText(key="id_")],
            [sg.Text(" ", size=(6, 0))],
            [sg.Button("Pesquisar"), sg.Button("Cancelar")],
        ]
        # criando janela
        janela_vg = sg.Window("Consulta gastos", layout_vg)
        event_vq, values_vq = janela_vg.read()
        x = fechar(event_vq)

        if event_vq == "Consultar vaquinha":
            janela_vg.close()
            ver_vq()
            ver_gasto()
            return True

        if x == False:
            janela_vg.close()
            return True
        fl = db.verificando_float(values_vq["id_"], "Digite apenas números!", "Atenção!")
        if fl[0] == False:
            valor = int(values_vq["id_"])
            filtroSql = f" where id_vaquinha = {valor}"
            v1 = False
        janela_vg.close()

    cursor.execute(f"select * from {tabela} {filtroSql}")
    linhas = cursor.fetchall()
    cursor.execute(f"select * from vaquinha where id = {valor}")
    linha = cursor.fetchall()
    x = len(linhas)
    if x == 0:
        mensagem("Registro não encontrado", "Pesquisa")
    else:
        rows = []
        toprow = ["valor", "Descrição"]
        for j in range(0,x):
            rows.append([linhas[j][2],linhas[j][3]])

        tabela = sg.Table(
            values=rows,  # Dados da tabela
            headings=toprow,  # Cabeçalhos da tabela
            auto_size_columns=True,  # Ajusta automaticamente o tamanho das colunas
            display_row_numbers=False,  # Não exibe números das linhas
            justification="center", key="-TABLE-",  # Centraliza o texto nas células , # Chave para identificar a tabela
            selected_row_colors="red on yellow",  # Cor de seleção das linhas
            enable_events=True,  # Habilita eventos
            expand_x=True,  # Permite expandir horizontalmente
            expand_y=True,  # Permite expandir verticalmente
            enable_click_events=True)  # Habilita eventos de clique
    
    layout = [[sg.Text(f"Mostrando os gasto da vaquinha: {linha[0][2]}")],
        [tabela]]
    janela = sg.Window("Mostrando gastos", layout, size=(715,200), resizable=True)
    while True:
        event, values = janela.read()
        if event == sg.WIN_CLOSED:
            return True
    cursor.close()
    db.desconecta_db(con)
    return True

def fechar(f):
    if f == sg.WIN_CLOSED or f == "Cancelar":
        return False

def mensagem(msg, msg_de_cima=" "):
    layout_msg = [[sg.Text(msg)]]
    janela_msg = sg.Window(f"{msg_de_cima}", layout_msg)
    event, values = janela_msg.read(timeout=5000)  # Espera por eventos por 5 segundos
    janela_msg.close()