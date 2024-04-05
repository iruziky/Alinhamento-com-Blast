import os
import pandas as pd

result_dir = "/home/iruziky/resultados"

fileNames_list = os.listdir(result_dir)

# col_names = [
#     'slen', 'qstart', 'qend', 'sstart', 
#     'send', 'bitscore', 'score', 'length', 'pident', 'nident', 'mismatch', 
#     'positive', 'gapopen', 'gaps', 'ppos'
# ]
uniResults = []
for fileName in fileNames_list:
    file_path = os.path.join(result_dir, fileName)  

    with open(file_path, 'r') as searchResult:
        file = searchResult.read()
        lines = file.split('\n')    

    # resultLines = []
    # for i in range (10):
    #     line = lines[i].split(',')
    #     resultLines.append(line[12:27])
    
    #df = pd.DataFrame(data=resultLines, columns=col_names)

    # Salvando o DataFrame como um arquivo CSV
    #csv_file_path = f"/home/iruziky/alignment/{fileName}.csv"  # Definindo o caminho para salvar o CSV
    #df.to_csv(csv_file_path, index=False)  # index=False para não salvar o índice do DataFrame

    
    line = lines[0].split(',')
    line[11] = fileName
    uniResults.append(line[11:27])

col_names = [
    'specie', 'slen', 'qstart', 'qend', 'sstart', 
    'send', 'bitscore', 'score', 'length', 'pident', 'nident', 'mismatch', 
    'positive', 'gapopen', 'gaps', 'ppos'
]

df = pd.DataFrame(data=uniResults, columns=col_names)

# Salvando o DataFrame como um arquivo CSV
csv_file_path = f"/home/iruziky/alignment/geral.csv"  # Definindo o caminho para salvar o CSV
df.to_csv(csv_file_path, index=False)  # index=False para não salvar o índice do DataFrame