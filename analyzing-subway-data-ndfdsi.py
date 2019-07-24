#!/usr/bin/env python
# coding: utf-8

# # Subway Data Analysis
# 
# ## Introduction
# 
# O sistema de ônibus e trens de Nova Iorque - o Metro Transit Authority - [fornece seus dados para download](http://web.mta.info/developers/developer-data-terms.html#data) através de  arquivos CSV. Dentre as informações disponíveis estão os **registros semanais de dados das catracas do metrô**. 
# 
# 
# Estes registros contém contagens cumulativas das entradas e saídas, normalmente agrupadas em períodos de 4 horas, com dados adicionais que permitem identificar a estação e catraca específica correspondente a cada linha do arquivo. Neste projeto iremos utilizar um desses registros, mas não precisa baixar nada agora! O primeiro exercício será escrever um código Python para fazer isso por você :-)
# 
# 
# 

# # Sobre este projeto
# 
# Neste projeto você irá aplicar todos os conhecimentos adquiridos neste primeiro mês de curso, com tarefas básicas de aquisição e limpeza de dados. No processo iremos descobrir informações essenciais sobre os dados, utilizando o que foi aprendido no curso de estatística. 
# 
# O objetivo deste projeto é explorar a relação entre os dados das catracas do metrô de Nova Iorque e o clima no dia da coleta. Para isso, além dos dados do metrô, precisaremos dos dados de clima da cidade de Nova Iorque. 
# 
# Os principais pontos que serão verificados neste trabalho:
# 
# - Coleta de dados da internet
# - Utilização de estatística para análise de dados
# - Manipulação de dados e criação de gráficos simples com o `Pandas`
# 
# *Como conseguir ajuda*: Sugerimos que busque apoio nos canais abaixo, na seguinte ordem de prioridade:
# 
# | Tipo de dúvida\Canais         	| Google 	| Fórum 	| Slack 	| Email 	|
# |-------------------------------	|--------	|-------	|-------	|-------	|
# | Programação Python e Pandas    	| 1      	| 2     	| 3     	|       	|
# | Requisitos do projeto         	|        	| 1     	| 2     	| 3     	|
# | Partes específicas do Projeto 	|        	| 1     	| 2     	| 3     	|
# 
# Os endereços dos canais são:
# 
# - Fórum: https://discussions.udacity.com/c/ndfdsi-project
# - Slack: [udacity-br.slack.com](https://udacity-br.slack.com/messages/C5MT6E3E1)
# - Email: data-suporte@udacity.com
# 
# **Espera-se que o estudante entregue este relatório com:**
# 
# - Todos os exercícios feitos, com atenção especial para os trechos de código a completar (sinalizados com `# your code here`), pois eles são essenciais para que o código rode corretamente
# - O arquivo ipynb exportado como HTML
# 
# Para entregar este projeto envie este `.ipynb` preenchido e o HTML, zipados, na página correspondente da sala de aula.

# # Sobre o dataset
# 
# Descrição das colunas
# <pre>
# C/A,UNIT,SCP,STATION,LINENAME,DIVISION,DATE,TIME,DESC,ENTRIES,EXITS
#   
# C/A      = Agrupamento de catracas de que a catraca faz parte (_Control Area_)
# UNIT     = Cabine de controle associada à estação onde a catraca se encontra (_Remote Unit for a station_)
# SCP      = Endereço específico da catraca (_Subunit Channel Position_)
# STATION  = Nome da estação onde a catraca se encontra
# LINENAME = Código representando todas linhas que passam na estação*
# DIVISION = Código representando a concessionária original da linha, antes da prefeitura assumir a gestão   
# DATE     = Representa a data (no formato MM-DD-YY) do evento de auditoria agendado
# TIME     = Representa o horário (hh:mm:ss) do evento de auditoria agendado
# DESc     = Descreve o tipo de evento de auditoria registrado:
#            1. "REGULAR" representando um evento de auditoria padrão, em que a contagem é feita a cada 4 horas
#            2. "RECOVR AUD" significa que o valor específico estava perdido, mas foi recuperado posteriormente 
#            3. Diversos códigos sinalizam situações em que auditorias são mais frequentes devido a atividades de
#               planejamento ou solução de problemas. 
# ENTRIES  = A contagem cumulativa de entradas associadas à catraca desde o último registro
# EXITS    = A contagem cumulativa de saídas associadas à catraca desde o último registro
# 
# *  Normalmente as linhas são representadas por um caractere. LINENAME 456NQR significa que os trens 4, 5, 6, N, Q e R passam pela estação.
# </pre>

