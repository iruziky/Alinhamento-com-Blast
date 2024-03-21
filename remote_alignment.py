from Bio.Blast import NCBIWWW
from Bio import SeqIO
import os, subprocess, sys

# Diretório padrão para a pasta com os fastas
fastas_dir = "/home/iruziky/fastas"
# Caminho para o arquivo de saída
result_dir = "/home/iruziky/resultados"

# Obtendo o nome de cada fasta no diretório padrão
fastas = os.listdir(fastas_dir)

# Iterando sobre o nome de cada arquivo no diretório padrão
for fasta in fastas:
    # Abrindo apenas arquivos .fa e .fasta
    nome_base, extensao = os.path.splitext(fasta)
    if extensao in {'.fasta', '.fa'}:
        fasta = nome_base
    else:
        continue  # Pula a iteração caso o arquivo não seja .fasta e nem .fa

    # Caminho completo para o arquivo fasta
    fasta_path = os.path.join(fastas_dir, (nome_base + extensao))

    # Caminho  completo para o resultado
    result_path = result_dir + nome_base

    # Opções de saída ($ blastn -help para mais opções)
    options = "10 qseqid qgi qacc qaccver qlen sseqid sallseqid sgi sallgi sacc saccver sallacc slen qstart qend sstart send bitscore score length pident nident mismatch positive gapopen gaps ppos staxid ssciname scomname sblastname sskingdom staxids sscinames scomnames sblastnames sskingdoms stitle salltitles sstrand qcovs qcovhsp qcovus"

    # Formulando o comando de pesquisa do blastn
    command = f'blastn -query {fasta_path} -db nt -remote -out {result_path} -max_target_seqs 10 -outfmt "{options}"'    
    print(command)

    # Executando o comando de pesquisa
    process = subprocess.run(command, capture_output=True, text=True, shell=True)

    # Caso ocorra um erro neste alinhamento, pular para o próximo
    if process.returncode != 0:
        print(process.returncode)
        continue

    # Escrevendo os resultados em um arquivo
    #with open(result_path, "r") as blast_result:
    #    # Salvando o resultado em um arquivo de texto
    #    linhas = blast_result.read()
    #    linha = linhas.split("\n")[0]
    #    linha_separada = linha.split("\t")
    