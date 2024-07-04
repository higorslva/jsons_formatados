import json
import re
import os

def extract_options_and_links(content):
    pattern = re.compile(r'\[(.*?)\]\((.*?)\)')
    matches = pattern.findall(content)
    return matches

def main():
    input_directory = 'conteudo_variado/limpo'  
    output_directory = 'conteudo_variado/formatado' 
    
    os.makedirs(output_directory, exist_ok=True)
    
    for filename in os.listdir(input_directory):
        if filename.startswith('response_') and filename.endswith('.json'):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, filename)
            
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            content = data.pop('content', '')
            metadata = data.pop('metadata', {})
            source_url = metadata.get('sourceURL', '')
            
            descriptions_and_links = extract_options_and_links(content)
        
            content = re.sub(r'\[(.*?)\]\((.*?)\)', r'', content)          

            output_data = {
                "opcao_e_link": [],
                "sourceURL": source_url,
                "descricao": content
            }
            for description, link in descriptions_and_links:
                output_data["opcao_e_link"].append({
                    "opcao": description,
                    "link": link
                })

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
