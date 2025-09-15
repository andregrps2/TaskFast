#!/usr/bin/env python3
"""
Demonstração Visual dos Temas do TaskFast
Mostra como cada tema aparece na prática com tarefas de exemplo.
"""

from config import (
    obter_simbolos_tema, obter_textos_tema, alterar_tema, 
    listar_temas, TEMA_ATUAL
)

def demonstrar_tema(nome_tema):
    """Demonstra visualmente como fica um tema específico"""
    alterar_tema(nome_tema)
    simbolos = obter_simbolos_tema()
    textos = obter_textos_tema()
    
    print(f"\n{'='*60}")
    print(f"🎨 {nome_tema.upper()}")
    print(f"{'='*60}")
    
    # Título do tema
    print(f"\n{textos.TITULO_PRINCIPAL}")
    print(simbolos.SEPARADOR_LINHA[:40])
    
    # Lista de tarefas de exemplo
    print(f"\nLISTA DE TAREFAS:")
    print(f"{simbolos.PONTEIRO_SELECAO}Tarefa atual selecionada")
    print(f"  {simbolos.FORMATO_CONCLUIDA} Tarefa já concluída")
    print(f"  {simbolos.FORMATO_PENDENTE} Tarefa pendente")
    print(f"  {simbolos.FORMATO_PENDENTE} Revisar código do projeto")
    print(f"{simbolos.MARCA_TEMA}{simbolos.FORMATO_PENDENTE} Tarefa marcada para ação")
    print(f"  {simbolos.FORMATO_CONCLUIDA} Enviar relatório")
    print(f"  {simbolos.FORMATO_PENDENTE} Agendar reunião")
    
    # Indicadores de navegação
    print(f"\nNAVEGAÇÃO:")
    print(f"  {simbolos.SETA_ESQUERDA} Dia anterior    {simbolos.SETA_DIREITA} Próximo dia")
    print(f"  {simbolos.SETA_CIMA} Tarefa acima     {simbolos.SETA_BAIXO} Tarefa abaixo")
    
    # Labels de status
    print(f"\nLEGENDA:")
    print(f"  {textos.LABEL_CONCLUIDA}")
    print(f"  {textos.LABEL_HOJE}")
    print(f"  {textos.LABEL_PASSADO}")
    print(f"  {textos.LABEL_FUTURO}")

def main():
    print("🎭 DEMONSTRAÇÃO VISUAL DOS TEMAS DO TASKFAST")
    print("=" * 60)
    print("Veja como cada tema aparece na prática:")
    
    tema_original = TEMA_ATUAL
    temas = listar_temas()
    
    # Demonstra cada tema
    for nome_tema, descricao in temas:
        demonstrar_tema(nome_tema)
        print(f"\nDescrição: {descricao}")
    
    # Restaura tema original
    alterar_tema(tema_original)
    
    print(f"\n{'='*60}")
    print("🎯 RESUMO DAS DIFERENÇAS ENTRE TEMAS:")
    print("=" * 60)
    
    print("\n📋 PADRÃO:")
    print("  • Símbolos clássicos [✓] [ ]")
    print("  • Ponteiros tradicionais ► ●")
    print("  • Estilo familiar e intuitivo")
    
    print("\n🌙 ESCURO (Cyberpunk):")
    print("  • Símbolos geométricos ◆◉ ◇○")
    print("  • Ponteiros angulares ▸ ▪")
    print("  • Visual futurista e moderno")
    
    print("\n☀️ CLARO (Moderno):")
    print("  • Símbolos elegantes ⟨✔⟩ ⟨○⟩")  
    print("  • Ponteiros direcionais ⇒ ◦")
    print("  • Design limpo e sofisticado")
    
    print("\n🎯 MINIMAL (Simples):")
    print("  • Símbolos básicos (x) ( )")
    print("  • Ponteiros minimalistas * -")
    print("  • Máxima simplicidade e clareza")
    
    print(f"\n{'='*60}")
    print("✨ Cada tema oferece uma experiência visual única!")
    print("🔄 Use Shift+T no programa principal para alternar")
    print("=" * 60)

if __name__ == "__main__":
    main()