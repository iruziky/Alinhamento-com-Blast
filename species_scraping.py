from bs4 import BeautifulSoup

# Caminho para o arquivo HTML local
file_path = '/home/iruziky/Área de Trabalho/ClassificationTree.html'

# Ler o conteúdo do arquivo HTML
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Analisar o HTML usando BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Encontrar todas as tags <a> com o atributo href
links = soup.find_all('a', href=True)

# Abrindo arquivo para salvar os nomes
arquivo = open("speciesNames.txt", "w")

# Extrair e imprimir o conteúdo das tags <a> com href
for link in links:
    arquivo.write(link.text + "\n")
arquivo.close()