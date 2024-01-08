from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import banco
from time import sleep
from datetime import datetime
from selenium.webdriver.common.by import By
from ligas_mercados import *
from querys import *
import shutil

banco.deletar_tabela('EventoOddArena')

banco.inserir_db(CREATE_TABLE_EVENTO_ODD_ARENA)
#banco.inserir_db(create_table_history)

try:
    service = FirefoxService(executable_path=GeckoDriverManager().install())
except:
    try:
        shutil.rmtree('/home/suportelinux/.wdm/drivers/')
        print('Removido com suceso')
    except Exception as err:
        print(err)
#service = FirefoxService(executable_path=GeckoDriverManager().install())
#service = FirefoxService(executable_path=GeckoDriverManager().install())
url = r'https://www.arenaesportiva.live/esportes/1'

option = Options()
option.add_argument('-headless')
option.headless = True
driver = webdriver.Firefox(service=service,options=option)

driver.get(url)

sleep(10)
evento = []
jogos_liga = {}
jogos_hora = {}

def eliminatorias(liga_eliminatoria):

    copa_eliminatoria = [chave for key, chave in jogos_liga.items() if liga_eliminatoria in key]
    lista_copa_eliminatoria = []
    for copa in copa_eliminatoria:
        for a in copa:
            lista_copa_eliminatoria.append(a)

    if len(lista_copa_eliminatoria) > 0:
       return True, lista_copa_eliminatoria

    return False, 0

def limpar_sujeiras_webscrapping(lista_liga, liga_pais):
    for liga,pais in zip(lista_liga,liga_pais):
        nome_liga = str(liga.get_text())
        if '' == nome_liga:
            lista_liga.remove(liga)
            liga_pais.remove(pais)
    return lista_liga, liga_pais

site2 = driver.find_elements(By.CLASS_NAME, 'home')

for i in site2:
    i.find_element(By.XPATH,'/html/body/div/div[3]/div/div[2]/button[1]').click()
    codigo = i.get_attribute('outerHTML')
    soup = BeautifulSoup(codigo, 'html.parser')
    jogo = soup.find_all(attrs={'class':"shadow-on-hover"})
    liga2 = soup.find_all(attrs={'class':'section-title__info'})
    ligas3 = [str(i.get_text()) for i in liga2]
    
    try:
        while 'Série A' not in ligas3:
            i.find_element(By.CLASS_NAME,'button-flat-5__title').click()
            codigo = i.get_attribute('outerHTML')
            soup = BeautifulSoup(codigo, 'html.parser')
            jogo = soup.find_all(attrs={'class':"shadow-on-hover"})
            liga2 = soup.find_all(attrs={'class':'section-title__info'})
            ligas3 = [str(i.get_text()) for i in liga2]
    except Exception as err:
        print(err)
    pais = soup.find_all(attrs={'class':'section-title'})
    liga2 = soup.find_all(attrs={'class':'section-title__info'})
   
    liga2 , pais = limpar_sujeiras_webscrapping(liga2,pais)

    for i,a,c in zip(liga2,jogo,pais):
        nome_liga = str(i.get_text())
        nome_pais = str(c.get_text())
        hora_dia_evento = a.find_all(attrs={'class':'caption-2'})
        urls = a.find_all('a')
        evento=[]
        for a,b in enumerate(urls):
            if b.get('href') not in evento:
                evento.append(b.get('href'))
        
        if 'ÁustriaBundesliga' == nome_pais:
            continue
        if 'UcrâniaPremier League' == nome_pais:
            continue
        if 'Bósnia e HerzegovinaPremier League' == nome_pais:
            continue
        if 'EtiópiaPremier League' == nome_pais:
            continue
        else:
            jogos_liga[nome_liga] = evento

        for a,d in zip(evento,hora_dia_evento):
            jogos_hora[a]= d.get_text()
        
site = driver.find_elements(By.CLASS_NAME, 'eventos-list')

cpmundo = False
#cpmundo, list_copa_do_mundo= eliminatorias("Copa do Mundo")
cpliga_campeoes, list_liga_campeoes= eliminatorias("Liga dos Campeões UEFA - ")
cplibertadores, list_libertadores= eliminatorias("Copa Libertadores - ")
cpliga_conferencia_europa, list_conferencia_europa = eliminatorias("Liga Conferência da Europa - ")
cp_feminino, list_feminino = eliminatorias("Campeonato Mundial - Feminino - ")


if cpmundo:
    if 'Copa do Mundo' in jogos_liga:
        jogos_liga['Copa do Mundo'] = list_copa_do_mundo
    else:
        for jogos in jogos_liga['Copa do Mundo']:
            list_copa_do_mundo.append(jogos)
        jogos_liga['Copa do Mundo'] = list_copa_do_mundo

if cpliga_campeoes:
    if 'Liga dos Campeões UEFA' not in jogos_liga:
        jogos_liga['Liga dos Campeões UEFA'] = list_liga_campeoes
    else:
        for jogos in jogos_liga['Liga dos Campeões UEFA']:
            list_liga_campeoes.append(jogos)
        jogos_liga['Liga dos Campeões UEFA'] = list_liga_campeoes

