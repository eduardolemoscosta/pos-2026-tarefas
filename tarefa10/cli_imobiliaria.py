import json
import os

def exibir_detalhes(imovel):
    """Exibe as informações do imóvel de forma organizada e legível."""
    print(f"\n{'='*50}")
    print(f" IMÓVEL: {imovel.get('descricao', 'Sem descrição').upper()}")
    print(f"{'='*50}")

    prop = imovel.get('proprietario', {})
    print(f"\n👤 PROPRIETÁRIO:")
    print(f"   Nome: {prop.get('nome')}")
    
    telefones = prop.get('telefones', [])
    if telefones:
        print(f"   Telefones: {', '.join(telefones)}")
    
    emails = prop.get('emails', [])
    if emails:
        print(f"   E-mails: {', '.join(emails)}")

    end = imovel.get('endereco', {})
    numero = end.get('numero', 'Não informado')
    print(f"\n📍 ENDEREÇO:")
    print(f"   Rua: {end.get('rua')}, Nº {numero}")
    print(f"   Bairro: {end.get('bairro')}")
    print(f"   Cidade: {end.get('cidade')}")

    carac = imovel.get('caracteristicas', {})
    print(f"\n🏠 CARACTERÍSTICAS:")
    print(f"   Tamanho: {carac.get('tamanho')}")
    print(f"   Quartos: {carac.get('numQuartos')}")
    print(f"   Banheiros: {carac.get('numBanheiros')}")

    print(f"\n💰 VALOR: {imovel.get('valor')}")
    print(f"{'='*50}\n")

def main():
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    caminho_json = os.path.join(diretorio_script, 'imobiliaria.json')

    try:
        with open(caminho_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except FileNotFoundError:
        print(f"\n[Erro] O arquivo 'imobiliaria.json' não foi encontrado na pasta.")
        return
    except json.JSONDecodeError:
        print(f"\n[Erro] O arquivo 'imobiliaria.json' contém erros de formatação.")
        return

    imoveis = dados.get("imobiliaria", {}).get("imoveis", [])

    if not imoveis:
        print("\nNenhum imóvel encontrado no arquivo.")
        return

    while True:
        print("\n" + "--- SISTEMA DE CONSULTA IMOBILIÁRIA ---".center(50))
        print("-" * 50)
        
        for i, imovel in enumerate(imoveis, start=1):
            print(f"[{i}] {imovel.get('descricao')}")
        
        print("[0] Sair do programa")
        print("-" * 50)

        escolha = input("Escolha o número do imóvel para detalhes: ").strip()

        if escolha == '0':
            print("\nEncerrando... Até logo!")
            break

        try:
            indice = int(escolha) - 1
            if 0 <= indice < len(imoveis):
                exibir_detalhes(imoveis[indice])
                input("Pressione ENTER para voltar ao menu...")
            else:
                print("\n[!] Ops! Escolha um número que esteja na lista.")
        except ValueError:
            print("\n[!] Por favor, digite apenas números.")

if __name__ == "__main__":
    main()