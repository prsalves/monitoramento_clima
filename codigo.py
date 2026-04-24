import requests #importa a biblioteca requests para requisições HTTP
import json #importa a biblioteca json para manusear arquivos no formato json
import time #importa a biblioteca time para fazer pequenas pausas
from datetime import datetime
import os

def obter_cidade(cidade): #define a função que vai obter a cidade
  while True:
    try:
      chave_API = "b7a59ad37bdad8a64d9a14bf566e117e"
      url = 'https://api.openweathermap.org/data/2.5/forecast' #link para obter a cidade
      params = {
          'q': cidade,
          'appid': chave_API,
          'units': 'metric',
          'lang' : 'pt_br' 
      } # parametros necessários para obter os dados (parametros da propria API, encontrados na documentação)
      response = requests.get(url, params=params) #utiliza a biblioteca requests para pegar os dados, passando o url e os parâmetros e armazenando na variável response
      dados = response.json() #armazenando os dados no formato json
      #tratamento de casos de erros:
      if dados['cod'] == '404':
        return cidade
      elif dados['cod'] == '401':
        print('Chave de API inválida')
      elif dados['cod'] == '400':
        print('Parâmetros inválidos')
      elif dados['cod'] == '403':
        print('Acesso negado')
      else :
        return dados
    except requests.exceptions.ConnectionError:
      return 'SI'
def formatar_dados(dados): #usado somente pelo desenvolvedor para analisar os dados
  json_formatado = json.dumps(dados, indent=4, ensure_ascii=False) #formata os dados, para melhor visualização
  print(json_formatado) #imprime os dados para análise


def obter_estado(dados): #função para obter o estado
  lat = dados['city']['coord']['lat'] #pega a latitude e longitute dentro dos dados
  lon = dados['city']['coord']['lon']
  chave_API = "b7a59ad37bdad8a64d9a14bf566e117e"
  url = f'http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={chave_API}'#link do software de geolocalização, da própria API
  params = {
      'lat' : lat,
      'lon' : lon,
      'limit' : 1,
      'appid' : chave_API
  } #parametros necessários, requisitados na documentaçãoda própria API
  response = requests.get(url, params=params) #armazena os dados na variavel response
  data = response.json() #transforma os dados em arquivo json
  estado = data[0].get('state') #pega o estado dentro do arquivo
  if not estado: #se não tiver estado, como é o caso de algumas cidades, imprimir 'não encontrado'
    estado = 'Não encontrado'
  return estado #retornar o estado
def exibir_dados(dados,estado): #função para exibir os dados
  total = []
  total.append(f"Cidade: {dados['city']['name']} - {estado} - {dados['city']['country']}") #imprime o nome da cidade, do estado e do país
  total.append('') #espaço vazio, apenas por estética
  total.append('-'*90) #cria uma espécie de separação entre os textos, apenas por fins estéticos
  total.append(f"{'Data':<20} {'Temp(°C)':>15} {'Descrição':>15} {'Sensação(°C)':>15} {'Humidade(%)':>17}") #imprime o cabeçalho da tabela, indicando as informações que serão listadas
  total.append('-'*90)
  contagem = 0 # contagem para limitar a quantidade de resultados na busca
  for data in dados['list']: #loop que pega os dados do arquivo 'dados', e armazeba cada um em uma variável
    date_str = (f"{data['dt_txt']}")
    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    date_formatada = date.strftime("%d/%m/%Y %H:%M:%S")
    temp = (f"{data['main']['temp']:.0f}°C")
    descricao = (f"{data['weather'][0]['description']}")
    sensacao = (f"{data['main']['feels_like']:.0f} °C")
    humidade = (f"{data['main']['humidity']}%")
    total.append(f"{date_formatada:<20} {temp:>10} {descricao:>20} {sensacao:>15} {humidade:>12}") #imprime as informações
    contagem +=1 #aumenta em 1 a contagem
    if contagem == 17: #limita a quantidade de resultados para 17 
      return total #encerra o programa
ultimos = []
while True:
  with open("cidades.txt", "r", encoding="utf-8") as f:
    lista = f.readlines()
  lista = [linha.strip() for linha in lista]
  for c in lista:
    dados_cidade = obter_cidade(c) # armazena os dados da cidade dentro de 'dados_cidade', chamando a função 'obter_cidade'
    if dados_cidade == c:
      print(f'Cidade {c} não encontrada')
    elif dados_cidade == 'SI':
      print('Sem conexão com a internet')
      if not ultimos:
        print('Não foi possível obter a última atualização')
        break
      else:
        for u in ultimos:
          print()
          print('Última aualização:',agora)
          for n in u:
            print(n)
      break
    else:
      agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
      print('Última aualização:',agora)
      estado = obter_estado(dados_cidade) #pega o estado de acordo com os dados da cidade
      dados = exibir_dados(dados_cidade,estado) #exibe os dados, de acordo com a cidade e o estado
      for d in dados:
        print(d)
      print()
      ultimos.append(dados)
      if len(ultimos) > len(lista):
        ultimos = []
  time.sleep(60)
  os.system('cls')