# # Lembretes
# 
# Antes de começarmos, alguns lembretes devem ter em mente ao usar os notebooks iPython:
# 
# - Lembre-se de que você pode ver do lado esquerdo de uma célula de código quando foi executado pela última vez se houver um número dentro das chaves.
# - Quando você inicia uma nova sessão do notebook, certifique-se de executar todas as células até o ponto em que você deixou a última vez. Mesmo que a saída ainda seja visível a partir de quando você executou as células em sua sessão anterior, o kernel começa em um estado novo, então você precisará recarregar os dados, etc. em uma nova sessão.
# - O ponto anterior é útil para ter em mente se suas respostas não correspondem ao que é esperado nos questionários da aula. Tente recarregar os dados e execute todas as etapas de processamento um a um para garantir que você esteja trabalhando com as mesmas variáveis e dados que estão em cada fase do questionário.

# ## Seção 1 - Coleta de Dados
# 
# ### *Exercicio 1.1*
# 
# Mãos a obra!! Agora é sua vez de coletar os dados. Escreva abaixo um código python que acesse o link http://web.mta.info/developers/turnstile.html e baixe os arquivos do mês de junho de 2017. O arquivo deverá ser salvo com o nome turnstile_170610.txt onde 10/06/17 é a data do arquivo.
# 
# <blockquote>
#     <p>Caso o site esteja fora do ar, use essa url:</p>
#     <p>https://s3.amazonaws.com/video.udacity-data.com/topher/2018/November/5bf32290_turnstile/turnstile.html</p>
# </blockquote>
# 
# Abaixo seguem alguns comandos que poderão te ajudar:
# 
# Utilize a biblioteca **urllib** para abrir e resgatar uma página da web. Utilize o comando abaixo onde **url** será o caminho da página da web onde se encontra o arquivo:
# 
# ```python
# u = urllib.urlopen(url)
# html = u.read()
# ```
# 
# Utilize a biblioteca **BeautifulSoup** para procurar na página pelo link do arquivo que deseja baixar. Utilize o comando abaixo para criar o seu objeto *soup* e procurar por todas as tags 'a'no documento:
#  
#  
# ```python
# soup = BeautifulSoup(html, "html.parser")
# links = soup.find_all('a')
# ```
# 
# Uma dica para baixar apenas os arquivos do mês de junho é verificar a data no nome do arquivo. Por exemplo, para baixar o arquivo do dia 17/06/2017 verifique se o link termina com *"turnstile_170610.txt"*. Se não fizer isso você baixará todos os arquivos da página. Para fazer isso utilize o comando conforme abaixo:
# 
# ```python
# if '1706' in link.get('href'):
# ```
# 
# E a dica final é utilizar o comando abaixo para fazer o download do arquivo txt:
# 
# ```python
# urllib.urlretrieve(link_do_arquivo, filename)
# ```
# 
# Lembre-se, primeiro, carregue todos os pacotes e funções que você estará usando em sua análise.

# In[1]:


import urllib
from urllib.request import urlretrieve
from bs4 import BeautifulSoup

url = 'http://web.mta.info/developers/turnstile.html'
u = urllib.request.urlopen(url)
html = u.read()

soup = BeautifulSoup(html, "html.parser")
links = soup.select('a[href*="1706"]')
url2 = url.split('turnstile')[0]

file_names = []

for link in links:
    aux = link.get('href')
    names = link.get('href').split("/")[3]
    file_names.append(names)
    urlretrieve(url2+aux, file_names[0])
    print(url2+aux)


