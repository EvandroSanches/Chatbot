import re
from bot import wppbot

lucy = wppbot('Lucy')
#lucy.treina()
lucy.inicia('Eduardo')

lucy.saudacao('Oi meu nome é Lucy!, isso é um teste de chatbot')
ultimo_texto = 'Oi meu nome é Lucy!, isso é um teste de chatbot'

texto = ''



while True:

    texto = lucy.escuta()
    texto = texto.replace(lucy.bot.name+': ','')

    if texto != ultimo_texto:
        texto_tratado = texto.lower()

        ultimo_texto = lucy.wiki_response(texto_tratado)

        if ultimo_texto == texto_tratado:

            ultimo_texto = lucy.calcular(texto_tratado)

            if ultimo_texto == texto_tratado:

                resposta = (lucy.bot.get_response(texto_tratado))
                bot_response = lucy.bot_response(resposta)

                if bot_response:
                    ultimo_texto = str(resposta)
                else:
                    ultimo_texto = lucy.resposta_treino()
                if ultimo_texto == 'aprender' or not bot_response:
                    ultimo_texto = lucy.aprender(ultimo_texto,ultimo_texto,'Obrigada por me ensinar',
                                  texto)
