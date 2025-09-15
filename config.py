"""
Arquivo de configuração do TaskFast
Contém constantes para personalização de cores, símbolos e temas.
"""

import curses

# ========================================
# CONFIGURAÇÃO DE TEMA
# ========================================

# Tema atual (pode ser alterado pelo usuário)
TEMA_ATUAL = "PADRÃO"

# Temas disponíveis
TEMAS_DISPONIVEIS = {
    "PADRÃO": "Tema padrão com cores clássicas",
    "ESCURO": "Tema escuro com cores mais suaves", 
    "CLARO": "Tema claro com cores mais brilhantes",
    "MINIMAL": "Tema minimalista com menos cores"
}

# ========================================
# SÍMBOLOS E MARCADORES POR TEMA
# ========================================

class SimbolosPadrao:
    """Símbolos do tema padrão - estilo clássico"""
    TAREFA_CONCLUIDA = "✓"
    TAREFA_PENDENTE = " "
    FORMATO_CONCLUIDA = f"[{TAREFA_CONCLUIDA}]"
    FORMATO_PENDENTE = f"[{TAREFA_PENDENTE}]"
    SETA_DIREITA = "→"
    SETA_ESQUERDA = "←"
    SETA_CIMA = "↑"
    SETA_BAIXO = "↓"
    DECORACAO_CALENDARIO = "═" * 20
    SEPARADOR_LINHA = "─" * 30
    SEPARADOR_SECAO = "=" * 40
    PONTEIRO_SELECAO = "► "
    MARCA_TEMA = "● "

class SimbolosEscuro:
    """Símbolos do tema escuro - estilo cyberpunk"""
    TAREFA_CONCLUIDA = "◉"
    TAREFA_PENDENTE = "○"
    FORMATO_CONCLUIDA = f"◆{TAREFA_CONCLUIDA}"
    FORMATO_PENDENTE = f"◇{TAREFA_PENDENTE}"
    SETA_DIREITA = "▶"
    SETA_ESQUERDA = "◀"
    SETA_CIMA = "▲"
    SETA_BAIXO = "▼"
    DECORACAO_CALENDARIO = "▓" * 20
    SEPARADOR_LINHA = "▬" * 30
    SEPARADOR_SECAO = "■" * 40
    PONTEIRO_SELECAO = "▸ "
    MARCA_TEMA = "▪ "

class SimbolosClaro:
    """Símbolos do tema claro - estilo moderno"""
    TAREFA_CONCLUIDA = "✔"
    TAREFA_PENDENTE = "○"
    FORMATO_CONCLUIDA = f"⟨{TAREFA_CONCLUIDA}⟩"
    FORMATO_PENDENTE = f"⟨{TAREFA_PENDENTE}⟩"
    SETA_DIREITA = "⇨"
    SETA_ESQUERDA = "⇦"
    SETA_CIMA = "⇧"
    SETA_BAIXO = "⇩"
    DECORACAO_CALENDARIO = "⚬" * 20
    SEPARADOR_LINHA = "⎯" * 30
    SEPARADOR_SECAO = "⚊" * 40
    PONTEIRO_SELECAO = "⇒ "
    MARCA_TEMA = "◦ "

class SimbolosMinimal:
    """Símbolos do tema minimal - estilo simples"""
    TAREFA_CONCLUIDA = "x"
    TAREFA_PENDENTE = " "
    FORMATO_CONCLUIDA = f"({TAREFA_CONCLUIDA})"
    FORMATO_PENDENTE = f"({TAREFA_PENDENTE})"
    SETA_DIREITA = ">"
    SETA_ESQUERDA = "<"
    SETA_CIMA = "^"
    SETA_BAIXO = "v"
    DECORACAO_CALENDARIO = "-" * 20
    SEPARADOR_LINHA = "_" * 30
    SEPARADOR_SECAO = "~" * 40
    PONTEIRO_SELECAO = "* "
    MARCA_TEMA = "- "

# ========================================
# DEFINIÇÕES DE CORES POR TEMA
# ========================================

class CoresPadrao:
    """Tema padrão - cores clássicas"""
    
    # Cores das tarefas
    TAREFA_CONCLUIDA = curses.COLOR_GREEN      # Verde para concluídas
    TAREFA_PENDENTE = curses.COLOR_WHITE       # Branco para pendentes
    TAREFA_HOJE = curses.COLOR_YELLOW          # Amarelo para tarefas de hoje  
    TAREFA_PASSADO = curses.COLOR_MAGENTA      # Magenta para tarefas do passado
    TAREFA_FUTURO = 8                          # Cinza escuro para futuro (cor 8)
    
    # Cores da interface
    TITULO_PRINCIPAL = curses.COLOR_CYAN       # Cyan para títulos
    DATA_ATUAL = curses.COLOR_YELLOW           # Amarelo para data atual
    DATA_HOJE = curses.COLOR_RED               # Vermelho para hoje no calendário
    HIGHLIGHT = curses.COLOR_BLACK             # Preto para texto destacado
    HIGHLIGHT_FUNDO = curses.COLOR_WHITE       # Fundo branco para highlight
    
    # Cores especiais
    COR_SELECAO_MULTIPLA = curses.COLOR_RED    # Vermelho para seleção múltipla
    COR_DESTAQUE = curses.COLOR_CYAN           # Cyan para destaques especiais