# ### *Exercicio 1.2*
# 
# Escreva uma função que pegue a lista de nomes dos arquivos que você baixou no exercicio 1.1 e consolide-os em um único arquivo. Deve existir apenas uma linha de cabeçalho no arquivo de saida. 
# 
# Por exemplo, se o arquivo_1 tiver:
# linha 1...
# linha 2...
# 
# e o outro arquivo, arquivo_2 tiver:
# linha 3...
# linha 4...
# linha 5...
# 
# Devemos combinar o arquivo_1 com arquivo_2 em um arquivo mestre conforme abaixo:
# 
# 'C/A, UNIT, SCP, DATEn, TIMEn, DESCn, ENTRIESn, EXITSn'
# linha 1...
# linha 2...
# linha 3...
# linha 4...
# linha 5...
# 
# **OBS:** Note que algumas colunas foram descartadas!

# In[2]:


import glob 

def create_master_turnstile_file(filenames, output_file):
    with open(output_file, 'w') as outfile:
        outfile.write('C/A,UNIT,SCP,STATION, LINENAME, DIVISION, DATEn,TIMEn,DESCn,ENTRIESn,EXITSn\n')
        for fname in filenames:
            with open(fname) as infile:
                infile.readline()
                for line in infile:
                    outfile.write(line)
                    
files = glob.glob("*.txt")                                  
create_master_turnstile_file(files, 'master-file.txt')


# ### *Exercicio 1.3*
# 
# Neste exercício, escreva um função que leia o master_file criado no exercicio anterior e carregue-o em um pandas dataframe. Esta função deve filtrar para que o dataframe possua apenas linhas onde a coluna "DESCn" possua o valor "Regular".
# 
# Por exemplo, se o data frame do pandas estiver conforme abaixo:
#     
#     ,C/A,UNIT,SCP,DATEn,TIMEn,DESCn,ENTRIESn,EXITSn
#     0,A002,R051,02-00-00,05-01-11,00:00:00,REGULAR,3144312,1088151
#     1,A002,R051,02-00-00,05-01-11,04:00:00,DOOR,3144335,1088159
#     2,A002,R051,02-00-00,05-01-11,08:00:00,REGULAR,3144353,1088177
#     3,A002,R051,02-00-00,05-01-11,12:00:00,DOOR,3144424,1088231
# 
# O dataframe deverá ficar conforme abaixo depois de filtrar apenas as linhas onde a coluna DESCn possua o valor REGULAR:
# 
#     0,A002,R051,02-00-00,05-01-11,00:00:00,REGULAR,3144312,1088151
#     2,A002,R051,02-00-00,05-01-11,08:00:00,REGULAR,3144353,1088177
# 

# In[ ]:


import pandas as pd

def filter_by_regular(filename):
    turnstile_data = pd.read_csv(filename,error_bad_lines=False)
    turnstile_data[turnstile_data["DESCn"] == "REGULAR"]
    return turnstile_data

def get_dataframe():
    return filter_by_regular(files[1])

data = get_dataframe()

data.head()


# ### *Exercicio 1.4*
# 
# 
# Os dados do metrô de NY possui dados cumulativos de entradas e saidas por linha. Assuma que você possui um dataframe chamado df que contém apenas linhas para uma catraca em particular (unico SCP, C/A, e UNIT). A função abaixo deve alterar essas entradas cumulativas para a contagem de entradas desde a última leitura (entradas desde a última linha do dataframe).
# 
# Mais especificamente, você deverá fazer duas coisas:
# 
# 1. Criar uma nova coluna chamada ENTRIESn_hourly
# 
# 2. Inserir nessa coluna a diferença entre ENTRIESn da linha atual e a da linha anterior. Se a linha possuir alguma NAN, preencha/substitua por 1.
# 
# Dica: as funções do pandas shift() e fillna() pode ser úteis nesse exercicio.
# 
# Abaixo tem um exemplo de como seu dataframe deve ficar ao final desse exercicio:
# 
#            C/A  UNIT       SCP     DATEn     TIMEn    DESCn  ENTRIESn    EXITSn  ENTRIESn_hourly
#     0     A002  R051  02-00-00  05-01-11  00:00:00  REGULAR   3144312   1088151                1
#     1     A002  R051  02-00-00  05-01-11  04:00:00  REGULAR   3144335   1088159               23
#     2     A002  R051  02-00-00  05-01-11  08:00:00  REGULAR   3144353   1088177               18
#     3     A002  R051  02-00-00  05-01-11  12:00:00  REGULAR   3144424   1088231               71
#     4     A002  R051  02-00-00  05-01-11  16:00:00  REGULAR   3144594   1088275              170
#     5     A002  R051  02-00-00  05-01-11  20:00:00  REGULAR   3144808   1088317              214
#     6     A002  R051  02-00-00  05-02-11  00:00:00  REGULAR   3144895   1088328               87
#     7     A002  R051  02-00-00  05-02-11  04:00:00  REGULAR   3144905   1088331               10
#     8     A002  R051  02-00-00  05-02-11  08:00:00  REGULAR   3144941   1088420               36
#     9     A002  R051  02-00-00  05-02-11  12:00:00  REGULAR   3145094   1088753              153
#     10    A002  R051  02-00-00  05-02-11  16:00:00  REGULAR   3145337   1088823              243

