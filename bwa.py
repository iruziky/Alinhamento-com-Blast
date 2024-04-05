import subprocess
import sys
import os

# Formar uma URL a partir de um arquivo RR e baixar o resultado
def fastq_down(RR):
    for idx in range(1, 3):
        url = f"ftp://ftp.sra.ebi.ac.uk/vol1/fastq/{RR[0:6]}/0{RR[9:11]}/{RR[0:11]}/{RR[0:11]}_{idx}.fastq.gz"
        #OBS: formatando uma url com esse padrão é possível baixar arquivos do ncbi sem a necessidade de um gerenciador
            
        # Formulando os comandos para execução
        comando = f"curl -L {url} -o {RR}_{idx}.fastq.gz"

        # Executando os comandos caso os arquivos das URL's ainda não tenham sido baixados
        if not os.path.exists(f"{RR}_URL_{idx}_complete"):
            custom_print(comando)
            if exe_and_verify(RR, comando):
                processo = subprocess.run(f"touch {RR}_URL_{idx}_complete", check=False)
                return processo.returncode
        else:
            return 0

# Imprime no console e escreve no arquivo output ao mesmo tempo
def custom_print(message):
    print(message)
    output_file.write(message + "\n")

# Executa um comando e verifica se houve algum erro
def exe_and_verify(fasta, comando):
    result = subprocess.run(comando, shell=True, check=False)

    if result.returncode == 0:
        custom_print(f"\nComando executado com sucesso para {fasta}\n")
        return 1
    else:
        custom_print(f"Erro ao executar o comando para {fasta}. Código de retorno: {result.returncode}\n")
        return 0

# Criando um arquivo para anexar as saídas do programa
output_file = open("./output.txt", "w")

# É necessário que tenha neste diretório um arquivo chamado list.txt com os nomes dos fastas que serão montados
unicycler_dir = "/data/home/iruziky.medeiros/unicycler"
fastas_dir = "/data/home/iruziky.medeiros/fastas" # Diretório para os arquivos .fasta indexados

# Abrindo o arquivo que contém o nome dos fastas que serão usados
file_listFasta = f"{unicycler_dir}/list.txt"
if os.path.exists(file_listFasta):
    arquivo = open(file_listFasta)
else:
    custom_print(f"Arquivo não encontrado: {file_listFasta}\n")
    sys.exit() # Encerra a execução

# Separando cada linha do arquivo
linhas = arquivo.read()
linhas = linhas.split("\n")

# Executando uma sequência de comandos para os fastas em questão
for fasta in linhas:
    # Corrigindo arquivos .fasta para .fa
    nome_base, extensao = os.path.splitext(fasta)
    if extensao in {'.fasta', '.fa'}:
        fasta = nome_base
    else:
        continue  # Pula a iteração caso o arquivo não seja .fasta e nem .fa

    # Apenas executa caso o arquivo final (.sam) não exista
    if os.path.exists(f"{unicycler_dir}/resultados_dir/{fasta}.sam"):
        custom_print(f"O arquivo {fasta}.sam já existe")
        continue

    custom_print("\nArquivo atual: " + fasta + "\n")

    # Baixando os arquivos .fastq para o fasta em questão
    if fastq_down(fasta) != 0:
        custom_print(f"Error: não foi possível baixar os arquivos .fastq para {fasta}\n")
        continue

    # Formulando comando para executar o bwa mem e samtools
    comando_bwa = f"bwa mem -t 16 -M {fastas_dir}/{fasta}.fa \
    {unicycler_dir}/{fasta}_1.fastq.gz \
    {unicycler_dir}/{fasta}_2.fastq.gz \
    | samtools view -h -F 4 > {unicycler_dir}/resultados_dir/{fasta}.sam"

    # Executando o comando_bwa
    custom_print (f"Executando BWA mem e samtools para {fasta}\n")
    if not (exe_and_verify(fasta, comando_bwa)):
        continue
    
    # Removendo arquivos temporários
    custom_print (f"Removendo arquivos temporários para {fasta}...")
    os.remove(f"{fasta}_1.fastq.gz")
    os.remove(f"{fasta}_2.fastq.gz")
    os.remove(f"{fasta}_URL_1_complete")
    os.remove(f"{fasta}_URL_2_complete")
    custom_print (f"Arquivos removidos com sucesso\n")
    
    custom_print (f"CONCLUÍDO o processamento para {fasta}\n")
    custom_print ("---------------------------------------------------------------------------\n")

print("------------------->Execução concluída com sucesso<-------------------")
arquivo.close()
output_file.close()
