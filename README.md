blastAlign:
Alinha uma sequência contra outra

remote_alignment:
Alinha uma sequência contra o NCBI

filter_alignment.py:
o remote-alignment retorna muitas colunas, e esse script é só pra selecionar e organizar as que desejamos e salvar em um .csv

mtOrNot.R:
Verifica se um peixe tem mitocôndria publicada no NCBI

bwa.py:
A partir de um diretório contendo arquivos fastas indexados, baixa o .sra para cada fasta (o início do nome do fasta deve ser o nome do sra que ele corresponde), "descompacta", executa o bwa e remove o .sra
obs: Não deve funcionar em .sra que tem menos de 10 caracteres no nome. preciso ajeitar isso