# In[ ]:


def get_hourly_entries(df):
    df['ENTRIESn_hourly'] = data.ENTRIESn - data.ENTRIESn.shift(1)
    df['ENTRIESn_hourly'] = data['ENTRIESn_hourly'].fillna(1).apply(int) 
    return df

data = get_hourly_entries(data)
data.head()


# ### *Exercicio 1.5*
# 
# Faça o mesmo do exercicio anterior mas agora considerando as saidas, coluna EXITSn.
# Para isso crie uma coluna chamada de EXITSn_hourly e insira a diferença entre a coluna EXITSn da linha atual versus a linha anterior. Se tiver algum NaN, preencha/substitua por 0.
# 
# 

# In[ ]:


def get_hourly_exits(df): 
    df['EXITSn_hourly'] = df.EXITSn - df.EXITSn.shift(1)
    df = df.fillna(0)
    df['EXITSn_hourly'] = df['EXITSn_hourly'].apply(int) 
    return df

data = get_hourly_exits(data)
data.head()


# ### *Exercicio 1.6*
# 
# Dado uma variável de entrada que representa o tempo no formato de:
#      "00:00:00" (hora: minutos: segundos)
#     
# Escreva uma função para extrair a parte da hora do tempo variável de entrada
# E devolva-o como um número inteiro. Por exemplo:
#          
#          1) se a hora for 00, seu código deve retornar 0
#          2) se a hora for 01, seu código deve retornar 1
#          3) se a hora for 21, seu código deve retornar 21
#         
# Por favor, devolva a hora como um número inteiro.
# 

# In[ ]:


def time_to_hour(time):
    hour = int(time[0:2])
    return hour

data['Hour'] = data['TIMEn'].map(lambda time: time_to_hour(str(time)))

print(time_to_hour('00:45:32'))
print(time_to_hour('01:59:36'))
print(time_to_hour('21:15:02'))

data.head()


# ## Exercicio 2 - Análise dos dados
# 
# ### *Exercicio 2.1*
# 
# Para verificar a relação entre o movimento do metrô e o clima, precisaremos complementar os dados do arquivo já baixado com os dados do clima.
# Nós complementamos para você este arquivo com os dados de clima de Nova Iorque  e disponibilizamos na área de materiais do projeto. Você pode acessa-lo pelo link: https://s3.amazonaws.com/content.udacity-data.com/courses/ud359/turnstile_data_master_with_weather.csv
# 
# Agora que temos nossos dados em um arquivo csv, escreva um código python que leia este arquivo e salve-o em um data frame do pandas. 
# 
# Dica: 
# 
# Utilize o comando abaixo para ler o arquivo:
# 
# ```python
# pd.read_csv('output_list.txt', sep=",")
# ```
# 
# 

# In[ ]:


filename = "turnstile_data_master_with_weather.csv"

data_weather = pd.read_csv(filename)
data_weather.head(5)


