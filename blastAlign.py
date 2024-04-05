from Bio.Blast.Applications import * # Biblioteca para acessar o Blast remotamente
import os # Biblioteca padrão para interagir com o sistema
import sys
import numpy

def escrever(file, text):
    arquivo = open(file, "a")
    arquivo.write(text)
    arquivo.close

dir =  '/home/iruziky/Desktop/novoplasty/'
files = os.listdir(dir) # Obtendo o nome de todos os arquivos no diretório referente
matriz = numpy.array([["qlen", "qstart", "qend", "sstart", "send", "positive", "gaps", "mismatch", "pident"]])

for fasta in files:
    our_file = '/home/iruziky/Desktop/unicycler/' + fasta
    this_file = dir + fasta
    final_file = '/home/iruziky/Desktop/comparação/' + fasta

    # Procurando por um arquivo de nome equivalente em outro diretório
    if (os.path.exists(our_file)):
        # Formulando o comando blast
        comando_blastn = NcbiblastnCommandline(
        query=this_file, subject=our_file, \
        outfmt="6 qlen qstart qend sstart send positive gaps mismatch pident", \
        out=final_file)
        print(comando_blastn)
        
        # Executando
        stdout, stderr = comando_blastn()
        # Abrindo resultado
        blast_result = open(final_file,"r")
        
        # Salvando o resultado em um arquivo de texto
        linhas = blast_result.read()
        linha = linhas.split("\n")[0]
        linha_separada = linha.split("\t")

        matriz = numpy.vstack([matriz, linha_separada])
     
        arquivo = open('/home/iruziky/Desktop/comparação/resultados.txt', 'a')
        arquivo.write(fasta + ":\n qlen qstart  qend    sstart  send    positive    gaps    mismatch    pident \n" + linha + "\n\n")
        arquivo.close()
        print(matriz)
        blast_result.close()
        os.remove(final_file)
        sys.exit()

    # Escrevendo o nome dos arquivos que não obtiveram correspondência
    else:
            escrever('/home/iruziky/Desktop/comparação/errors.txt', fasta + "\n")