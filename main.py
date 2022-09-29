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

#comandinhos pra startar o chrome

options = Options()
options.add_argument("start-maximized")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--headless")

#  Telegram

token = cred.token

def enviar_mensagem(chat_id, text, disable_notification=False):
    data = requests.get(
        f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}&disable_notifications={disable_notification}')
    #print(data.json())

#  Fim Telegram


bot = 2

while bot:

    fuel = 'null'
    co2 = 'null'

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    #  Logando
    driver.get('https://www.airlinemanager.com/')
    print('entrou no site')
    menu = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/div[1]/div/button[2]')
    menu.click()
    time.sleep(15)
    print('clicou no login')
    email = driver.find_element(By.XPATH, '//*[@id="lEmail"]')
    email.send_keys(cred.cred1)
    time.sleep(8)
    print('colocou o email')
    senha = driver.find_element(By.XPATH, '//*[@id="lPass"]')
    senha.send_keys(cred.cred2)
    time.sleep(8)
    print('colocou a senha')
    login = driver.find_element(By.XPATH, '//*[@id="btnLogin"]')
    login.click()
    print('fez o login')
    time.sleep(16)

    #  Fuel

    try:
        botaofu = driver.find_element(By.XPATH, '/html/body/div[9]/div/div[4]/div[3]/div')
        time.sleep(15)
        print('achou o botao de combustivel')
        botaofu.click()
        time.sleep(15)

        fu = driver.find_element(By.XPATH, '//*[@id="fuelMain"]/div/div[1]/span[2]/b').text
        fuele = fu.replace("$ ", "")
        fuelee = fuele.replace(",", "")
        fuel = int(fuelee)
        logging.warning('Preço do combustível obtido com sucesso!')

    except:
        logging.warning('Erro ao obter preço do combustível')

       #  CO2

    try:
        time.sleep(12)
        botaoco = driver.find_element(By.XPATH, '//*[@id="popBtn2"]')
        botaoco.click()
        time.sleep(15)
        co = driver.find_element(By.XPATH, '//*[@id="co2Main"]/div/div[2]/span[2]/b').text
        co2e = co.replace("$ ", "")
        co2ee = co2e.replace(",", "")
        co2 = int(co2ee)
        logging.warning('Preço do CO2 obtido com sucesso!')
        driver.quit()

    except:
        logging.warning('Erro ao obter preço do CO2')




    #  Hora dos avisos


    if fuel < 1000 or co2 < 150:

        # Telegram

        try:
            texto = (f'Preço do combustível: $ {fuel}, e do CO2: $ {co2}.')
            enviar_mensagem(chat_id='-853345222', text=texto)
            logging.warning('Informado no telegram com sucesso')

        except:
            logging.warning('Erro ao postar no telegram')

        #  Wordpress

        try:
            TITULO = 'Atualização de preço'
            TEXTO = (f'Preço do combustível: $ {fuel}, e do CO2: $ {co2}.')

            your_blog = Client('https://www.mafiabrasil.com/xmlrpc.php', cred.cred3, cred.cred4)

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

    elif fuel == 'null' or co2 == 'null':
        driver.quit()

    else:
        logging.warning('valores ainda estão muito altos')


    #  Refresh do bot
    logging.warning('Bot fará uma nova busca em 10 segundos')
    time.sleep(10)

