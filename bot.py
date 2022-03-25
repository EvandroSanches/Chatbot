import os
import time
import re
import wikipedia
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
from selenium import webdriver
from random import randint



class wppbot:

    dir_path = os.getcwd()

    def __init__(self, nome_bot):
        print(self.dir_path)
        self.bot = ChatBot(nome_bot)
        self.trainer = ListTrainer(self.bot)
        self.chrome = self.dir_path+'\chromedriver.exe'

        self.options = webdriver.ChromeOptions()
        self.options.add_argument("user-data-dir="+self.dir_path+"\profile\wpp")
        self.driver = webdriver.Chrome(self.chrome, chrome_options=self.options)

    def inicia(self,nome_contato):

        self.driver.get('https://web.whatsapp.com/')
        self.driver.implicitly_wait(20)

        self.caixa_de_pesquisa = self.driver.find_element_by_class_name('_3FRCZ')


        self.caixa_de_pesquisa.send_keys(nome_contato)
        time.sleep(2)
        print(nome_contato)
        self.contato = self.driver.find_element_by_xpath('//span[@title = "{}"]'.format(nome_contato))
        self.contato.click()
        time.sleep(2)


    def saudacao(self,frase):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name('_3uMse')

        self.caixa_de_mensagem.send_keys(self.bot.name+': '+frase)
        time.sleep(1)
        self.botao_enviar = self.driver.find_element_by_class_name('_1U1xa')
        self.botao_enviar.click()
        time.sleep(1)


    def responder(self,frase):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name('_3uMse')

        #resposta = (self.bot.get_response(frase))
        #if float(resposta.confidence) > 0.5:
        #resposta = str(resposta)
        self.caixa_de_mensagem.send_keys(self.bot.name+': '+frase)
        time.sleep(1)
        self.botao_enviar = self.driver.find_element_by_class_name('_1U1xa')
        self.botao_enviar.click()
        time.sleep(1)

    def bot_response(self,resposta):


        if float(resposta.confidence) > 0.5:
            resposta = str(resposta)
            self.responder(resposta)
            return True
        else:
            return False
            #self.responder('Desculpe ainda não sei como responder')




    def escuta(self):
        post = self.driver.find_elements_by_class_name('_2hqOq')
        ultimo = len(post) - 1
        texto = post[ultimo].find_element_by_css_selector('span.selectable-text').text

        return texto

    def aprender(self,ultimo_texto,frase_inicial,frase_final,frase):
        self.responder(frase_inicial)

        while True:

            texto = self.escuta()
            texto = texto.replace(self.bot.name + ': ', '')

            if texto != ultimo_texto:
                if ultimo_texto == frase_inicial:
                    self.responder(texto + ', esta correto?')
                    resposta = texto
                    ultimo_texto = texto
                else:
                    if texto == 'sim' or texto == 'Sim':

                        alimentacao = open('treino/Conversas.txt', 'a')
                        alimentacao.write('\n' + frase + '\t' + resposta)
                        alimentacao.close()

                        treino = [frase,resposta]
                        self.trainer.train(treino)
                        self.responder(frase_final)

                        ultimo_texto = self.escuta()
                        ultimo_texto = ultimo_texto.replace(self.bot.name + ': ', '')
                        return ultimo_texto

                    elif texto == 'não' or texto == 'Não':
                        ultimo_texto = self.escuta()
                        ultimo_texto = ultimo_texto.replace(self.bot.name + ': ', '')
                        return ultimo_texto



    def treina(self):
        lines = open('treino/Conversas.txt','r').readlines()

        for line in lines:
            line = line.replace('\n', '')
            parts = line.split('\t')
            self.trainer.train(parts)


    def resposta_treino (self):
        resposta = randint(0,7)
        lista = ['Desculpe ainda não sei como responder, como devo responder?','Ainda não conheço uma resposta, como devo responder?',
                 'Desconheço este assunto, o que devo dizer?', 'Não sei como responder, como devo responder?', 'Ainda não aprendi uma resposta para isso, o que devo dizer?',
                 'Ainda não sei isto, o que devo dizer?', 'O que devo responder?', 'O que devo dizer?']
        return lista[resposta]

    def wiki_response (self,ultimo_texto):
        Wiki_keywords = ['o que é ', 'quem é ', 'quem foi ', 'qual é a definição ', 'defina ', 'quem foram ',
                         'quem são ', 'quais são', 'quais foram', 'qual é', 'o que são']

        for key in Wiki_keywords:
            if ultimo_texto.startswith(key):

                wikipedia.set_lang('pt')
                search = None

                search = wikipedia.search(ultimo_texto)
                ultimo_texto = wikipedia.summary(search[0], sentences=1)
                self.responder(ultimo_texto)


        return ultimo_texto


    def calcular(self,ultimo_texto):

        formula = ultimo_texto
        formula = formula.replace('quanto é','')
        sair = False

        if ultimo_texto.find('+') or ultimo_texto.find('-') or ultimo_texto.find('*') or ultimo_texto.find('/') or ultimo_texto.find('^') or ultimo_texto.find('%'):

           if formula.count('*') > 0 and not sair:
               calculo = formula.split('*')

               if calculo[0].isdigit() and calculo[1].isdigit():
                   ultimo_texto = str((int(calculo[0])) * (int(calculo[1])))
                   self.responder(ultimo_texto)
               else:
                   ultimo_texto = 'Desculpe, sou capaz de calcular apenas matemática básica'
                   self.responder(ultimo_texto)
                   sair = True


           if formula.count('+') > 0 and not sair:
               calculo = formula.split('+')
               if calculo[0].isdigit() and calculo[1].isdigit():
                   ultimo_texto = str((int(calculo[0])) + (int(calculo[1])))
                   self.responder(ultimo_texto)
               else:
                   ultimo_texto = 'Desculpe, sou capaz de calcular apenas matemática básica'
                   self.responder(ultimo_texto)
                   sair = True

           if formula.count('-') > 0 and not sair:
               calculo = formula.split('-')
               if calculo[0].isdigit() and calculo[1].isdigit():
                   ultimo_texto = str((int(calculo[0])) - (int(calculo[1])))
                   self.responder(ultimo_texto)
               else:
                   ultimo_texto = 'Desculpe, sou capaz de calcular apenas matemática básica'
                   self.responder(ultimo_texto)
                   sair = True

           if formula.count('/') > 0 and not sair:
               calculo = formula.split('/')
               if calculo[0].isdigit() and calculo[1].isdigit():
                   ultimo_texto = str((int(calculo[0])) / (int(calculo[1])))
                   self.responder(ultimo_texto)
               else:
                   ultimo_texto = 'Desculpe, sou capaz de calcular apenas matemática básica'
                   self.responder(ultimo_texto)
                   sair = True

           if formula.count('^') > 0 and not sair:
               calculo = formula.split('^')
               if calculo[0].isdigit() and calculo[1].isdigit():
                   ultimo_texto = str((int(calculo[0])) ** (int(calculo[1])))
                   self.responder(ultimo_texto)
               else:
                   ultimo_texto = 'Desculpe, sou capaz de calcular apenas matemática básica'
                   self.responder(ultimo_texto)
                   sair = True

           if formula.count('%') > 0 and not sair:
               calculo = formula.split('%')
               if calculo[0].isdigit() and calculo[1].isdigit():
                   ultimo_texto = str((int(calculo[0])) % (int(calculo[1])))
                   self.responder(ultimo_texto)
               else:
                   ultimo_texto = 'Desculpe, sou capaz de calcular apenas matemática básica'
                   self.responder(ultimo_texto)
                   sair = True

        return ultimo_texto