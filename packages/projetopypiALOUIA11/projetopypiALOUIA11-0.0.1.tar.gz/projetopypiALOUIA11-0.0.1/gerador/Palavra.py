import random

def gerar_silaba():

    consoantes = 'bcdfghjklmnpqrstvwxyz'

    vogais = 'aeiou'

    return random.choice(consoantes) + random.choice(vogais)

def gerar_palavra_dissilaba():

    return gerar_silaba() + gerar_silaba()