class CoresEscuro:
    """Tema escuro - cores mais suaves"""
    
    # Cores das tarefas  
    TAREFA_CONCLUIDA = curses.COLOR_GREEN
    TAREFA_PENDENTE = 8                        # Cinza claro
    TAREFA_HOJE = curses.COLOR_YELLOW
    TAREFA_PASSADO = curses.COLOR_BLUE
    TAREFA_FUTURO = 8
    
    # Cores da interface
    TITULO_PRINCIPAL = curses.COLOR_BLUE
    DATA_ATUAL = curses.COLOR_CYAN
    DATA_HOJE = curses.COLOR_MAGENTA
    HIGHLIGHT = curses.COLOR_WHITE
    HIGHLIGHT_FUNDO = curses.COLOR_BLACK
    
    # Cores especiais
    COR_SELECAO_MULTIPLA = curses.COLOR_MAGENTA
    COR_DESTAQUE = curses.COLOR_BLUE

class CoresClaro:
    """Tema claro - cores mais brilhantes"""
    
    # Cores das tarefas
    TAREFA_CONCLUIDA = curses.COLOR_GREEN
    TAREFA_PENDENTE = curses.COLOR_BLACK
    TAREFA_HOJE = curses.COLOR_YELLOW  
    TAREFA_PASSADO = curses.COLOR_RED
    TAREFA_FUTURO = 8
    
    # Cores da interface
    TITULO_PRINCIPAL = curses.COLOR_BLUE
    DATA_ATUAL = curses.COLOR_MAGENTA
    DATA_HOJE = curses.COLOR_RED
    HIGHLIGHT = curses.COLOR_WHITE
    HIGHLIGHT_FUNDO = curses.COLOR_BLUE
    
    # Cores especiais
    COR_SELECAO_MULTIPLA = curses.COLOR_RED
    COR_DESTAQUE = curses.COLOR_BLUE

class CoresMinimal:
    """Tema minimalista - menos cores"""
    
    # Cores das tarefas
    TAREFA_CONCLUIDA = curses.COLOR_WHITE
    TAREFA_PENDENTE = 8
    TAREFA_HOJE = curses.COLOR_WHITE
    TAREFA_PASSADO = 8
    TAREFA_FUTURO = 8
    
    # Cores da interface
    TITULO_PRINCIPAL = curses.COLOR_WHITE
    DATA_ATUAL = curses.COLOR_WHITE
    DATA_HOJE = curses.COLOR_WHITE
    HIGHLIGHT = curses.COLOR_BLACK
    HIGHLIGHT_FUNDO = curses.COLOR_WHITE
    
    # Cores especiais
    COR_SELECAO_MULTIPLA = curses.COLOR_WHITE
    COR_DESTAQUE = curses.COLOR_WHITE

# ========================================
# MAPEAMENTO DE TEMAS
# ========================================

MAPA_TEMAS = {
    "PADRÃO": CoresPadrao,
    "ESCURO": CoresEscuro,
    "CLARO": CoresClaro,
    "MINIMAL": CoresMinimal
}

MAPA_SIMBOLOS = {
    "PADRÃO": SimbolosPadrao,
    "ESCURO": SimbolosEscuro,
    "CLARO": SimbolosClaro,
    "MINIMAL": SimbolosMinimal
}

# ========================================
# FUNÇÃO PARA OBTER CORES DO TEMA ATUAL
# ========================================

def obter_cores_tema():
    """Retorna a classe de cores do tema atual"""
    return MAPA_TEMAS.get(TEMA_ATUAL, CoresPadrao)

def obter_simbolos_tema():
    """Retorna a classe de símbolos do tema atual"""
    return MAPA_SIMBOLOS.get(TEMA_ATUAL, SimbolosPadrao)

def alterar_tema(nome_tema):
    """Altera o tema atual se for válido"""
    global TEMA_ATUAL
    if nome_tema in TEMAS_DISPONIVEIS:
        TEMA_ATUAL = nome_tema
        return True
    return False

def listar_temas():
    """Retorna lista de temas disponíveis"""
    return [(nome, descricao) for nome, descricao in TEMAS_DISPONIVEIS.items()]

def obter_info_tema():
    """Retorna informações do tema atual"""
    return {
        'nome': TEMA_ATUAL,
        'descricao': TEMAS_DISPONIVEIS.get(TEMA_ATUAL, "Tema desconhecido"),
        'cores': obter_cores_tema(),
        'simbolos': obter_simbolos_tema()
    }

# ========================================
# MAPEAMENTO DE PARES DE CORES
# ========================================

