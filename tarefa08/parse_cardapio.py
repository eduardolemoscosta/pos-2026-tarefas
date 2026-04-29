import xml.dom.minidom as minidom

def obter_texto(elemento, tag):
    """Função auxiliar para extrair o texto de uma tag XML de forma segura."""
    try:
        noh = elemento.getElementsByTagName(tag)[0]
        return noh.firstChild.nodeValue.strip() if noh.firstChild else ""
    except (IndexError, AttributeError):
        return ""

def main():
    arquivo_xml = 'cardapio.xml'
    
    try:
        dom = minidom.parse(arquivo_xml)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo_xml}' não foi encontrado.")
        return
    except Exception as e:
        print(f"Erro ao processar o XML: {e}")
        return


    pratos_nodes = dom.getElementsByTagName("prato")
    
    catalogo = {}
    
    for prato in pratos_nodes:
        id_prato = prato.getAttribute("id")
        nome = obter_texto(prato, "nome")
        descricao = obter_texto(prato, "descricao")
        calorias = obter_texto(prato, "calorias")
        tempo_preparo = obter_texto(prato, "tempoPreparo")
        
        preco_node = prato.getElementsByTagName("preco")[0]
        preco_valor = preco_node.firstChild.nodeValue.strip() if preco_node.firstChild else ""
        moeda = preco_node.getAttribute("moeda")
        preco_formatado = f"{preco_valor} ({moeda})"
        
        ingredientes_nodes = prato.getElementsByTagName("ingrediente")
        ingredientes = [node.firstChild.nodeValue.strip() for node in ingredientes_nodes if node.firstChild]
        
        catalogo[id_prato] = {
            "nome": nome,
            "descricao": descricao,
            "ingredientes": ingredientes,
            "preco": preco_formatado,
            "calorias": calorias,
            "tempoPreparo": tempo_preparo
        }

    while True:
        print("\n" + "="*35)
        print(" MENU DE PRATOS ".center(35, "="))
        print("="*35)
        
        for id_p, info in catalogo.items():
            print(f"[{id_p}] - {info['nome']}")
        print("-" * 35)
        
        opcao = input("Digite o ID do prato para ver mais detalhes (ou 'sair' para encerrar): ").strip().upper()
        
        if opcao == 'SAIR':
            print("Encerrando o programa...")
            break
            
        if opcao in catalogo:
            prato = catalogo[opcao]
            print("\n" + f" Detalhes do Prato: {opcao} ".center(35, "*"))
            print(f"Nome: {prato['nome']}")
            print(f"Descrição: {prato['descricao']}")
            print("Ingredientes:")
            for ing in prato['ingredientes']:
                print(f"  - {ing}")
            print(f"Preço: {prato['preco']}")
            print(f"Calorias: {prato['calorias']} kcal")
            print(f"Tempo de Preparo: {prato['tempoPreparo']}")
            print("*" * 35)
        else:
            print("\n[!] ID inválido! Por favor, verifique a lista e tente novamente.")

if __name__ == "__main__":
    main()