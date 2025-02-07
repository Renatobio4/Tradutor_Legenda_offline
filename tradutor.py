import os
import time
from argostranslate import package, translate
import torch
from tqdm import tqdm

def install_packages():
    # Atualize o índice de pacotes e instale o pacote necessário
    package.update_package_index()
    available_packages = package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == "en" and x.to_code == "pt", available_packages
        )
    )
    package_path = package_to_install.download()
    package.install_from_path(package_path)

def translate_line(line, translator, device):
    try:
        # Configurar o dispositivo para utilizar a GPU Nvidia
        os.environ["ARGOS_DEVICE_TYPE"] = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Verifica se a GPU está disponível
        if torch.cuda.is_available():
            # Limita a utilização da memória da GPU
            torch.cuda.set_per_process_memory_fraction(0.9)
        else:
            raise RuntimeError("GPU Nvidia não encontrada. Certifique-se de que os drivers da Nvidia estão instalados corretamente.")
        
        # Traduzir usando o dispositivo
        with torch.cuda.device(device):
            return translator.translate(line)
    except Exception as e:
        print(f"Error translating line: {line}. Error: {e}")
        return line

def translate_srt(file_path, translator, device):
    translated_lines = []

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in tqdm(lines, desc="Translating lines"):
            if line.strip().isdigit() or '-->' in line:
                translated_lines.append(line)
            else:
                translated_lines.append(translate_line(line, translator, device) + '\n')

    return translated_lines

def main():
    print("Iniciando o processo de tradução...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Instalar pacotes de tradução
    install_packages()
    
    installed_languages = translate.get_installed_languages()
    translator = installed_languages[0].get_translation(installed_languages[1])

    for root, dirs, files in os.walk(current_dir):
        for file_name in files:
            if file_name.endswith('en.srt'):
                file_path = os.path.join(root, file_name)
                new_file_name = file_name.replace('en.srt', 'pt-br.srt')
                new_file_path = os.path.join(root, new_file_name)
                
                if os.path.exists(new_file_path):
                    print(f"Translation already exists for: {new_file_path}")
                    continue
                
                print(f"Translating file: {file_path}")
                start_time = time.time()
                try:
                    # Verifica se a GPU está disponível antes de traduzir
                    if torch.cuda.is_available():
                        device = torch.device("cuda:0")
                    else:
                        user_input = input("GPU Nvidia não encontrada. Deseja continuar utilizando a CPU? (y/n): ")
                        if user_input.lower() != 'y':
                            print("Tradução cancelada pelo usuário.")
                            continue
                        device = torch.device("cpu")
                    
                    translated_lines = translate_srt(file_path, translator, device)
                    with open(new_file_path, 'w', encoding='utf-8') as new_file:
                        new_file.writelines(translated_lines)
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    print(f"File saved as: {new_file_path}")
                    print(f"Translation completed in {elapsed_time:.2f} seconds")
                except Exception as e:
                    print(f"Error translating file {file_path}: {e}")

if __name__ == "__main__":
    main()
