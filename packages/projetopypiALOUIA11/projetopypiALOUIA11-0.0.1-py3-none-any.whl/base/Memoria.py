def salvar_em_arquivo(palavras):

    palavras = ' '.join(palavras)

    with open('base_palavras.txt', 'a') as f:

        f.write(palavras)