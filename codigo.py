import requests
import json
import time

def obter_cidade():
  while True:
    cidade = input('Digite uma cidade:')
    chave_API = "xxxxxx"
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    params = {
        'q': cidade,
        'appid': chave_API,
        'units': 'metric',
        'lang' : 'pt_br' 
    }
    response = requests.get(url, params=params)
    dados = response.json()
    if dados['cod'] == '404':
      print('Cidade não encontrada')
      print()
    elif dados['cod'] == '401':
      print('Chave de API inválida')
    elif dados['cod'] == '400':
      print('Parâmetros inválidos')
    elif dados['cod'] == '403':
      print('Acesso negado')
    else :
      print('Cidade encontrada')
      print('Buscando...')
      print()
      time.sleep(3)
      return dados 
def formatar_dados(dados):
  #usado somente pelo desenvolvedor para analisar os dados
  json_formatado = json.dumps(dados, indent=4, ensure_ascii=False)
  print(json_formatado)


def obter_estado(dados):
  lat = dados['city']['coord']['lat']
  lon = dados['city']['coord']['lon']
  chave_API = "xxxxxx"
  url = f'http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={chave_API}'
  params = {
      'lat' : lat,
      'lon' : lon,
      'limit' : 1,
      'appid' : chave_API
  }
  response = requests.get(url, params=params)
  data = response.json()
  estado = data[0].get('state')
  if not estado:
    estado = 'Não encontrado'
  return estado
def exibir_dados(dados,estado):
  print(f"Cidade: {dados['city']['name']} - {estado} - {dados['city']['country']}")
  print()
  print('-'*90)
  print(f"{'Data':<20} {'Temp(°C)':>15} {'Descrição':>15} {'Sensação(°C)':>15} {'Humidade(%)':>17}")
  print('-'*90)
  contagem = 0
  for data in dados['list']:
    date = (f"{data['dt_txt']}")
    temp = (f"{data['main']['temp']:.0f}°C")
    descricao = (f"{data['weather'][0]['description']}")
    sensacao = (f"{data['main']['feels_like']:.0f} °C")
    humidade = (f"{data['main']['humidity']}%")
    print()
    time.sleep(0.2)
    print(f"{date:<20} {temp:>10} {descricao:>20} {sensacao:>15} {humidade:>12}")
    contagem +=1
    if contagem == 17:
      break

dados_cidade = obter_cidade()
estado = obter_estado(dados_cidade)
exibir_dados(dados_cidade,estado)