# ### *Exercicio 2.2*
# 
# Agora crie uma função que calcule a quantidade de dias chuvosos, para isso retorne a contagem do numero de dias onde a coluna *"rain"* é igual a 1.
# 
# Dica: Você também pode achar que a interpretação de números como números inteiros ou float pode não
#      funcionar inicialmente. Para contornar esta questão, pode ser útil converter
#      esses números para números inteiros. Isso pode ser feito escrevendo cast (coluna como inteiro).
#      Então, por exemplo, se queríamos lançar a coluna maxtempi como um número inteiro, nós devemos
#      escrever algo como cast (maxtempi as integer) = 76, em oposição a simplesmente
#      onde maxtempi = 76.

# In[ ]:


def num_rainy_days(df):
    df['rain'] = df['rain'].apply(int)
    rainy_daysounts = len(df[df['rain'] == 1.0].groupby('DATEn'))
    return rainy_days    
    
num_rainy_days(data_weather)


# ### *Exercicio 2.3*
# 
# Calcule se estava nebuloso ou não (0 ou 1) e a temperatura máxima para fog (isto é, a temperatura máxima 
#      para dias nebulosos).

# In[ ]:


def max_temp_aggregate_by_fog(df):
    return df[df['fog']==1]['maxtempi'].max()

max_temp_aggregate_by_fog(data_weather)


# ### *Exercicio 2.4
# 
# Calcule agora a média de 'meantempi' nos dias que são sábado ou domingo (finais de semana):

# In[ ]:


def avg_weekend_temperature(df):
    df = pd.read_csv(filename, sep=",")
    df['DayOfWeek'] = pd.to_datetime(df['DATEn']).dt.weekday_name
    #mean_temp_weekends = df[(df['DayOfWeek'] =='Saturday') | (df['DayOfWeek']=="Sunday")]['meantempi'].mean()
    weekend_data = df[(df['DayOfWeek'] =='Saturday') | (df['DayOfWeek']=="Sunday")]['meantempi']
    mean_temp_weekends = weekend_data.mean()
    return mean_temp_weekends

avg_weekend_temperature(data_weather)


# ### *Exercicio 2.5
# 
# Calcule a média da temperatura mínima 'mintempi' nos dias chuvosos onde da temperatura mínima foi maior que do 55 graus:

# In[ ]:


def avg_min_temperature(df):
    df = pd.read_csv(filename, sep=",")
    
    rainy_days55 = data_weather[(data_weather['rain'] == 1 ) & (data_weather['mintempi'] > 55)]['mintempi']
    avg_min_temp_rainy = rainy_days55.mean()
    
    return avg_min_temp_rainy

avg_min_temperature(data_weather)


# ### *Exercicio 2.6
# 
# Antes de realizar qualquer análise, pode ser útil olhar para os dados que esperamos analisar. Mais especificamente, vamos examinR as entradas por hora em nossos dados do metrô de Nova York para determinar a distribuição dos dados. Estes dados são armazenados na coluna ['ENTRIESn_hourly'].
#     
# Trace dois histogramas nos mesmos eixos para mostrar as entradas quando esta chovendo vs quando não está chovendo. 
# Abaixo está um exemplo sobre como traçar histogramas com pandas e matplotlib:
#      
# ```python
# Turnstile_weather ['column_to_graph']. Hist ()
# ```   
#     

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt

def entries_histogram(turnstile_weather):
    
    plt.figure(figsize=(12,6))
    turnstile_weather[turnstile_weather['rain'] == 0]['ENTRIESn_hourly'].hist(color='Red',bins = 20, range=(1000, 9000)) # your code here to plot a historgram for hourly entries when it is raining
    turnstile_weather[turnstile_weather['rain'] == 1]['ENTRIESn_hourly'].hist(color='green',bins = 20, range=(1000, 9000)) # your code here to plot a histogram for hourly entries when it is not raining
    plt.legend(("No Rain","Rain"))
    plt.xlabel("Entries hours")
    plt.ylabel("Frequency")
    plt.title("Histograma de entradas por linha no Metrô de New York")
    return plt


entries_histogram(data_weather)


# ### *Exercicio 2.7
# 
# Os dados que acabou de plotar que tipo de ditribuição? Existe diferença na distribuição entre dias chuvosos e não chuvosos?

