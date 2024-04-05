library(rentrez)
library(XML)
library(dplyr)

setwd("/home/iruziky/Desktop/SearchEngine") # Diretório padrão
set_entrez_key("8aee6ec6123db1eac75f6d196ec7f6bc6409") # Acess-key para o ncbi

# Lendo o arquivo que contém o nome de todas as espécies
species <- read.table(
  "speciesNames.txt",
  sep = "\n",
  stringsAsFactors = FALSE)
species <- as.list(species$V1)

species <- species[-c(1: 25799)]
species[1]

# Salvando os dados de peixes sem mtDNA
ls_candidates <- list()

# Registrando quantos peixes já foram analisados, para salvar os dados a cada "x" repetições
controle <- 0

for (specie in species){
  cat("\n")
  cat(specie, ":\n")
  tryCatch(
    {
      # Fazendo uma busca no ncbi e armazenando
      res <- entrez_search(
        db = "nucleotide", 
        term = paste(specie, " [PORG] AND mitochondrion [ALL]"),
        retmax = 99999,
        use_history = TRUE) # Permite obter todos os resultados da busca
    },
    
    error = function(e)
    {
      Sys.sleep(60)
      res <- entrez_search(
        db = "nucleotide", 
        term = paste(specie, " [PORG] AND mitochondrion [ALL]"),
        retmax = 99999,
        use_history = TRUE) # Permite obter todos os resultados da busca
    }
  )
  
  Sys.sleep(0.1)
    
  # Acessando cada resultado da busca e registrando em xml
  recs <- entrez_fetch(
    db = "nucleotide",
    web_history = res$web_history,
    rettype = "xml",
    parsed = TRUE)
  
  # Realizando uma busca no xml
  lengsOfSearch <- xpathSApply(recs, "//GBSet/GBSeq/GBSeq_length", xmlValue)
  lengsOfSearch <- as.numeric(lengsOfSearch)
  
  # Variáveis de controle e de registro
  contador <- 0
  encontrados <- 0
  idsCol <- list()
  lengthsCoul <- list()
  
  # Procurando por resultados a partir do tamanho
  for (leng_ in lengsOfSearch)
  {
    # Parâmetro para identificar um peixe que possivelmente tem mtDNA
    if (leng_ >= 12000 && leng_ <= 22000)
    {
      # Regristando os dados
      idsCol <- append(idsCol, res$ids[contador + 1])
      lengthsCoul <- append(lengthsCoul, leng_)
      
      cat("ID: ", res$ids[contador + 1], "\nTamanho: ", leng_, "\n")
      encontrados <- encontrados + 1
    }
    # Obtendo a quantidade de mtDNA disponível
    contador <- contador + 1
  }
  
  # Salvando o nome do peixe, caso não tenho encontrado nenhum mtDNA
  if (encontrados == 0)
    ls_candidates <- append(ls_candidates, as.character(specie))

  else
  {
    # Criando um novo dataframe para cada peixe com mtDNA e registrando id e tamanho de cada mtDNA disponível
    novo_dt <- data.frame(ids = as.character(idsCol), tamanhos = as.integer(lengthsCoul))
    caminho <- paste0("/home/iruziky/Desktop/SearchEngine/resultados/", specie, ".csv")
    write.csv(novo_dt, caminho, row.names = FALSE)
  }
  
  cat("\nMitogenomas encontrados: ", encontrados, "\n")

  controle <- controle + 1
  if (controle == 100)
  {
    # Lendo os nomes que já foram registrado para unir posteriormente aos novos nomes encontrados
    coluna_antiga <- read.csv("candidatos.csv")

    # Convertendo a lista em um dataframe com uma coluna chamada "Candidatos"
    coluna_nova <- data.frame(Candidatos = unlist(ls_candidates))
    
    # Juntando a lista antiga com a nova
    coluna_resultante <- bind_rows(coluna_antiga, coluna_nova)
    
    # Salvando o dataframe atualizado como um arquivo CSV
    write.csv(coluna_resultante, "candidatos.csv", row.names = FALSE)
    
  
    # Esvaziando o vetor para não consumir memória, pois já  regristamos seus dados
    ls_candidates <- list()
    
    # Reiniciando a contagem de iterações
    controle <- 0 
    
    # Reiniciando contagem da média de tempo
    tempo_total <- 0
    
    # Apagando variáveis para liberar memória
    rm(coluna_antiga)
    rm(coluna_nova)
    rm(coluna_resultante)
  }
}