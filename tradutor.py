import os
import time
from argostranslate import package, translate
import torch
from tqdm import tqdm

def install_packages():
    package.update_package_index()
    available_packages = package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == "en" and x.to_code == "pt", available_packages
        )
    )
    package_path = package_to_install.download()
    package.install_from_path(package_path)

def configure_device():
    if torch.cuda.is_available():
        os.environ["ARGOS_DEVICE_TYPE"] = "cuda"
        torch.cuda.set_per_process_memory_fraction(0.9)
        return torch.device("cuda:0")
    else:
        os.environ["ARGOS_DEVICE_TYPE"] = "cpu"
        user_input = input("GPU Nvidia não encontrada. Deseja continuar utilizando a CPU? (y/n): ")
        if user_input.lower() != 'y':
            print("Tradução cancelada pelo usuário.")
            return None
        return torch.device("cpu")

def translate_line(line, translator, device):
    try:
        with torch.cuda.device(device) if device.type == "cuda" else torch.device("cpu"):
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
    install_packages()
    installed_languages = translate.get_installed_languages()
    translator = installed_languages[0].get_translation(installed_languages[1])
    device = configure_device()
    if device is None:
        return

    for root, dirs, files in os.walk(current_dir):
        for file_name in files:
            # Verifique se o arquivo corresponde aos critérios
            if (file_name.endswith('.srt') or file_name.endswith('.en.srt') or file_name.endswith('_en.srt')) and \
            not (file_name.endswith('.pt-br.srt') or file_name.endswith('_pt-br.srt') or file_name.endswith('PT.srt')):
                file_path = os.path.join(root, file_name)

            # Substituições específicas para evitar sobreposições
                                
                if file_name.endswith('_en.srt'):
                    new_file_name = file_name.replace('_en.srt', '_pt-br.srt')
                    new_file_name = new_file_name.replace('.en', '')
                
                elif file_name.endswith('.en.srt'):
                    new_file_name = file_name.replace('.en.srt', '.pt-br.srt')
                    new_file_name = new_file_name.replace('_en', '')


                elif file_name.endswith('.srt'):
                    new_file_name = file_name.replace('.srt', '.pt-br.srt')
                    new_file_name = new_file_name.replace('en', '')
          
                new_file_path = os.path.join(root, new_file_name)

                if os.path.exists(new_file_path):
                    print(f"Translation already exists for: {new_file_path}")
                    continue

                print(f"Translating file: {file_path}")

                start_time = time.time()
                try:
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
