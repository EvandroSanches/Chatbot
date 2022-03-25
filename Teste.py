def responder(self, frase):
    self.caixa_de_mensagem = self.driver.find_element_by_class_name('_3uMse')
    self.caixa_de_mensagem.send_keys(self.bot.name + ': ' + frase)
    time.sleep(1)
    self.botao_enviar = self.driver.find_element_by_class_name('_1U1xa')
    self.botao_enviar.click()
    time.sleep(1)