if cpliga_conferencia_europa:        
    if 'Liga Conferência da Europa' not in jogos_liga:
        jogos_liga['Liga Conferência da Europa'] = list_conferencia_europa
    else:
        for jogos in jogos_liga['Liga Conferência da Europa']:
            list_conferencia_europa.append(jogos)
        jogos_liga['Liga Conferência da Europa'] = list_conferencia_europa

if cp_feminino:
    if 'Campeonato Mundial - Feminino' not in jogos_liga:
        jogos_liga['Campeonato Mundial - Feminino'] = list_feminino
    else:
        for jogos in jogos_liga['Campeonato Mundial - Feminino']:
            list_feminino.append(jogos)

if cplibertadores:
    if 'Copa Libertadores' not in jogos_liga:
        jogos_liga['Copa Libertadores'] = list_libertadores
    else:
        for jogos in jogos_liga['Copa Libertadores']:
            list_libertadores.append(jogos)
        

for liga,jogo in jogos_liga.items():
    if liga in LIGA_ID:
        for id in jogo:  
            eventoid_rename = id.replace('/subevento/prematch/evento/','')
            nova_url = r'https://www.arenaesportiva.live' + id
            driver.get(nova_url)
            sleep(10)
            jogos_hora[id] = jogos_hora[id].replace(' ', '')
            convert_data = jogos_hora[id].split('·')
            troca_mes = convert_data[0].split('/')
            jogos_hora[id] = f'{troca_mes[1]}/{troca_mes[0]} · {convert_data[1]}'
            site = driver.find_elements(By.CLASS_NAME, 'subeventos-dados')
            for i in site:
                codigo_id = i.get_attribute('outerHTML')
                soupid = BeautifulSoup(codigo_id, 'html.parser')
                nome_evento = soupid.find('p')
                time_evento = nome_evento.get_text()
                if "Borussia M'gladbach" in time_evento:
                    time_evento = time_evento.replace("Borussia M'gladbach","Borussia M gladbach")
                print(time_evento)
                mercado =soupid.find_all(attrs={'class':'button-odd-default__title'})
                bets = soupid.find_all(attrs={'class':'button-odd-default__info'})
                subeventos = soupid.find_all(attrs={'class':'subeventos-dados--item'})                    
                for a in subeventos:
                    nome_mercado = a.find_all('h2')
                    for nome in nome_mercado:
                        mercado_nome = nome.get_text()
                    if mercado_nome in MERCADOS_PUXADOS:
                        mercado_teste = a.find_all(attrs={'class':'button-odd-default__title'})
                        bets_teste = a.find_all(attrs={'class':'button-odd-default__info'})
                        testandoidmercado = CODIGOS_MERCADOS[mercado_nome]
                        placar_nameodd=[]
                        for i, c in enumerate(mercado_teste):
                            teste = str(c).replace('<span class="button-odd-default__title truncate subhead dark-disabled">','')
                            teste2 = teste.replace('</span>','')
                            if CODIGOS_MERCADOS[mercado_nome] == 1019:
                                if teste2 not in placar_nameodd:
                                    placar_nameodd.append(teste2)
                                else:
                                    teste2 = teste2[::-1]
                            
                            bet_1 = str(bets_teste[i]).replace('<span class="button-odd-default__info subhead dark-primary">','')
                            bet_2 = bet_1.replace('</span>','')
                            sql = """
                                    INSERT into EventoOddArena
                                    (eventoid, evento, mercadoid, nomemercado, nomeodd, cotacao,
                                    inicioevento, torneioid, torneio, dataatualizacao)
                                    values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');""" %(eventoid_rename, time_evento,
                                    CODIGOS_MERCADOS[mercado_nome],NOMES_MERCADOS[mercado_nome],teste2,bet_2,jogos_hora[id],
                                    LIGA_ID[liga],NOMES_LIGAS[liga],datetime.now())
                            sql2 = """
                                    INSERT into EventoOddArenaHistory
                                    (eventoid, evento, mercadoid, nomemercado, nomeodd, cotacao,
                                    inicioevento, torneioid, torneio, dataatualizacao)
                                    values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');""" %(eventoid_rename, time_evento,
                                    CODIGOS_MERCADOS[mercado_nome],NOMES_MERCADOS[mercado_nome],teste2,bet_2,jogos_hora[id],
                                    LIGA_ID[liga],NOMES_LIGAS[liga],datetime.now())
                            banco.inserir_db(sql)
                            #banco.inserir_db(sql2)
                            

driver.quit()



"""
for a,d in NOMES_LIGAS:
    print(a,d,'\n')
#print('#########################################')
#print(jogos_liga)

#print(jogos_liga['Liga dos Campeões UEFA'])

copadomundo = [chave for key, chave in jogos_liga.items() if "Copa do Mundo" in key]

list_cp =[]

for cpmundo in copadomundo:
    for a in cpmundo:
        list_cp.append(a)
if len(list_cp) > 0:        
    jogos_liga['Copa do Mundo'] = list_cp

copalibertadores_grupos = [chave for key, chave in jogos_liga.items() if "Copa Libertadores - " in key]

list_copaliberadores =[]

for cplibertadores in copalibertadores_grupos:
    for a in cplibertadores:
        list_copaliberadores.append(a)

if len(list_copaliberadores) > 0:
    jogos_liga['Copa Libertadores'] = list_copaliberadores

#print(list_copaliberadores)
"""