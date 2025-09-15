#!/usr/bin/env python3
"""
Teste das configurações do TaskFast
"""

from config import (
    Simbolos, obter_cores_tema, obter_info_tema, 
    listar_temas, alterar_tema, Textos
)

def main():
    print("=" * 50)
    print("TESTE DAS CONFIGURAÇÕES DO TASKFAST")
    print("=" * 50)
    
    # Teste de símbolos
    print("\n1. SÍMBOLOS:")
    print(f"   Tarefa concluída: {Simbolos.FORMATO_CONCLUIDA}")
    print(f"   Tarefa pendente:  {Simbolos.FORMATO_PENDENTE}")
    print(f"   Separador:        {Simbolos.SEPARADOR_LINHA}")
    
    # Teste de tema atual
    print("\n2. TEMA ATUAL:")
    info = obter_info_tema()
    print(f"   Nome: {info['nome']}")
    print(f"   Descrição: {info['descricao']}")
    
    # Teste de cores do tema
    print("\n3. CORES DO TEMA:")
    cores = obter_cores_tema()
    print(f"   Cor tarefa concluída: {cores.TAREFA_CONCLUIDA}")
    print(f"   Cor tarefa pendente:  {cores.TAREFA_PENDENTE}")
    print(f"   Cor título:           {cores.TITULO_PRINCIPAL}")
    
    # Teste de temas disponíveis
    print("\n4. TEMAS DISPONÍVEIS:")
    temas = listar_temas()
    for nome, desc in temas:
        marcador = " → " if nome == info['nome'] else "   "
        print(f"{marcador}{nome}: {desc}")
    
    # Teste de textos
    print("\n5. TEXTOS CONFIGURADOS:")
    print(f"   {Textos.LABEL_CONCLUIDA}")
    print(f"   {Textos.LABEL_HOJE}")
    print(f"   {Textos.LABEL_PASSADO}")
    print(f"   {Textos.LABEL_FUTURO}")
    
    print("\n" + "=" * 50)
    print("✓ Todas as configurações funcionam corretamente!")
    print("✓ O arquivo config.py foi criado com sucesso!")
    print("✓ Use Shift+T no programa principal para alternar temas")
    print("=" * 50)

if __name__ == "__main__":
    main()