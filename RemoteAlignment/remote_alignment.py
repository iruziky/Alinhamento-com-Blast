from Bio.Blast import NCBIWWW
from Bio import SeqIO
import os, subprocess, sys
import time

# Diretório padrão para a pasta com os fastas
fastas_dir = "/home/iruziky/Desktop/Bioinformatic/novoplasty/fastas"

# Obtendo o nome de cada fasta no diretório padrão
fastas = os.listdir(fastas_dir)

# Iterando sobre o nome de cada arquivo no diretório padrão
for fasta in fastas:
    print("Arquivo atual:", fasta, "\n")

    # Abrindo apenas arquivos fasta
    fasta_base, fasta_extensao = os.path.splitext(fasta)
    if fasta_extensao not in {'.fasta', '.fa', 'fsa'}:
        continue  # Pula a iteração caso o arquivo não seja fasta

    # Caminho completo para o arquivo fasta
    fasta_path = os.path.join(fastas_dir, fasta)

    # Opções de saída ($ blastn -help para mais opções)
    options = "10 qseqid qgi qacc qaccver qlen sseqid sallseqid sgi sallgi sacc saccver sallacc slen qstart qend sstart send bitscore score length pident nident mismatch positive gapopen gaps ppos staxid ssciname scomname sblastname sskingdom staxids sscinames scomnames sblastnames sskingdoms stitle salltitles sstrand qcovs qcovhsp qcovus"

    # Caminho para o resultado
    results_path = f"/home/iruziky/Desktop/Bioinformatic/NCBI/blast/RemoteAlignment/results/{fasta_base}"

    # Pulando a iteração caso já exista um arquivo de resultado para este fasta
    if os.path.exists(results_path):
        print("Este arquivo já possui um alinhamento listado \n")
        continue

    # Formulando o comando de pesquisa do blastn
    command = f'blastn -query {fasta_path} -db nt -remote -out {results_path} -max_target_seqs 10 -outfmt "{options}"'    
    print(command)

    # Executando o comando de pesquisa
    process = subprocess.run(command, capture_output=True, text=True, shell=True)
    time.sleep(5)    

    # Caso ocorra um erro neste alinhamento, pular para o próximo
    if process.returncode != 0:
        print("Ocorreu um erro... \n")
        continue

    print("Execução concluída com sucesso \n")

    # Escrevendo os resultados em um arquivo
    #with open(result_path, "r") as blast_result:
    #    # Salvando o resultado em um arquivo de texto
    #    linhas = blast_result.read()
    #    linha = linhas.split("\n")[0]
    #    linha_separada = linha.split("\t")