from setuptools import setup, find_packages
import os

# Função para encontrar todos os arquivos em um diretório
def find_files(directory, file_extension):
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(file_extension):
                file_list.append(os.path.join(root, file))
    return file_list

# Encontre todos os arquivos .so na pasta raiz do projeto
so_files = find_files('.', '.so')

# Use a lista de arquivos .so como data_files
data_files = [(os.path.dirname(file), [file]) for file in so_files]

long_description = open("README.md").read()

setup(
    name='where_i_went',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'exifread',
        'folium',
        'tqdm',
        'branca==0.6.0',
        'certifi==2023.7.22',
        'charset-normalizer==3.2.0',
        'ExifRead==3.0.0',
        'idna==3.4',
        'Jinja2==3.1.2',
        'MarkupSafe==2.1.3',
        'numpy==1.25.2',
        'requests==2.31.0',
        'tqdm==4.66.1',
        'urllib3==2.0.4',
    ],
    data_files=data_files,  # Inclua os arquivos .so
    long_description=long_description,
    long_description_content_type='text/markdown',
)

