import xml.etree.ElementTree as ET
import json
import os

def parse_xml_para_dicionario(caminho_arquivo):
    """Lê o arquivo XML e o converte para um dicionário Python estruturado."""
    tree = ET.parse(caminho_arquivo)
    root = tree.getroot()
    
    dados = {"imobiliaria": {"imoveis": []}}
    
    for imovel in root.findall('imovel'):
        imovel_dict = {}
        
        descricao = imovel.find('descricao')
        if descricao is not None:
            imovel_dict['descricao'] = descricao.text
            
        proprietario = imovel.find('proprietario')
        if proprietario is not None:
            prop_dict = {}
            
            nome = proprietario.find('nome')
            if nome is not None:
                prop_dict['nome'] = nome.text
                
            telefones = proprietario.findall('telefone')
            if telefones:
                prop_dict['telefones'] = [t.text for t in telefones]
                
            emails = proprietario.findall('email')
            if emails:
                prop_dict['emails'] = [e.text for e in emails]
                
            imovel_dict['proprietario'] = prop_dict
            
        endereco = imovel.find('endereco')
        if endereco is not None:
            end_dict = {}
            for campo in ['rua', 'bairro', 'cidade', 'numero']:
                elem = endereco.find(campo)
                if elem is not None:
                    end_dict[campo] = elem.text
            imovel_dict['endereco'] = end_dict
            
        carac = imovel.find('caracteristicas')
        if carac is not None:
            carac_dict = {}
            for campo in ['tamanho', 'numQuartos', 'numBanheiros']:
                elem = carac.find(campo)
                if elem is not None:
                    carac_dict[campo] = elem.text
            imovel_dict['caracteristicas'] = carac_dict
            
        valor = imovel.find('valor')
        if valor is not None:
            imovel_dict['valor'] = valor.text
            
        dados['imobiliaria']['imoveis'].append(imovel_dict)
        
    return dados

def main():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
    arquivo_xml = os.path.join(diretorio_atual, 'imobiliaria.xml')
    arquivo_json = os.path.join(diretorio_atual, 'imobiliaria.json')
    
    try:
        dados_dicionario = parse_xml_para_dicionario(arquivo_xml)
        
        with open(arquivo_json, 'w', encoding='utf-8') as f:
            json.dump(dados_dicionario, f, ensure_ascii=False, indent=4)
            
        print(f"Sucesso! Arquivo JSON gerado em: {arquivo_json}")
        
    except FileNotFoundError:
        print(f"[Erro] O arquivo '{arquivo_xml}' não foi encontrado.")
    except ET.ParseError as e:
        print(f"[Erro de Parse] Verifique se o arquivo XML está bem formatado e SEM a tag DTD (<!DOCTYPE>). Detalhe: {e}")
    except Exception as e:
        print(f"[Erro Inesperado]: {e}")

if __name__ == "__main__":
    main()