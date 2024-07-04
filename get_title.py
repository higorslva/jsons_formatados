import os
import json
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict

def get_page_title(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string if soup.title else "No Title Found"
            return title.strip()
        else:
            return "Failed to retrieve"
    except Exception as e:
        return f"Error: {e}"

def update_json_files(root_directory):
    for root, dirs, files in os.walk(root_directory):
        if "formatado" in root:
            json_files = [file for file in files if file.endswith('.json')]
            for json_file in json_files:
                file_path = os.path.join(root, json_file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        source_url = data.get("sourceURL", "")
                        if source_url:
                            opcao_menu = get_page_title(source_url)
                            print(f"Adicionando 'opcao_menu': {opcao_menu} no arquivo {file_path}")

                            # Reordenar o dicionário para adicionar opcao_menu no início
                            new_data = OrderedDict()
                            new_data["opcao_menu"] = opcao_menu
                            for key, value in data.items():
                                if key == "opcao_e_link":
                                    new_data["opcao_e_link"] = [
                                        {**{"opcao_submenu": item.pop("opcao")}, **item} for item in value
                                    ]
                                else:
                                    new_data[key] = value

                            with open(file_path, 'w', encoding='utf-8') as file:
                                json.dump(new_data, file, ensure_ascii=False, indent=4)
                            print(f"Arquivo {file_path} atualizado com sucesso.")
                        else:
                            print(f"URL de origem não encontrada no arquivo {file_path}.")
                except Exception as e:
                    print(f"Erro ao processar o arquivo {file_path}: {e}")

if __name__ == '__main__':
    update_json_files('.')