def inicializar_pares_cores():
    """Inicializa os pares de cores baseado no tema atual"""
    cores = obter_cores_tema()
    
    # Pares de cores padrão (mantém a numeração original)
    curses.init_pair(1, cores.TAREFA_CONCLUIDA, -1)        # Tarefas concluídas
    curses.init_pair(2, cores.TAREFA_PENDENTE, -1)         # Tarefas pendentes  
    curses.init_pair(3, cores.HIGHLIGHT, cores.HIGHLIGHT_FUNDO)  # Highlight
    curses.init_pair(4, cores.COR_DESTAQUE, -1)            # Destaque especial
    curses.init_pair(5, cores.DATA_ATUAL, -1)              # Data atual
    curses.init_pair(6, cores.DATA_HOJE, -1)               # Hoje no calendário
    curses.init_pair(7, cores.TAREFA_HOJE, -1)             # Tarefas de hoje
    curses.init_pair(8, cores.TAREFA_PASSADO, -1)          # Tarefas do passado
    curses.init_pair(9, cores.TAREFA_FUTURO, -1)           # Tarefas do futuro
    
    # Par adicional para seleção múltipla
    if curses.COLORS > 10:
        curses.init_pair(10, cores.COR_SELECAO_MULTIPLA, -1)

# ========================================
# CONFIGURAÇÕES GERAIS
# ========================================

class ConfigGeral:
    # Formato de data
    FORMATO_DATA = "%Y-%m-%d"
    FORMATO_DATA_EXIBICAO = "%d/%m/%Y"
    
    # Configurações de interface
    ALTURA_MINIMA_TERMINAL = 20
    LARGURA_MINIMA_TERMINAL = 60
    
    # Arquivos de dados
    ARQUIVO_HISTORICO = "checklist_historico.json"
    ARQUIVO_PENDENTES = "checklist_pendentes.json"
    ARQUIVO_CONFIG = "config_usuario.json"
    
    # Configurações de codificação
    ENCODING = "utf-8"
    
    # Configurações de backup
    FAZER_BACKUP = True
    MAX_BACKUPS = 5

# ========================================
# MENSAGENS E TEXTOS POR TEMA
# ========================================

class TextosPadrao:
    """Textos do tema padrão"""
    TITULO_PRINCIPAL = "📋 TASKFAST - GERENCIADOR DE TAREFAS"
    LABEL_CONCLUIDA = "[x] = concluído"
    LABEL_HOJE = "Amarelo = hoje"
    LABEL_PASSADO = "Laranja = passado"
    LABEL_FUTURO = "Cinza = futuro"

class TextosEscuro:
    """Textos do tema escuro - cyberpunk"""
    TITULO_PRINCIPAL = "▣ TASKFAST - CYBER ORGANIZER"
    LABEL_CONCLUIDA = "◉ = executado"
    LABEL_HOJE = "Hoje = destaque"
    LABEL_PASSADO = "Antigo = registro"
    LABEL_FUTURO = "Futuro = planejado"

class TextosClaro:
    """Textos do tema claro - moderno"""
    TITULO_PRINCIPAL = "⚡ TASKFAST - TASK MANAGER"
    LABEL_CONCLUIDA = "✔ = finalizado"
    LABEL_HOJE = "Atual = ativo"
    LABEL_PASSADO = "Anterior = histórico"
    LABEL_FUTURO = "Próximo = agendado"

class TextosMinimal:
    """Textos do tema minimal - simples"""
    TITULO_PRINCIPAL = "TASKFAST"
    LABEL_CONCLUIDA = "(x) = feito"
    LABEL_HOJE = "hoje"
    LABEL_PASSADO = "passado"
    LABEL_FUTURO = "futuro"

# Mapeamento de textos por tema
MAPA_TEXTOS = {
    "PADRÃO": TextosPadrao,
    "ESCURO": TextosEscuro,
    "CLARO": TextosClaro,
    "MINIMAL": TextosMinimal
}

def obter_textos_tema():
    """Retorna a classe de textos do tema atual"""
    return MAPA_TEXTOS.get(TEMA_ATUAL, TextosPadrao)

# Classe de textos gerais (não muda com tema)
class TextosGerais:
    # Mensagens de status
    MSG_SEM_TAREFAS = "Nenhuma tarefa para este dia"
    MSG_TAREFA_ADICIONADA = "Tarefa adicionada com sucesso!"
    MSG_TAREFA_REMOVIDA = "Tarefa removida!"
    MSG_TEMA_ALTERADO = "Tema alterado para: {}"
    
    # Instruções
    INSTRUCOES_NAVEGACAO = [
        "← → = navegar dias",
        "↑ ↓ = navegar tarefas", 
        "ENTER = marcar/desmarcar",
        "a = adicionar tarefa",
        "d = remover tarefa",
        "m = seleção múltipla",
        "h = ajuda",
        "Shift+T = alterar tema",
        "q = sair"
    ]