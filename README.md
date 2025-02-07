# Tradutor_Legenda_offline

Script em Python traduz arquivos de legenda (.srt) do inglês para o português usando a biblioteca Argos Translate e coforme o modelo.argosmodel uma GPU Nvidia, se disponível.

## Funcionalidades

- Atualiza e instala pacotes de tradução.
- Traduz linhas de arquivos .srt.
- Utiliza a GPU Nvidia para acelerar a tradução, se disponível.

## Requisitos

- Python 3.6 ou superior
- Sistema operacional Windows 11 ou Linux Ubuntu
- Pacotes e bibliotecas:
  - os
  - time
  - argostranslate
  - torch
  - tqdm

## Instalação

### Windows 11

1. Instale o Python 3.6 ou superior a partir do [site oficial](https://www.python.org/downloads/).
2. Abra o Prompt de Comando e instale os pacotes necessários:

```sh
pip install argostranslate tqdm
```

Para usar o uma GPU Nvidia, você precisará instalar o PyTorch:
```sh
pip install torch 
```

3. Certifique-se de que os drivers da Nvidia estão instalados corretamente.

### Linux Ubuntu

1. Instale o Python 3.6 ou superior:
```sh
sudo apt update
sudo apt install python3 python3-pip
```

2. Instale os pacotes necessários:
```sh
pip3 install argostranslate torch tqdm
```

Para usar o uma GPU Nvidia, você precisará instalar o PyTorch:
```sh
pip3 install torch 
```

3. Certifique-se de que os drivers da Nvidia estão instalados corretamente.

## Uso

1. Coloque o script `tradutor.py` no mesmo diretório ou em um nível superior às pastas onde os arquivos .srt em inglês estão localizados.
2. Certifique-se de que os arquivos .srt em inglês estejam organizados em pastas e subpastas conforme necessário.

3. Execute o script:
```sh
python tradutor.py
```
4. O script procurará arquivos que terminam em `en.srt` e os traduzirá, salvando-os com o sufixo `pt-br.srt`.

## Alterações Possíveis no script para ajustar o final do nome do arquivo a ser traduzido e do  sufixo do arquivo traduzido

- Para modificar os sufixos dos arquivos traduzidos, altere as seguintes variáveis no script:
  - `if file_name.endswith('en.srt'):` para `if file_name.endswith('<novo_sufixo>.srt'):` 


  - `new_file_name = file_name.replace('en.srt', 'pt-br.srt')` para `new_file_name = file_name.replace('<antigo_sufixo>.srt', '<novo_sufixo>.srt')`

## Estrutura do Projeto

```plaintext
/raiz_do_projeto
│
├── tradutor.py
├── pasta1/
│   ├── subpasta1/
│   │   ├── arquivo1_en.srt
│   │   ├── arquivo2_en.srt
│   └── subpasta2/
│       ├── arquivo3_en.srt
│
└── pasta2/
    ├── subpasta1/
    │   ├── arquivo4_en.srt
    └── subpasta2/
        ├── arquivo5_en.srt
        ├── arquivo6_en.srt
```

## Créditos

Este script foi desenvolvido para automatizar a tradução de arquivos de legenda usando a biblioteca Argos Translate e possivel utilização de GPU Nvidia conforme o modelo disponível da biblioteca Argos Translate .

```plaintext
 Modelo offline na utilização da CPU e de uma GPU Nvidia:


 translate-en_pt-1_0.argosmodel ├── modelo utiliza mais a CPU do que a GPU.


```
