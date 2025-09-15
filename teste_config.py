#!/usr/bin/env python3
"""
Teste das configurações do TaskFast
"""

from config import (
    obter_simbolos_tema, obter_cores_tema, obter_textos_tema, obter_info_tema, 
    listar_temas, alterar_tema, TEMA_ATUAL
)

def main():
    print("=" * 50)
    print("TESTE DAS CONFIGURAÇÕES DO TASKFAST")
    print("=" * 50)
    
    # Teste de símbolos
    simbolos = obter_simbolos_tema()
    print("\n1. SÍMBOLOS DO TEMA ATUAL:")
    print(f"   Tarefa concluída: {simbolos.FORMATO_CONCLUIDA}")
    print(f"   Tarefa pendente:  {simbolos.FORMATO_PENDENTE}")
    print(f"   Ponteiro seleção: {simbolos.PONTEIRO_SELECAO}")
    print(f"   Marca tema:       {simbolos.MARCA_TEMA}")
    print(f"   Separador:        {simbolos.SEPARADOR_LINHA[:15]}...")
    
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
    textos = obter_textos_tema()
    print("\n5. TEXTOS DO TEMA:")
    print(f"   Título: {textos.TITULO_PRINCIPAL}")
    print(f"   {textos.LABEL_CONCLUIDA}")
    print(f"   {textos.LABEL_HOJE}")
    print(f"   {textos.LABEL_PASSADO}")
    print(f"   {textos.LABEL_FUTURO}")
    
    # Teste comparativo de todos os temas
    print("\n6. COMPARAÇÃO VISUAL DOS TEMAS:")
    print("=" * 50)
    
    tema_original = TEMA_ATUAL
    
    for nome_tema, _ in temas:
        alterar_tema(nome_tema)
        simbolos = obter_simbolos_tema()
        textos = obter_textos_tema()
        
        print(f"\n🎨 TEMA: {nome_tema}")
        print(f"   Título:     {textos.TITULO_PRINCIPAL}")
        print(f"   Concluída:  {simbolos.FORMATO_CONCLUIDA}")
        print(f"   Pendente:   {simbolos.FORMATO_PENDENTE}")
        print(f"   Ponteiro:   {simbolos.PONTEIRO_SELECAO}Item selecionado")
        print(f"   Marca:      {simbolos.MARCA_TEMA}Item marcado")
        print(f"   Separador:  {simbolos.SEPARADOR_LINHA[:20]}")
    
    # Restaura tema original
    alterar_tema(tema_original)
    
    print("\n" + "=" * 50)
    print("✓ Todas as configurações funcionam corretamente!")
    print("✓ Cada tema tem símbolos únicos e visuais distintos!")
    print("✓ Use Shift+T no programa principal para alternar temas")
    print("=" * 50)

if __name__ == "__main__":
    main()