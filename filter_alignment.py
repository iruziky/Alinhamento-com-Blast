import os
import pandas as pd

result_dir = "\\Users\\Iruziky\\Downloads\\mtDNAxNCBI"

fileNames_list = os.listdir(result_dir)

uniResults = []
for fileName in fileNames_list:
    file_path = os.path.join(result_dir, fileName)  

    with open(file_path, 'r') as searchResult:
        file = searchResult.read()
        lines = file.split('\n')    
    
    try:
        line = lines[0].split(',')
        line[11] = fileName
        uniResults.append(line[11:27])

    except:
        print("Erro ao filtrar os dados do arquivo",fileName,
              "\n Este arquivo será desconsiderado")
        continue        

col_names = [
    'specie', 'slen', 'qstart', 'qend', 'sstart', 
    'send', 'bitscore', 'score', 'length', 'pident', 'nident', 'mismatch', 
    'positive', 'gapopen', 'gaps', 'ppos'
]

df = pd.DataFrame(data=uniResults, columns=col_names)

# Salvando o DataFrame como um arquivo CSV
csv_file_path = f"\\Users\\Iruziky\\Desktop\\geral.csv"  # Definindo o caminho para salvar o CSV
df.to_csv(csv_file_path, index=False)  # index=False para não salvar o índice do DataFrame
