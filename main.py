import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
import requests
import cred
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc import WordPressPost

#comandos para startar o chrome, evitar erros de scraping

options = Options()
options.add_argument("start-maximized")
options.add_argument("window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--headless")

#  Telegram

token = cred.token

# Função de envio de mensagem

def enviar_mensagem(chat_id, text, disable_notification=False):
    data = requests.get(
        f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}&disable_notifications={disable_notification}')
    #print(data.json())


bot = 2

# Inicio do Loop

while bot:

    fuel = 'null'
    co2 = 'null'
    
    # Abrir o Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    #  Logando no site, e clicando nos botões. Sleep para garantir que a pagina vai carregar a tempo
    driver.get('https://www.airlinemanager.com/')
    menu = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/div[1]/div/button[2]')
    menu.click()
    time.sleep(15)
    email = driver.find_element(By.XPATH, '//*[@id="lEmail"]')
    email.send_keys(cred.cred1)
    time.sleep(8)
    senha = driver.find_element(By.XPATH, '//*[@id="lPass"]')
    senha.send_keys(cred.cred2)
    time.sleep(8)
    login = driver.find_element(By.XPATH, '//*[@id="btnLogin"]')
    login.click()
    time.sleep(16)

    #  Depois de logar, inicio da pesquisa de Fuel

    try:
        botaofu = driver.find_element(By.XPATH, '/html/body/div[9]/div/div[4]/div[3]/div')
        time.sleep(15)
        botaofu.click()
        time.sleep(15)

        fu = driver.find_element(By.XPATH, '//*[@id="fuelMain"]/div/div[1]/span[2]/b').text
        # Tratando dados
        fuele = fu.replace("$ ", "")
        fuelee = fuele.replace(",", "")
        fuel = int(fuelee)
        # Aviso do log
        logging.warning('Preço do combustível obtido com sucesso!')

    except:
        logging.warning('Erro ao obter preço do combustível')

       #  Inicio da pesquisa de CO2

    try:
        time.sleep(12)
        botaoco = driver.find_element(By.XPATH, '//*[@id="popBtn2"]')
        botaoco.click()
        time.sleep(15)
        co = driver.find_element(By.XPATH, '//*[@id="co2Main"]/div/div[2]/span[2]/b').text
        # Tratando dados
        co2e = co.replace("$ ", "")
        co2ee = co2e.replace(",", "")
        co2 = int(co2ee)
        # Aviso do log
        logging.warning('Preço do CO2 obtido com sucesso!')
        driver.quit()

    except:
        logging.warning('Erro ao obter preço do CO2')




    #  Hora dos avisos: Telegram + Wordpress


    if fuel < 1000 or co2 < 150:

        # Postar no Telegram

        try:
            texto = (f'Preço do combustível: $ {fuel}, e do CO2: $ {co2}.')
            enviar_mensagem(chat_id='-853345222', text=texto)
            logging.warning('Informado no telegram com sucesso')

        except:
            logging.warning('Erro ao postar no telegram')

        #  Postar no Wordpress

        try:
            TITULO = 'Atualização de preço'
            TEXTO = (f'Preço do combustível: $ {fuel}, e do CO2: $ {co2}.')

            your_blog = Client('Site do Cliente', cred.cred3, cred.cred4)

            myposts = your_blog.call(posts.GetPosts())

            post = WordPressPost()
            post.title = TITULO
            post.slug = ''
            post.content = TEXTO
            post.id = your_blog.call(posts.NewPost(post))
            post.post_status = 'publish'
            your_blog.call(posts.EditPost(post.id, post))
            logging.warning('Postado no Wordpress com sucesso!')

        except:
            logging.warning('Erro ao postar no wordpress')
    
    # Tratando erros
    elif fuel == 'null' or co2 == 'null':
        driver.quit()
    
    # Aguardando próximo atualização
    else:
        logging.warning('valores ainda estão muito altos')


    #  Refresh do bot
    logging.warning('Bot fará uma nova busca em 30 minutos')
    time.sleep(1800)

