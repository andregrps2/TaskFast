import curses
import json
import os
import sys
from datetime import datetime, timedelta
import calendar
import locale
import platform
from config import (
    obter_simbolos_tema, obter_cores_tema, obter_textos_tema, inicializar_pares_cores, 
    ConfigGeral, TextosGerais, obter_info_tema, alterar_tema, listar_temas
)

# Obtém o diretório onde o executável está localizado
if getattr(sys, 'frozen', False):
    # Se está executando como executável (PyInstaller)
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Se está executando como script Python
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ARQUIVO = os.path.join(BASE_DIR, ConfigGeral.ARQUIVO_HISTORICO)
ARQUIVO_PENDENTES = os.path.join(BASE_DIR, ConfigGeral.ARQUIVO_PENDENTES)

def carregar_historico():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_historico(historico):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

def carregar_pendentes():
    """Carrega tarefas pendentes do arquivo separado"""
    if os.path.exists(ARQUIVO_PENDENTES):
        with open(ARQUIVO_PENDENTES, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_pendentes(pendentes):
    """Salva tarefas pendentes no arquivo separado"""
    with open(ARQUIVO_PENDENTES, "w", encoding="utf-8") as f:
        json.dump(pendentes, f, ensure_ascii=False, indent=2)

def calcular_tempo_relativo(data_origem_str, data_atual_str):
    """Calcula tempo relativo entre duas datas de forma amigável"""
    try:
        data_origem = datetime.strptime(data_origem_str, "%Y-%m-%d").date()
        data_atual = datetime.strptime(data_atual_str, "%Y-%m-%d").date()
        
        # Se for o mesmo dia, não mostra nada
        if data_origem == data_atual:
            return ""
        
        # Calcula diferença em dias
        diferenca = (data_atual - data_origem).days
        
        if diferenca == 0:
            return ""
        elif diferenca > 0:
            # TAREFAS DO PASSADO (pendentes atrasadas)
            if diferenca == 1:
                return "há 1 dia"
            elif diferenca < 7:
                return f"há {diferenca} dias"
            elif diferenca < 14:
                return "há 1 semana"
            elif diferenca < 30:
                semanas = diferenca // 7
                dias_restantes = diferenca % 7
                if dias_restantes == 0:
                    return f"há {semanas} semanas"
                elif semanas == 1:
                    return f"há 1 semana e {dias_restantes} dia{'s' if dias_restantes > 1 else ''}"
                else:
                    return f"há {semanas} semanas e {dias_restantes} dia{'s' if dias_restantes > 1 else ''}"
            elif diferenca < 365:
                meses = diferenca // 30
                dias_restantes = diferenca % 30
                if dias_restantes == 0:
                    return f"há {meses} mês{'es' if meses > 1 else ''}"
                elif meses == 1:
                    return f"há 1 mês e {dias_restantes} dia{'s' if dias_restantes > 1 else ''}"
                else:
                    return f"há {meses} meses e {dias_restantes} dia{'s' if dias_restantes > 1 else ''}"
            else:
                anos = diferenca // 365
                dias_restantes = diferenca % 365
                if dias_restantes == 0:
                    return f"há {anos} ano{'s' if anos > 1 else ''}"
                else:
                    return f"há {anos} ano{'s' if anos > 1 else ''} e {dias_restantes} dia{'s' if dias_restantes > 1 else ''}"
        else:
            # TAREFAS DO FUTURO (agendadas)
            diferenca = abs(diferenca)
            if diferenca == 1:
                return "em 1 dia"
            elif diferenca < 7:
                return f"em {diferenca} dias"
            elif diferenca < 14:
                return "em 1 semana"
            elif diferenca < 30:
                semanas = diferenca // 7
                dias_restantes = diferenca % 7
                if dias_restantes == 0:
                    return f"em {semanas} semanas"
                elif semanas == 1:
                    return f"em 1 semana e {dias_restantes} dia{'s' if dias_restantes > 1 else ''}"
                else:
                    return f"em {semanas} semanas e {dias_restantes} dia{'s' if dias_restantes > 1 else ''}"
            elif diferenca < 365:
                meses = diferenca // 30
                dias_restantes = diferenca % 30
                if dias_restantes == 0:
                    return f"em {meses} mês{'es' if meses > 1 else ''}"
                elif meses == 1:
                    return f"em 1 mês e {dias_restantes} dia{'s' if dias_restantes > 1 else ''}"
                else:
                    return f"em {meses} meses e {dias_restantes} dia{'s' if dias_restantes > 1 else ''}"
            else:
                anos = diferenca // 365
                dias_restantes = diferenca % 365
                if dias_restantes == 0:
                    return f"em {anos} ano{'s' if anos > 1 else ''}"
                else:
                    return f"em {anos} ano{'s' if anos > 1 else ''} e {dias_restantes} dia{'s' if dias_restantes > 1 else ''}"
    except:
        return f"desde {data_origem_str}"

def obter_cor_tarefa(tarefa, data_str):
    """Determina a cor da tarefa baseada no tempo relativo"""
    if tarefa["feito"]:
        return curses.color_pair(1)  # Tarefas concluídas
    
    if 'origem' not in tarefa:
        return curses.color_pair(7)  # Tarefas de hoje (sem origem)
    
    try:
        data_origem = datetime.strptime(tarefa['origem'], ConfigGeral.FORMATO_DATA).date()
        data_atual = datetime.strptime(data_str, ConfigGeral.FORMATO_DATA).date()
        
        if data_origem == data_atual:
            return curses.color_pair(7)  # Tarefas de hoje
        elif data_origem < data_atual:
            return curses.color_pair(8)  # Tarefas do passado
        else:
            return curses.color_pair(9)  # Tarefas do futuro
    except:
        return curses.color_pair(2)  # Cor padrão se houver erro

def get_data_string(data):
    """Converte datetime para string no formato configurado"""
    return data.strftime(ConfigGeral.FORMATO_DATA)

def carregar_tarefas_do_dia(historico, data_str):
    """Carrega tarefas do dia específico"""
    tarefas_do_dia = []
    
    # Carrega tarefas concluídas do dia específico
    if data_str in historico:
        tarefas_do_dia.extend(historico[data_str])
    
    # Carrega TODAS as tarefas pendentes (independente de data)
    pendentes = carregar_pendentes()
    for pendente in pendentes:
        # Verifica se a tarefa já não foi adicionada (evita duplicatas)
        if not any(t["texto"] == pendente["texto"] for t in tarefas_do_dia):
            tarefas_do_dia.append(pendente.copy())
    
    # Se não há tarefas, cria tarefas padrão apenas para hoje ou data futura
    if not tarefas_do_dia:
        hoje = datetime.now().date()
        data_atual = datetime.strptime(data_str, "%Y-%m-%d")
        data_carregada = data_atual.date()
        
        # Só cria tarefas padrão se for hoje ou data futura
        if data_carregada >= hoje:
            tarefas_do_dia = [
            ]
    
    return tarefas_do_dia

def salvar_tarefas_do_dia(historico, data_str, tarefas):
    """Salva tarefas concluídas no histórico e pendentes no arquivo separado"""
    # Separa tarefas concluídas e pendentes
    tarefas_concluidas = [t for t in tarefas if t["feito"]]
    tarefas_pendentes = [t for t in tarefas if not t["feito"]]
    
    # Salva tarefas concluídas no histórico
    if tarefas_concluidas:
        historico[data_str] = tarefas_concluidas
    elif data_str in historico:
        del historico[data_str]
    
    # Gerencia tarefas pendentes
    pendentes_atuais = carregar_pendentes()
    
    # Remove pendentes que foram concluídas
    pendentes_atuais = [p for p in pendentes_atuais 
                       if not any(t["texto"] == p["texto"] and t["feito"] for t in tarefas)]
    
    # Adiciona novas tarefas pendentes (que não existem ainda)
    for pendente in tarefas_pendentes:
        if not any(p["texto"] == pendente["texto"] for p in pendentes_atuais):
            # Se não tem origem, define como o dia atual
            if "origem" not in pendente:
                pendente["origem"] = data_str
            pendentes_atuais.append(pendente)
    
    # Salva pendentes atualizadas
    salvar_pendentes(pendentes_atuais)
    # Persistência imediata do histórico (antes só era feito ao sair / trocar dia)
    salvar_historico(historico)

def formatar_data_completa(data):
    """Formata data completa em português"""
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
             "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    
    dia_semana = dias_semana[data.weekday()]
    mes = meses[data.month - 1]
    
    return f"{dia_semana}, {data.day} de {mes} de {data.year}"

def gerar_calendario_mensal(data_central):
    """Gera um calendário mensal completo"""
    # Configuração do calendário
    cal = calendar.Calendar(firstweekday=0)  # Segunda-feira como primeiro dia
    ano = data_central.year
    mes = data_central.month
    
    # Nomes dos meses em português
    meses_pt = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    
    # Cabeçalho do mês/ano
    mes_ano = f"{meses_pt[mes-1]} {ano}"
    
    # Dias da semana abreviados
    dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    
    # Gera matriz do calendário
    semanas = cal.monthdayscalendar(ano, mes)
    
    return {
        "mes_ano": mes_ano,
        "dias_semana": dias_semana,
        "semanas": semanas,
        "dia_atual": data_central.day,
        "hoje": datetime.now().day if datetime.now().month == mes and datetime.now().year == ano else None
    }

def desenhar_calendario(stdscr, linha_inicial, calendario, col_width, offset_x=0):
    """Desenha o calendário mensal na coluna especificada"""
    linha_atual = linha_inicial
    
    # Cabeçalho do mês/ano
    mes_ano = calendario["mes_ano"]
    stdscr.addstr(linha_atual, offset_x + 2, mes_ano, curses.A_BOLD | curses.color_pair(5))
    linha_atual += 1
    
    # Linha decorativa
    decoracao = "═" * min(len(mes_ano) + 4, col_width - 2)
    stdscr.addstr(linha_atual, offset_x + 2, decoracao, curses.color_pair(4))
    linha_atual += 2
    
    # Cabeçalho dos dias da semana
    cal_width = 22  # 7 dias * 3 chars + espaços
    x_cal = offset_x + 2
    
    header_linha = ""
    for dia in calendario["dias_semana"]:
        header_linha += f"{dia} "
    
    stdscr.addstr(linha_atual, x_cal, header_linha, curses.A_BOLD | curses.color_pair(4))
    linha_atual += 1
    
    # Linha separadora
    sep_linha = "─" * len(header_linha)
    stdscr.addstr(linha_atual, x_cal, sep_linha, curses.A_DIM)
    linha_atual += 1
    
    # Desenha as semanas do calendário
    for semana in calendario["semanas"]:
        pos_x = x_cal
        for i, dia in enumerate(semana):
            if dia == 0:
                pos_x += 3
                continue
                
            if dia == calendario["hoje"]:
                # Hoje - destaque especial com fundo
                stdscr.addstr(linha_atual, pos_x, f"{dia:2d}", 
                             curses.A_BOLD | curses.A_REVERSE | curses.color_pair(6))
            elif dia == calendario["dia_atual"]:
                # Dia selecionado - moldura
                stdscr.addstr(linha_atual, pos_x, f"[{dia:1d}]" if dia < 10 else f"[{dia}]", 
                             curses.A_BOLD | curses.color_pair(5))
                pos_x += 3
                continue
            else:
                # Dia normal
                stdscr.addstr(linha_atual, pos_x, f"{dia:2d}", curses.A_NORMAL)
            
            pos_x += 3
            
        linha_atual += 1
    
    return linha_atual

def desenhar_legendas_compactas(stdscr, linha_inicial, col_width, offset_x=0):
    """Desenha legendas compactas na coluna especificada"""
    linha_atual = linha_inicial + 2
    
    # Linha separadora
    stdscr.addstr(linha_atual, offset_x, "─" * col_width, curses.A_DIM)
    linha_atual += 1
    
    # Calcula larguras das colunas (dividir em 2)
    col1_width = col_width // 2 - 2
    col2_start = offset_x + col1_width + 2
    
    # Legendas organizadas em duas colunas para economizar espaço
    legendas_col1 = [
        ("NAVEGAÇÃO", curses.A_BOLD | curses.color_pair(4)),
        ("j/k = ↑↓ tarefas", curses.A_DIM),
        ("h/l = ← → dias", curses.A_DIM),
        ("H/L = ← → meses", curses.A_DIM),
        ("t = hoje", curses.A_DIM),
        ("", curses.A_DIM),  # Espaço
        ("CORES", curses.A_BOLD | curses.color_pair(4)),
        (obter_textos_tema().LABEL_CONCLUIDA, curses.color_pair(1)),
        (obter_textos_tema().LABEL_HOJE, curses.color_pair(7)),
        (obter_textos_tema().LABEL_PASSADO, curses.color_pair(8)),
        (obter_textos_tema().LABEL_FUTURO, curses.color_pair(9)),
    ]
    
    legendas_col2 = [
        ("AÇÕES", curses.A_BOLD | curses.color_pair(4)),
        ("ENTER/SPC = marcar feito", curses.A_DIM),
        ("o = nova tarefa", curses.A_DIM),
        ("Shift+V = seleção múltipla", curses.A_DIM),
        ("j/k = navega+preseleciona", curses.A_DIM),
        ("dd = cortar/deletar", curses.A_DIM),
        ("p = colar embaixo", curses.A_DIM),
        ("P = colar em cima", curses.A_DIM),
        ("Shift+T = alterar tema", curses.A_DIM),
        ("ESC = sair", curses.A_DIM),
    ]
    
    # Desenha coluna 1
    for i, (texto, cor) in enumerate(legendas_col1):
        if linha_atual + i < stdscr.getmaxyx()[0] - 2:
            if texto:  # Não desenha linhas vazias
                stdscr.addstr(linha_atual + i, offset_x + 2, texto[:col1_width], cor)
    
    # Desenha coluna 2
    for i, (texto, cor) in enumerate(legendas_col2):
        if linha_atual + i < stdscr.getmaxyx()[0] - 2:
            if texto:  # Não desenha linhas vazias
                stdscr.addstr(linha_atual + i, col2_start, texto[:col1_width], cor)
    
    return linha_atual + max(len(legendas_col1), len(legendas_col2))

def mostrar_info_tema(stdscr):
    """Mostra informações do tema atual e permite alternar"""
    info_tema = obter_info_tema()
    temas = listar_temas()
    
    altura, largura = stdscr.getmaxyx()
    linha_atual = 2
    
    # Título
    stdscr.addstr(linha_atual, 2, "CONFIGURAÇÃO DE TEMA", curses.A_BOLD | curses.color_pair(4))
    linha_atual += 2
    
    # Tema atual
    stdscr.addstr(linha_atual, 2, f"Tema atual: {info_tema['nome']}", curses.color_pair(5))
    linha_atual += 1
    stdscr.addstr(linha_atual, 2, f"Descrição: {info_tema['descricao']}", curses.A_DIM)
    linha_atual += 1
    
    # Mostra símbolos do tema atual
    simbolos = info_tema['simbolos']
    textos = obter_textos_tema()
    stdscr.addstr(linha_atual, 2, f"Símbolos: {simbolos.FORMATO_CONCLUIDA} / {simbolos.FORMATO_PENDENTE}", curses.A_DIM)
    linha_atual += 1
    stdscr.addstr(linha_atual, 2, f"Título: {textos.TITULO_PRINCIPAL}", curses.A_DIM)
    linha_atual += 2
    
    # Lista de temas disponíveis
    stdscr.addstr(linha_atual, 2, "Temas disponíveis:", curses.A_BOLD | curses.color_pair(4))
    linha_atual += 1
    
    for i, (nome, descricao) in enumerate(temas):
        # Usar o ponteiro do tema atual para mostrar seleção
        simbolos_tema = obter_simbolos_tema()
        marcador = simbolos_tema.PONTEIRO_SELECAO if nome == info_tema['nome'] else "  "
        cor = curses.color_pair(5) if nome == info_tema['nome'] else curses.A_DIM
        texto = f"{marcador}{i+1}. {nome} - {descricao}"
        
        if linha_atual < altura - 4:
            stdscr.addstr(linha_atual, 2, texto[:largura-4], cor)
        linha_atual += 1
    
    linha_atual += 2
    stdscr.addstr(linha_atual, 2, "Pressione 1-4 para alterar tema, ESC para voltar", curses.A_DIM)
    
    stdscr.refresh()
    
    # Loop de seleção de tema
    while True:
        key = stdscr.getch()
        
        if key == 27:  # ESC
            break
        elif key >= ord('1') and key <= ord('4'):
            numero_tema = key - ord('1')
            if numero_tema < len(temas):
                nome_tema = temas[numero_tema][0]
                if alterar_tema(nome_tema):
                    # Reinicializa cores com novo tema
                    try:
                        inicializar_pares_cores()
                        stdscr.clear()
                        stdscr.addstr(altura//2, largura//2 - 15, 
                                    f"Tema alterado para: {nome_tema}", 
                                    curses.A_BOLD | curses.color_pair(1))
                        stdscr.refresh()
                        curses.napms(1000)  # Pausa de 1 segundo
                    except:
                        pass
                break

def main(stdscr):
    # Configurações iniciais para otimizar a interface
    try:
        # Tenta configurar a localização para UTF-8
        if platform.system() != "Windows":
            try:
                locale.setlocale(locale.LC_ALL, '')
            except:
                pass
        
        # Configurações de terminal mais seguras
        curses.curs_set(0)  # Esconde cursor inicialmente
        stdscr.nodelay(False)  # Entrada bloqueante
        stdscr.timeout(-1)  # Sem timeout
        stdscr.clear()  # Limpa a tela para começar fresh
        
        # Verifica se o terminal suporta cores
        if not curses.has_colors():
            raise Exception("Terminal não suporta cores")
            
        # Configuração de cores mais robusta
        curses.start_color()
        curses.use_default_colors()  # Usa cores padrão do terminal
        
        # Define pares de cores usando configuração do tema
        try:
            inicializar_pares_cores()
        except:
            # Se falhar ao configurar cores, usa padrões básicos
            for i in range(1, 10):
                try:
                    curses.init_pair(i, curses.COLOR_WHITE, -1)
                except:
                    pass
    
    except Exception as e:
        # Se falhar na inicialização, tenta uma configuração mais básica
        try:
            stdscr.clear()
            curses.curs_set(0)
        except:
            pass

    idx = 0
    historico = carregar_historico()
    data_atual = datetime.now()
    data_str = get_data_string(data_atual)
    tarefas = carregar_tarefas_do_dia(historico, data_str)
    
    last_key = None  # Para detectar 'dd'
    modo_edicao = False
    modo_navegacao_data = False
    nova_tarefa = ""
    tarefa_copiada = None  # Para armazenar tarefa cortada/copiada
    tarefas_copiadas = []  # Para armazenar múltiplas tarefas cortadas
    modo_selecao_multipla = False  # Modo de seleção múltipla
    tarefas_selecionadas = set()  # Índices das tarefas selecionadas
    ultima_direcao = None  # Para rastrear direção de navegação no modo múltiplo

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Define layout de duas colunas (INVERTIDO)
        col_esquerda_width = (width * 2) // 3  # 2/3 para tarefas (esquerda)
        col_direita_width = width - col_esquerda_width - 1  # 1/3 para calendário (direita)
        separador_x = col_esquerda_width
        
        # Controla a visibilidade do cursor baseado no modo
        if modo_edicao:
            curses.curs_set(1)  # Cursor visível no modo edição
        else:
            curses.curs_set(0)  # Cursor invisível no modo navegação
        
        # COLUNA ESQUERDA - TAREFAS
        if modo_edicao:
            # Cabeçalho no modo edição ocupando toda a largura
            stdscr.addstr(0, 0, "═" * width, curses.A_BOLD)
            titulo = " NOVA TAREFA "
            stdscr.addstr(0, (width - len(titulo)) // 2, titulo, curses.A_BOLD)
            stdscr.addstr(1, 2, "Digite a nova tarefa (textos longos são permitidos) e pressione ENTER para confirmar", curses.A_DIM)
            stdscr.addstr(2, 2, "Pressione ESC para cancelar | Use ◀▶ para navegar em textos longos", curses.A_DIM)
            linha_tarefas = 4
        else:
            # Cabeçalho da coluna esquerda - TAREFAS
            textos_tema = obter_textos_tema()
            simbolos_tema = obter_simbolos_tema()
            titulo_tarefas = textos_tema.TITULO_PRINCIPAL
            stdscr.addstr(0, 2, titulo_tarefas, curses.A_BOLD | curses.color_pair(4))
            # Usa separador do tema
            separador = simbolos_tema.SEPARADOR_LINHA[:min(len(titulo_tarefas), col_esquerda_width - 4)]
            stdscr.addstr(1, 2, separador, curses.A_DIM)
            linha_tarefas = 2

        # SEPARADOR VERTICAL
        for i in range(height):
            stdscr.addstr(i, separador_x, "│", curses.A_DIM)

        # COLUNA DIREITA - CALENDÁRIO E LEGENDAS
        col_direita_x = separador_x + 2
        if not modo_edicao:
            # Data completa no topo da coluna direita
            data_completa = formatar_data_completa(data_atual)
            # Adiciona indicador de modo se estiver em seleção múltipla
            if modo_selecao_multipla:
                data_completa += f" | SELEÇÃO MÚLTIPLA ({len(tarefas_selecionadas)})"
            # Trunca se muito longo para a coluna
            data_display = data_completa[:col_direita_width-2]
            cor_header = curses.color_pair(6) if modo_selecao_multipla else curses.color_pair(5)
            stdscr.addstr(0, col_direita_x, data_display, curses.A_BOLD | cor_header)
            
            # Calendário mensal
            calendario = gerar_calendario_mensal(data_atual)
            linha_pos_cal = desenhar_calendario(stdscr, 2, calendario, col_direita_width, col_direita_x)
            
            # Legendas compactas
            desenhar_legendas_compactas(stdscr, linha_pos_cal, col_direita_width, col_direita_x)

        # Lista de tarefas na coluna esquerda
        linha_atual_tarefa = linha_tarefas
        for i, t in enumerate(tarefas):
            if linha_atual_tarefa >= height - 4:  # Para se chegou no final da tela
                break
            
            simbolos = obter_simbolos_tema()
            prefixo = simbolos.FORMATO_CONCLUIDA if t["feito"] else simbolos.FORMATO_PENDENTE
            texto_tarefa = t['texto']
            
            # Mostra tempo relativo da tarefa (passado OU futuro)
            if 'origem' in t and not t["feito"]:
                tempo_relativo = calcular_tempo_relativo(t['origem'], data_str)
                if tempo_relativo:  # Só adiciona se não for vazio (mesmo dia)
                    texto_tarefa += f" ({tempo_relativo})"
            
            linha_completa = f"{prefixo} {texto_tarefa}"
            cor = obter_cor_tarefa(t, data_str)
            
            # Área disponível para o texto na coluna esquerda
            max_texto_width = col_esquerda_width - 6  # Margem + seta + espaços
            
            # Destaque da tarefa selecionada
            if i == idx and not modo_edicao:
                if modo_selecao_multipla:
                    # Modo seleção múltipla - indica múltiplas seleções possíveis
                    if i in tarefas_selecionadas:
                        stdscr.addstr(linha_atual_tarefa, 0, simbolos.MARCA_TEMA, curses.A_BOLD | curses.color_pair(6))  # Selecionada
                    else:
                        stdscr.addstr(linha_atual_tarefa, 0, simbolos.SETA_DIREITA, curses.A_BOLD | curses.color_pair(4))  # Cursor no modo múltiplo
                else:
                    # Modo normal - seta indicadora do tema
                    stdscr.addstr(linha_atual_tarefa, 0, simbolos.PONTEIRO_SELECAO, curses.A_BOLD | curses.color_pair(4))
            elif modo_selecao_multipla and i in tarefas_selecionadas:
                # Tarefa selecionada mas não é o cursor atual
                stdscr.addstr(linha_atual_tarefa, 0, simbolos.MARCA_TEMA, curses.A_BOLD | curses.color_pair(6))
            elif i == idx and modo_edicao:
                # Destacar onde a nova tarefa será inserida
                stdscr.addstr(linha_atual_tarefa, 0, simbolos.PONTEIRO_SELECAO, curses.A_BOLD | curses.color_pair(4))
            
            # Quebra o texto em múltiplas linhas se necessário
            if len(linha_completa) <= max_texto_width:
                # Desenha o texto com tratamento de erro
                try:
                    stdscr.addstr(linha_atual_tarefa, 2, linha_completa, cor)
                except curses.error:
                    # Se falhar ao desenhar, tenta sem cor
                    try:
                        stdscr.addstr(linha_atual_tarefa, 2, linha_completa)
                    except curses.error:
                        # Se ainda falhar, trunca o texto
                        texto_truncado = linha_completa[:max_texto_width-3] + "..."
                        stdscr.addstr(linha_atual_tarefa, 2, texto_truncado)
                linha_atual_tarefa += 1
            else:
                # Texto precisa ser quebrado em múltiplas linhas
                texto_restante = linha_completa
                primeira_linha = True
                
                while texto_restante and linha_atual_tarefa < height - 4:
                    if len(texto_restante) <= max_texto_width:
                        # Última parte do texto
                        if primeira_linha:
                            try:
                                stdscr.addstr(linha_atual_tarefa, 2, texto_restante, cor)
                            except curses.error:
                                try:
                                    stdscr.addstr(linha_atual_tarefa, 2, texto_restante)
                                except curses.error:
                                    pass
                        else:
                            # Continua com indentação
                            try:
                                stdscr.addstr(linha_atual_tarefa, 6, texto_restante, cor)
                            except curses.error:
                                try:
                                    stdscr.addstr(linha_atual_tarefa, 6, texto_restante)
                                except curses.error:
                                    pass
                        texto_restante = ""
                    else:
                        # Precisa quebrar a linha
                        # Tenta quebrar em um espaço para não cortar palavras
                        linha_atual_texto = texto_restante[:max_texto_width]
                        ultimo_espaco = linha_atual_texto.rfind(' ')
                        
                        if ultimo_espaco > max_texto_width // 2 and not primeira_linha:
                            # Quebra no espaço se não for muito no início
                            linha_para_mostrar = linha_atual_texto[:ultimo_espaco]
                            texto_restante = texto_restante[ultimo_espaco + 1:]  # +1 para pular o espaço
                        else:
                            # Quebra forçada
                            linha_para_mostrar = linha_atual_texto
                            texto_restante = texto_restante[max_texto_width:]
                        
                        if primeira_linha:
                            try:
                                stdscr.addstr(linha_atual_tarefa, 2, linha_para_mostrar, cor)
                            except curses.error:
                                try:
                                    stdscr.addstr(linha_atual_tarefa, 2, linha_para_mostrar)
                                except curses.error:
                                    pass
                            primeira_linha = False
                        else:
                            # Continua com indentação para mostrar que é continuação
                            try:
                                stdscr.addstr(linha_atual_tarefa, 6, linha_para_mostrar, cor)
                            except curses.error:
                                try:
                                    stdscr.addstr(linha_atual_tarefa, 6, linha_para_mostrar)
                                except curses.error:
                                    pass
                    
                    linha_atual_tarefa += 1
            
            # Adiciona linha pontilhada se está no modo edição
            if i == idx and modo_edicao and linha_atual_tarefa < height - 3:
                stdscr.addstr(linha_atual_tarefa, 2, "┄┄┄ Nova tarefa será inserida aqui ┄┄┄", 
                            curses.A_DIM | curses.color_pair(4))
                linha_atual_tarefa += 1
            
            # Pequeno espaçamento entre tarefas longas para melhor legibilidade
            if linha_atual_tarefa > linha_tarefas + i + 1:
                linha_atual_tarefa += 0  # Pode adicionar 1 aqui se quiser mais espaço

        if modo_edicao:
            # Caixa de entrada da nova tarefa na coluna esquerda
            nova_linha_y = linha_tarefas + len(tarefas) + 2
            if nova_linha_y < height - 4:  # Verifica se cabe na tela
                box_width = min(col_esquerda_width - 4, 60)  # Aumenta largura máxima da caixa
                box_start = 2
                
                stdscr.addstr(nova_linha_y, box_start, "┌" + "─" * (box_width - 2) + "┐", curses.A_BOLD)
                stdscr.addstr(nova_linha_y + 1, box_start, "│", curses.A_BOLD)
                stdscr.addstr(nova_linha_y + 1, box_start + box_width - 1, "│", curses.A_BOLD)
                stdscr.addstr(nova_linha_y + 2, box_start, "└" + "─" * (box_width - 2) + "┘", curses.A_BOLD)
                
                # Prefixo da nova tarefa
                stdscr.addstr(nova_linha_y + 1, box_start + 2, "[ ] ", curses.color_pair(2))
                
                # Área disponível para o texto (sem as bordas e prefixo)
                texto_area_width = box_width - 8  # 2 bordas + 2 espaços + 4 chars do "[ ] "
                
                # Implementa scroll horizontal para textos longos
                texto_len = len(nova_tarefa)
                cursor_pos = texto_len
                
                if texto_len <= texto_area_width:
                    # Texto cabe completamente na caixa
                    texto_display = nova_tarefa
                    cursor_x_relativo = cursor_pos
                else:
                    # Texto é maior que a caixa - implementa scroll
                    # Calcula o offset do scroll para manter o cursor visível
                    scroll_offset = max(0, cursor_pos - texto_area_width + 1)
                    texto_display = nova_tarefa[scroll_offset:scroll_offset + texto_area_width]
                    cursor_x_relativo = cursor_pos - scroll_offset
                    
                    # Se ainda estamos no início do scroll, não mostra indicador
                    if scroll_offset > 0:
                        # Mostra indicador de que há mais texto à esquerda
                        texto_display = "◀" + texto_display[1:]
                    
                    # Se há mais texto à direita, mostra indicador
                    if scroll_offset + texto_area_width < texto_len:
                        texto_display = texto_display[:-1] + "▶"
                
                # Desenha o texto
                stdscr.addstr(nova_linha_y + 1, box_start + 6, texto_display, curses.A_BOLD)
                
                # Posiciona o cursor
                cursor_x = box_start + 6 + cursor_x_relativo
                
                # Garante que o cursor não saia da caixa
                if cursor_x >= box_start + box_width - 1:
                    cursor_x = box_start + box_width - 2
                
                stdscr.move(nova_linha_y + 1, cursor_x)
        
        # Linha de status na parte inferior (mostra tema atual)
        if not modo_edicao and height > 3:
            info_tema = obter_info_tema()
            status_texto = f"Tema: {info_tema['nome']} | Shift+T para alterar"
            status_y = height - 1
            # Trunca se necessário
            status_display = status_texto[:width-2] if len(status_texto) > width-2 else status_texto
            try:
                stdscr.addstr(status_y, 1, status_display, curses.A_DIM | curses.color_pair(4))
            except:
                pass  # Ignora se não conseguir desenhar na última linha

        tecla = stdscr.getch()

        if modo_edicao:
            if tecla == 27:  # ESC cancela edição
                modo_edicao = False
                nova_tarefa = ""
            elif tecla in (curses.KEY_ENTER, 10, 13):  # Enter confirma edição
                if nova_tarefa.strip():
                    tarefas.insert(idx + 1, {"texto": nova_tarefa.strip(), "feito": False})
                    idx += 1
                    # Persistir imediatamente após adicionar
                    salvar_tarefas_do_dia(historico, data_str, tarefas)
                modo_edicao = False
                nova_tarefa = ""
            elif tecla in (curses.KEY_BACKSPACE, 127, 8):
                nova_tarefa = nova_tarefa[:-1]
            else:
                try:
                    nova_tarefa += chr(tecla)
                except:
                    pass
        else:
            # ESC no modo navegação = sair do modo múltiplo ou sair e salvar
            if tecla == 27:
                if modo_selecao_multipla:
                    # Se está no modo múltiplo, apenas sai do modo
                    modo_selecao_multipla = False
                    tarefas_selecionadas.clear()
                else:
                    # Se não está no modo múltiplo, sai do programa
                    salvar_tarefas_do_dia(historico, data_str, tarefas)
                    salvar_historico(historico)
                    curses.curs_set(0)  # Garante que o cursor esteja invisível ao sair
                    break

            char = chr(tecla) if 0 <= tecla <= 255 else ""

            if char == "j":
                if modo_selecao_multipla and tarefas:
                    # No modo múltiplo, j move para baixo
                    if ultima_direcao == "k":
                        # Indo na direção oposta: remove da seleção antes de mover
                        if idx in tarefas_selecionadas:
                            tarefas_selecionadas.remove(idx)
                            # Move sem adicionar à seleção (só remove)
                            idx = (idx + 1) % len(tarefas)
                            # Verifica se removeu todas as pré-seleções
                            if not tarefas_selecionadas:
                                modo_selecao_multipla = False
                                ultima_direcao = None
                        else:
                            # Não há mais o que remover, agora começa a adicionar
                            idx = (idx + 1) % len(tarefas)
                            tarefas_selecionadas.add(idx)
                            ultima_direcao = "j"
                    else:
                        # Mesma direção ou primeira vez: move e adiciona
                        idx = (idx + 1) % len(tarefas)
                        tarefas_selecionadas.add(idx)
                        ultima_direcao = "j"
                else:
                    # Modo normal
                    idx = (idx + 1) % len(tarefas) if tarefas else 0
            elif char == "k":
                if modo_selecao_multipla and tarefas:
                    # No modo múltiplo, k move para cima
                    if ultima_direcao == "j":
                        # Indo na direção oposta: remove da seleção antes de mover
                        if idx in tarefas_selecionadas:
                            tarefas_selecionadas.remove(idx)
                            # Move sem adicionar à seleção (só remove)
                            idx = (idx - 1) % len(tarefas)
                            # Verifica se removeu todas as pré-seleções
                            if not tarefas_selecionadas:
                                modo_selecao_multipla = False
                                ultima_direcao = None
                        else:
                            # Não há mais o que remover, agora começa a adicionar
                            idx = (idx - 1) % len(tarefas)
                            tarefas_selecionadas.add(idx)
                            ultima_direcao = "k"
                    else:
                        # Mesma direção ou primeira vez: move e adiciona
                        idx = (idx - 1) % len(tarefas)
                        tarefas_selecionadas.add(idx)
                        ultima_direcao = "k"
                else:
                    # Modo normal
                    idx = (idx - 1) % len(tarefas) if tarefas else 0
            elif char == "V" and tecla == 86:  # Shift+V para modo seleção múltipla
                modo_selecao_multipla = not modo_selecao_multipla
                if not modo_selecao_multipla:
                    tarefas_selecionadas.clear()
                    ultima_direcao = None
                else:
                    # Inicia com a tarefa atual selecionada
                    if tarefas:
                        tarefas_selecionadas.add(idx)
                        ultima_direcao = None  # Reset direção
            elif char == "h":  # Dia anterior
                # Salva dia atual antes de mudar
                salvar_tarefas_do_dia(historico, data_str, tarefas)
                data_atual = data_atual - timedelta(days=1)
                data_str = get_data_string(data_atual)
                tarefas = carregar_tarefas_do_dia(historico, data_str)
                idx = 0
                # Limpa seleções antigas (índices não são mais válidos)
                tarefas_selecionadas.clear()
                ultima_direcao = None
            elif char == "l":  # Próximo dia
                # Salva dia atual antes de mudar
                salvar_tarefas_do_dia(historico, data_str, tarefas)
                data_atual = data_atual + timedelta(days=1)
                data_str = get_data_string(data_atual)
                tarefas = carregar_tarefas_do_dia(historico, data_str)
                idx = 0
                # Limpa seleções antigas (índices não são mais válidos)
                tarefas_selecionadas.clear()
                ultima_direcao = None
            elif char == "H":  # Mês anterior
                # Salva dia atual antes de mudar
                salvar_tarefas_do_dia(historico, data_str, tarefas)
                if data_atual.month == 1:
                    data_atual = data_atual.replace(year=data_atual.year - 1, month=12)
                else:
                    data_atual = data_atual.replace(month=data_atual.month - 1)
                data_str = get_data_string(data_atual)
                tarefas = carregar_tarefas_do_dia(historico, data_str)
                idx = 0
                # Limpa seleções antigas (índices não são mais válidos)
                tarefas_selecionadas.clear()
                ultima_direcao = None
            elif char == "L":  # Próximo mês
                # Salva dia atual antes de mudar
                salvar_tarefas_do_dia(historico, data_str, tarefas)
                if data_atual.month == 12:
                    data_atual = data_atual.replace(year=data_atual.year + 1, month=1)
                else:
                    data_atual = data_atual.replace(month=data_atual.month + 1)
                data_str = get_data_string(data_atual)
                tarefas = carregar_tarefas_do_dia(historico, data_str)
                idx = 0
                # Limpa seleções antigas (índices não são mais válidos)
                tarefas_selecionadas.clear()
                ultima_direcao = None
            elif char == "t":  # Volta para hoje
                # Salva dia atual antes de mudar
                salvar_tarefas_do_dia(historico, data_str, tarefas)
                data_atual = datetime.now()
                data_str = get_data_string(data_atual)
                tarefas = carregar_tarefas_do_dia(historico, data_str)
                idx = 0
                # Limpa seleções antigas (índices não são mais válidos)
                tarefas_selecionadas.clear()
                ultima_direcao = None
            elif char == "T":  # Alternar tema (Shift+T)
                mostrar_info_tema(stdscr)
                stdscr.clear()  # Limpa tela após voltar
            elif tecla in (curses.KEY_ENTER, 10, 13):  # Enter marca/desmarca ou marca seleções múltiplas
                if tarefas:
                    if modo_selecao_multipla:
                        # No modo múltiplo, Enter faz toggle das tarefas pré-selecionadas
                        if tarefas_selecionadas:
                            # Verifica o estado das tarefas selecionadas
                            tarefas_feitas = [i for i in tarefas_selecionadas if i < len(tarefas) and tarefas[i]["feito"]]
                            tarefas_pendentes = [i for i in tarefas_selecionadas if i < len(tarefas) and not tarefas[i]["feito"]]
                            
                            if len(tarefas_feitas) == len(tarefas_selecionadas):
                                # Todas estão feitas -> marca como pendente
                                for i in tarefas_selecionadas:
                                    if i < len(tarefas):
                                        tarefas[i]["feito"] = False
                            else:
                                # Algumas ou nenhuma estão feitas -> marca todas como feitas
                                for i in tarefas_selecionadas:
                                    if i < len(tarefas):
                                        tarefas[i]["feito"] = True
                        
                        # Limpa seleções e sai do modo múltiplo
                        tarefas_selecionadas.clear()
                        modo_selecao_multipla = False
                    else:
                        # Modo normal, marca/desmarca tarefa
                        tarefas[idx]["feito"] = not tarefas[idx]["feito"]
                    # Persistir após toggle (multi ou single)
                    salvar_tarefas_do_dia(historico, data_str, tarefas)
            elif tecla == 32:  # Espaço marca/desmarca ou marca seleções múltiplas
                if tarefas:
                    if modo_selecao_multipla:
                        # No modo múltiplo, Espaço faz toggle das tarefas pré-selecionadas
                        if tarefas_selecionadas:
                            # Verifica o estado das tarefas selecionadas
                            tarefas_feitas = [i for i in tarefas_selecionadas if i < len(tarefas) and tarefas[i]["feito"]]
                            tarefas_pendentes = [i for i in tarefas_selecionadas if i < len(tarefas) and not tarefas[i]["feito"]]
                            
                            if len(tarefas_feitas) == len(tarefas_selecionadas):
                                # Todas estão feitas -> marca como pendente
                                for i in tarefas_selecionadas:
                                    if i < len(tarefas):
                                        tarefas[i]["feito"] = False
                            else:
                                # Algumas ou nenhuma estão feitas -> marca todas como feitas
                                for i in tarefas_selecionadas:
                                    if i < len(tarefas):
                                        tarefas[i]["feito"] = True
                        
                        # Limpa seleções e sai do modo múltiplo
                        tarefas_selecionadas.clear()
                        modo_selecao_multipla = False
                    else:
                        # Modo normal, marca/desmarca tarefa
                        tarefas[idx]["feito"] = not tarefas[idx]["feito"]
                    # Persistir após toggle (multi ou single)
                    salvar_tarefas_do_dia(historico, data_str, tarefas)
            elif char == "o":
                modo_edicao = True
                nova_tarefa = ""
            elif char == "d":
                if last_key == "d" and tarefas:
                    if modo_selecao_multipla and tarefas_selecionadas:
                        # Modo múltiplo - corta todas as tarefas selecionadas
                        tarefas_copiadas = []
                        indices_para_remover = sorted(tarefas_selecionadas, reverse=True)
                        
                        # Copia as tarefas selecionadas antes de deletar
                        for i in indices_para_remover:
                            if i < len(tarefas):
                                tarefas_copiadas.append(tarefas[i].copy())
                        
                        # Remove as tarefas do arquivo de pendentes se necessário
                        pendentes_atuais = carregar_pendentes()
                        for i in indices_para_remover:
                            if i < len(tarefas) and not tarefas[i]["feito"]:
                                pendentes_atuais = [p for p in pendentes_atuais 
                                                  if p["texto"] != tarefas[i]["texto"]]
                        salvar_pendentes(pendentes_atuais)
                        
                        # Remove as tarefas da lista atual (em ordem reversa para não afetar índices)
                        for i in indices_para_remover:
                            if i < len(tarefas):
                                tarefas.pop(i)
                        
                        # Limpa seleção múltipla e ajusta índice
                        tarefas_selecionadas.clear()
                        modo_selecao_multipla = False  # Sai do modo múltiplo automaticamente
                        idx = max(0, min(idx, len(tarefas) - 1)) if tarefas else 0
                        tarefa_copiada = None  # Limpa cópia single para usar múltipla
                        
                    else:
                        # Modo normal - corta uma tarefa
                        tarefa_copiada = tarefas[idx].copy()
                        tarefas_copiadas = []  # Limpa cópia múltipla
                        tarefa_deletada = tarefas[idx]
                        
                        # Remove da lista atual
                        tarefas.pop(idx)
                        
                        # Se for uma tarefa pendente, remove também do arquivo de pendentes
                        if not tarefa_deletada["feito"]:
                            pendentes_atuais = carregar_pendentes()
                            pendentes_atuais = [p for p in pendentes_atuais 
                                              if p["texto"] != tarefa_deletada["texto"]]
                            salvar_pendentes(pendentes_atuais)
                        
                        idx = max(0, idx - 1)
                    # Persistir após deletar/cortar
                    salvar_tarefas_do_dia(historico, data_str, tarefas)
                    
                    last_key = None
                    continue
                last_key = "d"
            elif char == "p":  # Colar embaixo da tarefa selecionada
                if tarefas_copiadas:  # Múltiplas tarefas copiadas
                    # Cola todas as tarefas múltiplas
                    for i, tarefa_para_colar in enumerate(tarefas_copiadas):
                        nova_tarefa = tarefa_para_colar.copy()
                        nova_tarefa["origem"] = data_str  # Atualiza origem para o dia atual
                        if tarefas:
                            tarefas.insert(idx + 1 + i, nova_tarefa)
                        else:
                            tarefas.append(nova_tarefa)
                    
                    if tarefas:
                        idx = min(idx + len(tarefas_copiadas), len(tarefas) - 1)
                    else:
                        idx = 0
                        
                elif tarefa_copiada and tarefas:  # Uma tarefa copiada
                    nova_tarefa = tarefa_copiada.copy()
                    nova_tarefa["origem"] = data_str  # Atualiza origem para o dia atual
                    tarefas.insert(idx + 1, nova_tarefa)
                    idx += 1  # Move seleção para a tarefa colada
                elif tarefa_copiada and not tarefas:
                    # Se não há tarefas, adiciona como primeira
                    nova_tarefa = tarefa_copiada.copy()
                    nova_tarefa["origem"] = data_str  # Atualiza origem para o dia atual
                    tarefas.append(nova_tarefa)
                    idx = 0
                # Persistir após colar
                salvar_tarefas_do_dia(historico, data_str, tarefas)
                last_key = None
            elif char == "P":  # Colar em cima da tarefa selecionada (Shift+P)
                if tarefas_copiadas:  # Múltiplas tarefas copiadas
                    # Cola todas as tarefas múltiplas
                    for i, tarefa_para_colar in enumerate(tarefas_copiadas):
                        nova_tarefa = tarefa_para_colar.copy()
                        nova_tarefa["origem"] = data_str  # Atualiza origem para o dia atual
                        if tarefas:
                            tarefas.insert(idx + i, nova_tarefa)
                        else:
                            tarefas.append(nova_tarefa)
                    
                    # idx permanece apontando para a primeira tarefa colada
                    
                elif tarefa_copiada:  # Uma tarefa copiada
                    nova_tarefa = tarefa_copiada.copy()
                    nova_tarefa["origem"] = data_str  # Atualiza origem para o dia atual
                    if tarefas:
                        # Insere antes da tarefa atual (em cima)
                        tarefas.insert(idx, nova_tarefa)
                        # idx permanece o mesmo, mas agora aponta para a nova tarefa
                    else:
                        # Se não há tarefas, adiciona como primeira
                        tarefas.append(nova_tarefa)
                        idx = 0
                # Persistir após colar
                salvar_tarefas_do_dia(historico, data_str, tarefas)
                last_key = None
            else:
                last_key = None

# Função para detectar terminal compatível
def verificar_compatibilidade_terminal():
    """Verifica se o terminal é compatível com curses"""
    try:
        # Verifica variáveis de ambiente importantes
        term = os.environ.get('TERM', '')
        
        # Lista de terminais conhecidos como problemáticos
        terminais_problematicos = ['dumb', 'unknown']
        
        if term.lower() in terminais_problematicos:
            return False, f"Terminal '{term}' não é compatível"
        
        # Para macOS, aceita a maioria dos terminais
        if platform.system() == "Darwin":
            # Se tem TERM definido e não está na lista problemática, aceita
            if term and term not in terminais_problematicos:
                return True, "Terminal macOS compatível"
        
        # Verifica se estamos no VS Code (mas não bloqueia automaticamente)
        if 'VSCODE' in os.environ or 'TERM_PROGRAM' in os.environ:
            term_program = os.environ.get('TERM_PROGRAM', '')
            if 'vscode' in term_program.lower():
                # Apenas avisa, mas ainda tenta
                return True, "Terminal VS Code (tentativa)"
        
        # Testa inicialização básica do curses
        import curses
        test_screen = curses.initscr()
        curses.endwin()
        
        return True, "Terminal compatível"
    except Exception as e:
        return False, f"Erro na verificação: {str(e)}"

def executar_modo_fallback():
    """Modo texto simples quando curses não funciona"""
    print("=" * 60)
    print("TASKFAST - MODO TEXTO SIMPLES")
    print("=" * 60)
    print("O terminal atual não suporta a interface gráfica completa.")
    print("Executando em modo de compatibilidade...")
    print()
    
    historico = carregar_historico()
    data_atual = datetime.now()
    data_str = get_data_string(data_atual)
    tarefas = carregar_tarefas_do_dia(historico, data_str)
    
    while True:
        print(f"\n📅 Data atual: {formatar_data_completa(data_atual)}")
        print("─" * 50)
        
        if not tarefas:
            print("Nenhuma tarefa para hoje.")
        else:
            for i, tarefa in enumerate(tarefas):
                simbolos = obter_simbolos_tema()
                status = simbolos.FORMATO_CONCLUIDA if tarefa["feito"] else simbolos.FORMATO_PENDENTE
                tempo_relativo = ""
                if 'origem' in tarefa and not tarefa["feito"]:
                    tempo_relativo = calcular_tempo_relativo(tarefa['origem'], data_str)
                    if tempo_relativo:
                        tempo_relativo = f" ({tempo_relativo})"
                
                print(f"{i+1:2d}. {status} {tarefa['texto']}{tempo_relativo}")
        
        print("\n" + "─" * 50)
        print("Comandos: [n]ova tarefa, [m]arcar feito (num), [d]ia anterior, [p]róximo dia, [s]air")
        
        try:
            comando = input("Digite o comando: ").strip().lower()
        except KeyboardInterrupt:
            print("\nSaindo...")
            break
        
        if comando == 's':
            break
        elif comando == 'n':
            nova_tarefa = input("Digite a nova tarefa: ").strip()
            if nova_tarefa:
                tarefas.append({"texto": nova_tarefa, "feito": False})
                print(f"Tarefa '{nova_tarefa}' adicionada!")
        elif comando == 'd':
            salvar_tarefas_do_dia(historico, data_str, tarefas)
            data_atual = data_atual - timedelta(days=1)
            data_str = get_data_string(data_atual)
            tarefas = carregar_tarefas_do_dia(historico, data_str)
        elif comando == 'p':
            salvar_tarefas_do_dia(historico, data_str, tarefas)
            data_atual = data_atual + timedelta(days=1)
            data_str = get_data_string(data_atual)
            tarefas = carregar_tarefas_do_dia(historico, data_str)
        elif comando.isdigit():
            num = int(comando) - 1
            if 0 <= num < len(tarefas):
                tarefas[num]["feito"] = not tarefas[num]["feito"]
                status = "concluída" if tarefas[num]["feito"] else "pendente"
                print(f"Tarefa {num+1} marcada como {status}")
        
        # Salva as alterações
        salvar_tarefas_do_dia(historico, data_str, tarefas)
        salvar_historico(historico)

# Executa o programa com tratamento de erro para terminais
# Executa o programa com tratamento de erro para terminais
if __name__ == "__main__":
    # No macOS, tenta executar diretamente primeiro
    if platform.system() == "Darwin":
        try:
            # Configura ambiente para macOS
            os.environ.setdefault('TERM', 'xterm-256color')
            if 'LC_ALL' not in os.environ:
                try:
                    os.environ['LC_ALL'] = 'pt_BR.UTF-8'
                except:
                    os.environ['LC_ALL'] = 'C.UTF-8'
            
            print("🚀 Iniciando TaskFast para macOS...")
            curses.wrapper(main)
            sys.exit(0)
            
        except KeyboardInterrupt:
            print("\n👋 Programa encerrado pelo usuário.")
            sys.exit(0)
        except Exception as e:
            print(f"⚠️ Interface gráfica não funcionou: {e}")
            print("Tentando modo alternativo...")
    
    # Para outros sistemas ou se macOS falhou, verifica compatibilidade
    compativel, mensagem = verificar_compatibilidade_terminal()
    
    if not compativel:
        print(f"⚠️  Aviso: {mensagem}")
        resposta = input("Deseja executar em modo texto simples? (s/N): ").strip().lower()
        if resposta in ['s', 'sim', 'y', 'yes']:
            executar_modo_fallback()
        else:
            print("Dicas para resolver:")
            print("- macOS: Use Terminal.app ou iTerm2")
            print("- Windows: Use Windows Terminal, PowerShell ou cmd")
            print("- Configure: export TERM=xterm-256color")
        sys.exit(0)
    
    # Se o terminal é compatível, tenta executar normalmente
    try:
        print(f"✅ {mensagem}")
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\n👋 Programa interrompido pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print("\n🔧 Soluções possíveis:")
        print("1. Execute em um terminal dedicado:")
        if platform.system() == "Darwin":  # macOS
            print("   - Terminal.app (Aplicações > Utilitários > Terminal)")
            print("   - iTerm2 (recomendado): https://iterm2.com")
        elif platform.system() == "Windows":
            print("   - Windows Terminal (recomendado)")
            print("   - PowerShell ou Prompt de Comando")
        else:  # Linux/Unix
            print("   - Terminal nativo do sistema")
        
        print("\n2. Instale dependências se necessário:")
        if platform.system() == "Windows":
            print("   pip install windows-curses")
        
        print("\n" + "─" * 50)
        resposta = input("Tentar modo texto simples? (s/N): ").strip().lower()
        if resposta in ['s', 'sim', 'y', 'yes']:
            try:
                executar_modo_fallback()
            except KeyboardInterrupt:
                print("\n👋 Programa encerrado.")
            except Exception as fallback_error:
                print(f"❌ Erro no modo fallback: {fallback_error}")
        else:
            print("\n📞 Para suporte: https://github.com/andregrps2/TaskFast")