# ** Resposta **: 
# 
# Conforme observado esta é uma distribuição assimetrica positiva, devido a sua "cauda" mais longa à direita da ordenada segundo o blog. https://www.ensinoeinformacao.com/estatist-prob-curso-assimetria
# 
# Existe uma grande diferença de entradas entre dias chuvosos e não chuvosos, sendo que nos dias que não houve chuva teve quase o dobro de entradas no metrô do que nos dias que choveu.

# ### *Exercicio 2.8
# 
# Construa uma função que que retorne:
# 
# 1. A média das entradas com chuva
# 2. A média das entradas sem chuva
# 
# 
# 

# In[ ]:


import numpy as np

import pandas

def means(turnstile_weather):
    noRain = turnstile_weather[turnstile_weather['rain'] == 0]['ENTRIESn_hourly']
    without_rain_mean = noRain.mean()
    
    Rain = turnstile_weather[turnstile_weather['rain'] == 1]['ENTRIESn_hourly']
    with_rain_mean = Rain.mean()
    
    return with_rain_mean, without_rain_mean # leave this line for the grader

means(data_weather)


# Responda as perguntas abaixo de acordo com a saida das suas funções:
# 
# 1. Qual a média das entradas com chuva?
# 2. Qual a média das entradas sem chuva?
# 

# ** Resposta **:
#  
# Para dias chuvosos a média de entradas é 1105, já para dias que não choveu a média 1090.

# ## Exercicio 3 - Map Reduce
# 
# ### *Exercicio 3.1*
# 
# A entrada para esse exercício e o mesmo arquivo da seção anterior (Exercicio 2). Você pode baixar o arquivo neste link:
# 
#  https://s3.amazonaws.com/content.udacity-data.com/courses/ud359/turnstile_data_master_with_weather.csv
# 
# Varmos criar um mapeador agora. Para cada linha de entrada, a saída do mapeador deve IMPRIMIR (não retornar) a UNIT como uma chave e o número de ENTRIESn_hourly como o valor. Separe a chave e o valor por uma guia. Por exemplo: 'R002 \ t105105.0'
# 
# Exporte seu mapeador em um arquivo chamado mapper_result.txt e envie esse arquivo juntamente com a sua submissão. O código para exportar seu mapeador já está escrito no código abaixo.
# 
# 
# 

# In[ ]:


import sys

def mapper():
    
    for line in sys.stdin:
        data = line.strip().split(",")

        if len(data) >= 7:
            print(data[1]+"\t"+data[6])

sys.stdin = open('turnstile_data_master_with_weather.csv')
sys.stdout = open('mapper_result.txt', 'w')


# In[ ]:


mapper()


# ### *Exercicio 3.2*
# 
# Agora crie o redutor. Dado o resultado do mapeador do exercicio anterior, o redutor deve imprimir(Não retornar) uma linha por UNIT, juntamente com o número total de ENTRIESn_hourly.Ao longo de maio (que é a duração dos nossos dados), separados por uma guia. Um exemplo de linha de saída do redutor pode ser assim: 'R001 \ t500625.0'
# 
# Você pode assumir que a entrada para o redutor está ordenada de tal forma que todas as linhas correspondentes a uma unidade particular são agrupados. No entanto a saida do redutor terá repetição pois existem lojas que aparecem em locais diferentes dos arquivos.
# 
# Exporte seu redutor em um arquivo chamado reducer_result.txt e envie esse arquivo juntamente com a sua submissão.

# In[ ]:


def reducer():
    total_Entries = 0
    oldKey = None

    for line in sys.stdin:
        mapped = line.strip().split("\t")
        if len(mapped) != 2:
            continue
        
        thisKey, thisEntries = mapped
        
        try:
            thisEntryFloat = float(thisEntries)
            if oldKey and oldKey != thisKey:
                print(f"{oldKey}\t{total_Entries}")
                oldKey = thisKey
                total_Entries = 0
            
            oldKey = thisKey
            total_Entries += thisEntryFloat
        except ValueError:
            pass
            
sys.stdin = open('mapper_result.txt')
sys.stdout = open('reducer_result.txt', 'w')


# In[ ]:


reducer()

