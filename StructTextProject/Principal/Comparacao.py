'''WordEmbeddings'''
from gensim.models import KeyedVectors
from gensim.models import Word2Vec
import sys
from IPython.display import display, HTML
from IPython.display import Image
from jinja2 import Template
import mysql.connector as mysql
import math
import networkx as nx
import matplotlib.pyplot as plt



from Model import Classes

class Comparacao:
    # skip_gram_model = KeyedVectors.load_word2vec_format('skip_s50.txt',binary=False)
    # print("skip-gram pronto")

    def __init__(self,con,con2):
        self.con = con
        self.con2 = con2
        self.cbow_model =KeyedVectors.load_word2vec_format('cbow_s100.txt', binary=False)
        self.Comparacao = self._CompararConhecimentos(self.con,self.con2)

    def most_similar(positive, negative, model):
        table_list_template = """
            <table>
                <tr>
                    <th>Word</th>
                    <th>Similaridade</th>
                </tr>
                {% for item in items %}

                <TR>
                    <TD class="c1">{{item[0]}}</TD>
                    <TD class="c2">{{item[1]}}</TD>
                </TR>
                {% endfor %}
            </table>
            """
        nn = model.most_similar(positive=positive, negative=negative)
        tmpl = Template(table_list_template)
        output_html = tmpl.render(items=nn)
        return HTML(output_html)

    def ImprimirConhecimento(self):
        conhecimento = self.Comparacao

        for palavra in conhecimento:
            print("Palavra: ", palavra.verbo.text, "-", palavra.verbo.i, "-", palavra.verbo.pos_)

            print(f"{'Substantivo principal: '}{[substanP.text for substanP in palavra.substantivoPrincipal]}{[substanP.i for substanP in palavra.substantivoPrincipal]}")

            print(f"{'Substantivo posterior: '}{[substan.text for substan in palavra.substantivo]}")

            print(f"{'Demais verbos: '}{[verb.text for verb in palavra.verbos]}")

            print(f"{'Adjetivos: '}{[adj.text for adj in palavra.adjetivos]}")

            print(f"{'Demais relações: '}{[demaisR.text for demaisR in palavra.demaisRelacoes]}")

            print("--------------------------")
            print("\n")
            print("\n")



    def _ListarSinonimos(self,palavra, cursor):
        listaDeSinonimos = []

        query = "select * from WordNet_WordNetBr.synsets where unidade = '" + str(palavra) + "'"
        try:
            cursor.execute(query)
            records = cursor.fetchall()

            for record in records:
                query2 = "select * from WordNet_WordNetBr.synsets where id = " + record[2]

                try:
                    cursor.execute(query2)
                    records2 = cursor.fetchall()

                    for rec in records2:
                        listaDeSinonimos.append(rec)
                except:
                    print("An exception occurred")

        except Exception as e:
            print(e)

        return listaDeSinonimos


    def _CompararConhecimentos(self,con, con2):
        db = mysql.connect(
            host="localhost",
            user="root",
            password="Eunaosei1997",
            database="WordNet_WordNetBr",
            auth_plugin='mysql_native_password'
        )

        substantivoComCase1 = []
        substantivoComCase2 = []
        existeCase1 = 0
        existeCase2 = 0

        cursor = db.cursor()

        listaDeSinonimos = []

        jaAdicionouSubstantivo = 0

        listaDeVerbos = []

        listaDeVerbosNaoExistentes = []

        encontrou = 0

        continua = 0

        achouVerbo = 0

        for palavra in con:

            if palavra.palavra.pos_ == "V" or palavra.palavra.pos_ == "VAUX" or palavra.palavra.pos_ == "PCP":

                listaDeSinonimos = self._ListarSinonimos(palavra.palavra.lemma_, cursor)

                for palavraFraseTeste in con2:

                    if palavraFraseTeste.palavra.pos_ == "V" or palavraFraseTeste.palavra.pos_ == "VAUX" or palavraFraseTeste.palavra.pos_ == "PCP":

                        if palavraFraseTeste.palavra.lemma_.lower() != "":
                            if palavra.palavra.lemma_.lower() != "":
                                if palavraFraseTeste.palavra.pos_ != "PUNCT":
                                    if palavra.palavra.pos_ != "PUNCT":
                                        if palavraFraseTeste.palavra.pos_ != "NUM":
                                            if palavra.palavra.pos_ != "NUM":
                                                # Verifica se o verbo da frase principal e o verbo da frase que está sendo testada tem mais de 0.6 de semelhança

                                                if palavra.palavra.lemma_ != palavraFraseTeste.palavra.lemma_:

                                                    # Verifica se a palavra está na lista de sinônimos
                                                    for sinonimo in listaDeSinonimos:

                                                        if sinonimo[0].upper() == palavraFraseTeste.palavra.lemma_.upper():
                                                            continua = 1

                                                else:
                                                    continua = 1

                                                if continua == 0:
                                                    if palavra.palavra.lemma_.lower() in self.cbow_model.vocab and palavraFraseTeste.palavra.lemma_.lower() in self.cbow_model.vocab:
                                                        if self.cbow_model.similarity(palavra.palavra.lemma_.lower(),palavraFraseTeste.palavra.lemma_.lower()) > 0.6 and self.cbow_model.similarity(palavra.palavra.text.lower(),palavraFraseTeste.palavra.text.lower()) > 0.6:
                                                            continua = 1

                                                if continua == 1:
                                                    verbo = Classes.VerboIgual(palavraFraseTeste.palavra)

                                                    VerboPrincipalNegativo = 0
                                                    VerboTesteNegativo = 0

                                                    # Verifica se as polaridades dos verbos coicidem
                                                    for relacao in palavra.demaisRelacoes:
                                                        if relacao.pos_ == "ADV":
                                                            for tag in relacao.tag_:
                                                                if tag[0][0][0] == "Polarity" and tag[0][0][1] == "Neg":
                                                                    VerboPrincipalNegativo = 1

                                                    for relacao in palavraFraseTeste.demaisRelacoes:
                                                        if relacao.pos_ == "ADV":
                                                            for tag in relacao.tag_:
                                                                if tag[0][0][0] == "Polarity" and tag[0][0][1] == "Neg":
                                                                    VerboTesteNegativo = 1

                                                                    # Verificando se o verbo que está sendo analisado é positivo ou negativo
                                                    if VerboPrincipalNegativo == VerboTesteNegativo:

                                                        # VERIFICAR O SUBSTANTIVO PRINCIPAL
                                                        for substantivoPrincipal_FrasePrincipal in palavra.substantivoPrincipal:

                                                            '''Verificar se existe e qual é o case do substantivo da frase principal.'''

                                                            for pesquisando_substantivo in con:
                                                                if pesquisando_substantivo.palavra.i == substantivoPrincipal_FrasePrincipal.i:

                                                                    for substantivoPosterior in pesquisando_substantivo.substantivo:

                                                                        for pesquisando_substantivo_posterior in con:
                                                                            if pesquisando_substantivo_posterior.palavra.i == substantivoPosterior.i:

                                                                                for relacao in pesquisando_substantivo_posterior.demaisRelacoes:

                                                                                    if relacao.dep_ == "case":
                                                                                        substantivoComCase1.append(
                                                                                            relacao)
                                                                                        substantivoComCase1.append(
                                                                                            pesquisando_substantivo_posterior.palavra)
                                                                                        substantivoComCase1.append(
                                                                                            substantivoPrincipal_FrasePrincipal)

                                                                                        existeCase1 = 1

                                                            for substantivo in palavraFraseTeste.substantivoPrincipal:

                                                                if existeCase1 == 1:

                                                                    '''Verificar se existe e qual é o case do substantivo da frase a ser testada.'''

                                                                    for pesquisando_substantivo in con2:
                                                                        if pesquisando_substantivo.palavra.i == substantivo.i:

                                                                            for substantivoPosterior in pesquisando_substantivo.substantivo:

                                                                                for pesquisando_substantivo_posterior in con2:
                                                                                    if pesquisando_substantivo_posterior.palavra.i == substantivoPosterior.i:

                                                                                        for relacao in pesquisando_substantivo_posterior.demaisRelacoes:

                                                                                            if relacao.dep_ == "case":
                                                                                                substantivoComCase2.append(
                                                                                                    relacao)
                                                                                                substantivoComCase2.append(
                                                                                                    pesquisando_substantivo_posterior.palavra)
                                                                                                substantivoComCase2.append(
                                                                                                    substantivo)

                                                                                                existeCase2 = 1
                                                                if substantivoPrincipal_FrasePrincipal.text.lower() != "":
                                                                    if substantivo.text.lower() != "":
                                                                        if substantivoPrincipal_FrasePrincipal.text.lower() in self.cbow_model.vocab and substantivo.text.lower() in self.cbow_model.vocab:
                                                                            if substantivo.pos_ == "N" and self.cbow_model.similarity(
                                                                                    substantivoPrincipal_FrasePrincipal.text.lower(),
                                                                                    substantivo.text.lower()) > 0.5 or substantivoPrincipal_FrasePrincipal.text == substantivo.text:

                                                                                if existeCase1 == 1 and existeCase2 == 1:
                                                                                    if str(substantivoComCase1[
                                                                                               0].text) + " " + str(
                                                                                            substantivoComCase1[
                                                                                                1].text) == str(
                                                                                        substantivoComCase2[
                                                                                            0].text) + " " + str(
                                                                                        substantivoComCase2[1].text):
                                                                                        # print("Encontrou: "+str(substantivoComCase1[2].text)+" "+str(substantivoComCase1[0].text)+" "+str(substantivoComCase1[1].text+" "+palavraFraseTeste.palavra.text))

                                                                                        # verbo = VerboIgual(palavraFraseTeste.palavra)
                                                                                        verbo.substantivoPrincipal.append(
                                                                                            substantivoComCase1[2])

                                                                                        if jaAdicionouSubstantivo == 0:
                                                                                            substantivo = Classes.VerboIgual(
                                                                                                substantivoComCase1[2])
                                                                                            substantivo.substantivo.append(
                                                                                                substantivoComCase1[1])

                                                                                            substantivo2 = Classes.VerboIgual(
                                                                                                substantivoComCase1[1])
                                                                                            substantivo2.demaisRelacoes.append(
                                                                                                substantivoComCase1[0])

                                                                                            listaDeVerbos.append(
                                                                                                substantivo)
                                                                                            listaDeVerbos.append(
                                                                                                substantivo2)

                                                                                            jaAdicionouSubstantivo = 1

                                                                                        # listaDeVerbos.append(verbo)

                                                                                    elif str(substantivoComCase1[
                                                                                                 0].text) + " " + str(
                                                                                            substantivoComCase1[
                                                                                                1].text) != str(
                                                                                        substantivoComCase2[
                                                                                            0].text) + " " + str(
                                                                                        substantivoComCase2[1].text):
                                                                                        print("Não encontrou: " + str(
                                                                                            substantivoComCase1[
                                                                                                2].text) + " " + str(
                                                                                            substantivoComCase1[
                                                                                                0].text) + " " + str(
                                                                                            substantivoComCase1[
                                                                                                1].text + " " + palavraFraseTeste.palavra.text))

                                                                                    else:
                                                                                        if str(substantivoComCase1[
                                                                                                   0].text) + " " + str(
                                                                                                substantivoComCase1[
                                                                                                    1].text) == str(
                                                                                            substantivoComCase2[
                                                                                                0].text) + " " + str(
                                                                                            substantivoComCase2[
                                                                                                1].text) and str(
                                                                                            substantivoComCase1[
                                                                                                0].text) + " " + str(
                                                                                            substantivoComCase1[
                                                                                                1].text) == "":
                                                                                            print("ok")

                                                                                # Caso o substantivo principal do verbo não tenha cases ele adiciona somente o substantivo principal na comparação extraida
                                                                                if existeCase1 == 0 and existeCase2 == 0:

                                                                                    for substantivoTeste in palavraFraseTeste.substantivoPrincipal:

                                                                                        for substantivoPrincipal in palavra.substantivoPrincipal:

                                                                                            if substantivoTeste.pos_ != "NPROP" and substantivoPrincipal.pos_ != "NPROP":

                                                                                                if substantivoTeste.text.lower() != "":
                                                                                                    if substantivoPrincipal.text.lower() != "":
                                                                                                        if substantivoTeste.pos_ != "PUNCT":
                                                                                                            if substantivoPrincipal.pos_ != "PUNCT":
                                                                                                                if substantivoTeste.pos_ != "NUM":
                                                                                                                    if substantivoPrincipal.pos_ != "NUM":
                                                                                                                        if substantivoTeste.text.lower() in self.cbow_model.vocab and substantivoPrincipal.text.lower() in self.cbow_model.vocab:
                                                                                                                            if self.cbow_model.similarity(
                                                                                                                                    substantivoTeste.text.lower(),
                                                                                                                                    substantivoPrincipal.text.lower()) > 0.5:
                                                                                                                                # verbo = VerboIgual(palavraFraseTeste.palavra)
                                                                                                                                verbo.substantivoPrincipal.append(
                                                                                                                                    substantivoTeste)
                                                                                            else:

                                                                                                if substantivoTeste.pos_ == "NPROP" and substantivoPrincipal.pos_ == "NPROP":
                                                                                                    if substantivoTeste.text == substantivoPrincipal.text:
                                                                                                        verbo.substantivoPrincipal.append(
                                                                                                            substantivoTeste)

                                                                    existeCase2 = 0
                                                                existeCase1 = 0

                                                                # VERIFICAR DEMAIS RELAÇÕES DO VERBO
                                                                for relacaoTeste in palavraFraseTeste.demaisRelacoes:
                                                                    achouRelacao = 0

                                                                    for relacaoPrincipal in palavra.demaisRelacoes:

                                                                        if relacaoPrincipal.text.lower() != "":
                                                                            if relacaoTeste.text.lower() != "":
                                                                                if relacaoPrincipal.pos_ != "PUNCT":
                                                                                    if relacaoTeste.pos_ != "PUNCT":
                                                                                        if relacaoPrincipal.pos_ != "NUM":
                                                                                            if relacaoTeste.pos_ != "NUM":
                                                                                                if relacaoPrincipal.text.lower() in self.cbow_model.vocab and relacaoTeste.text.lower():
                                                                                                    if self.cbow_model.similarity(
                                                                                                            relacaoPrincipal.text.lower(),
                                                                                                            relacaoTeste.text.lower()) > 0.5:
                                                                                                        achouRelacao = 1

                                                                    if achouRelacao == 1:
                                                                        verbo.demaisRelacoes.append(relacaoTeste)

                                                                # VERIFICAR OS OUTROS VERBOS
                                                                achouSinonimo = 0

                                                                for verboTeste in palavraFraseTeste.verbos:
                                                                    listaDeSinonimos_ComparandoVerbos = self._ListarSinonimos(
                                                                        verboTeste.lemma_, cursor)
                                                                    achouSinonimo = 0
                                                                    for verboPrincipal in palavra.verbos:

                                                                        for sinonimo in listaDeSinonimos_ComparandoVerbos:

                                                                            if verboPrincipal.lemma_.upper() == \
                                                                                    sinonimo[0].upper():
                                                                                achouSinonimo = 1

                                                                        if achouSinonimo == 1:
                                                                            verbo.verbos.append(verboTeste)

                                                                # VERIFICAR OS SUBSTANTIVOS POSTERIORES

                                                                for substantivoPosteriorTeste in palavraFraseTeste.substantivo:

                                                                    for substantivoPosteriorPrincipal in palavra.substantivo:

                                                                        if substantivoPosteriorTeste.pos_ != "NPROP" and substantivoPosteriorPrincipal.pos_ != "NPROP":

                                                                            if substantivoPosteriorTeste.text.lower() != "":
                                                                                if substantivoPosteriorPrincipal.text.lower() != "":
                                                                                    if substantivoPosteriorTeste.pos_ != "PUNCT":
                                                                                        if substantivoPosteriorPrincipal.pos_ != "PUNCT":
                                                                                            if substantivoPosteriorTeste.pos_ != "NUM":
                                                                                                if substantivoPosteriorPrincipal.pos_ != "NUM":
                                                                                                    if substantivoPosteriorTeste.text.lower() in self.cbow_model.vocab and substantivoPosteriorPrincipal.text.lower() in self.cbow_model.vocab:
                                                                                                        if self.cbow_model.similarity(
                                                                                                                substantivoPosteriorTeste.text.lower(),
                                                                                                                substantivoPosteriorPrincipal.text.lower()) > 0.5:
                                                                                                            verbo.substantivo.append(
                                                                                                                substantivoPosteriorTeste)


                                                                        else:
                                                                            if substantivoPosteriorTeste.pos_ == "NPROP" and substantivoPosteriorPrincipal.pos_ == "NPROP":
                                                                                if substantivoPosteriorTeste.text == substantivoPosteriorPrincipal:
                                                                                    verbo.substantivo.append(
                                                                                        substantivoPosteriorTeste)

                                                                listaDeVerbos.append(verbo)
                                                            else:
                                                                print("Verbos diferentes por um adv negativo")

                                                        continua = 0

            PesoAdjetivos = 0.4
            PesoVerbos = 0.6

            if palavra.palavra.pos_ == "NPROP" or palavra.palavra.pos_ == "N" or palavra.palavra.pos_ == "PROADJ" or palavra.palavra.pos_ == "PRO-KS" or palavra.palavra.pos_ == "PROPESS" or palavra.palavra.pos_ == "PRO-KS-REL" or palavra.palavra.pos_ == "PROSUB" and palavra.palavra.dep_ != "case":

                for palavraFraseTeste in con2:

                    substantivosIguais = 0
                    if palavraFraseTeste.palavra.pos_ == "NPROP" or palavraFraseTeste.palavra.pos_ == "N" or palavraFraseTeste.palavra.pos_ == "PROADJ" or palavraFraseTeste.palavra.pos_ == "PRO-KS" or palavraFraseTeste.palavra.pos_ == "PROPESS" or palavraFraseTeste.palavra.pos_ == "PRO-KS-REL" or palavraFraseTeste.palavra.pos_ == "PROSUB" and palavraFraseTeste.palavra.dep_ != "case":

                        if palavra.palavra.text.upper() != palavraFraseTeste.palavra.text.upper():

                            if palavra.palavra.pos_ != "NPROP" and palavraFraseTeste.palavra.pos_ != "NPROP":

                                if palavra.palavra.text.lower() != "":
                                    if palavraFraseTeste.palavra.text.lower()!="":
                                        if palavra.palavra.text.lower() != "PUNCT":
                                            if palavraFraseTeste.palavra.text.lower() != "PUNCT":
                                                if palavra.palavra.text.lower() != "NUM":
                                                    if palavraFraseTeste.palavra.text.lower() != "NUM":
                                                        if palavra.palavra.text.lower() in self.cbow_model.vocab and palavraFraseTeste.palavra.text.lower() in self.cbow_model.vocab:
                                                            if self.cbow_model.similarity(palavra.palavra.text.lower(),palavraFraseTeste.palavra.text.lower()) > 0.6:
                                                                # verbo = VerboIgual(palavraFraseTeste.palavra)
                                                                substantivosIguais = 1
                            else:

                                if palavra.palavra.text == palavraFraseTeste.palavra.text:
                                    substantivosIguais = 1

                        if palavra.palavra.text.upper() == palavraFraseTeste.palavra.text.upper():
                            # verbo = VerboIgual(palavraFraseTeste.palavra)
                            substantivosIguais = 1

                        if substantivosIguais == 1:

                            # verbo = VerboIgual(palavraFraseTeste.palavra)

                            # Conferir se os substantivos realmente são iguais analisando os adjetivos e a quais verbos eles estão ligados
                            achouAdjetivo = 0

                            if len(palavra.adjetivos) > 0:

                                for adjetivoPrincipal in palavra.adjetivos:

                                    for adjetivoTeste in palavraFraseTeste.adjetivos:

                                        if adjetivoPrincipal.text.upper() != adjetivoTeste.text.upper():

                                            if adjetivoPrincipal.text.lower() != "":
                                                if adjetivoTeste.text.lower() != "":
                                                    if adjetivoPrincipal.pos_ != "PUNCT":
                                                        if adjetivoTeste.pos_ != "PUNCT":
                                                            if adjetivoPrincipal.pos_ != "NUM":
                                                                if adjetivoTeste.pos_ != "NUM":
                                                                    if adjetivoPrincipal.text.lower() in self.cbow_model.vocab and adjetivoTeste.text.lower() in self.cbow_model.vocab:
                                                                        if self.cbow_model.similarity(adjetivoPrincipal.text.lower(),adjetivoTeste.text.lower()) > 0.64:
                                                                            achouAdjetivo += 1

                                        else:
                                            achouAdjetivo += 1

                            listaDeVerbosPrincipal = []
                            listaDeVerbosTeste = []

                            for verboUtilizado in con:

                                if verboUtilizado.palavra.pos_ == "V" or verboUtilizado.palavra.pos_ == "VAUX":

                                    if len(verboUtilizado.substantivoPrincipal) > 0:

                                        if verboUtilizado.substantivoPrincipal[0].i == palavra.palavra.i:
                                            listaDeVerbosPrincipal.append(verboUtilizado)

                            for verboUtilizado in con2:
                                if verboUtilizado.palavra.pos_ == "V" or verboUtilizado.palavra.pos_ == "VAUX":

                                    if len(verboUtilizado.substantivoPrincipal) > 0:

                                        if verboUtilizado.substantivoPrincipal[0].i == palavraFraseTeste.palavra.i:
                                            listaDeVerbosTeste.append(verboUtilizado)

                            achouVerbo = 0

                            for verboP in listaDeVerbosPrincipal:

                                SinVerboP = self._ListarSinonimos(verboP.palavra.lemma_, cursor)

                                for verboT in listaDeVerbosTeste:

                                    if verboP.palavra.text.upper() != verboT.palavra.text.upper():

                                        for sinonimoVp in SinVerboP:

                                            if sinonimoVp[0].upper() == verboT.palavra.text.upper():
                                                achouVerbo += 1

                                    else:
                                        achouVerbo += 1

                            '''
                            print(palavra.palavra.text)
                            print(palavraFraseTeste.palavra.text)
                            print(achouVerbo," de ",len(listaDeVerbosPrincipal)," verbos encontrado")
                            print(achouAdjetivo," de ",len(palavra.adjetivos)," adjetivos encontrado")
                            #print(math.ceil(len(listaDeVerbosPrincipal)*0.6))
                            '''

                            achouVerboEmResultado = 0
                            if achouVerbo >= math.ceil(
                                    len(listaDeVerbosPrincipal) * PesoVerbos) and achouAdjetivo >= math.ceil(
                                    len(palavra.adjetivos) * PesoAdjetivos):

                                '''
                                for vb in listaDeVerbos:
                                    print(vb.palavra.i," ",palavraFraseTeste.palavra.i," ",palavraFraseTeste.palavra.text)
                                    if vb.palavra.i == palavraFraseTeste.palavra.i:
                                        print(palavraFraseTeste.palavra.text)
                                        vb.substantivo = palavraFraseTeste.substantivo
                                        vb.demaisRelacoes = palavraFraseTeste.demaisRelacoes
                                        vb.verbos = palavraFraseTeste.verbos
                                        vb.adjetivos = palavraFraseTeste.adjetivos
                                        achouVerboEmResultado = 1
    
    
    
    
    
                                if achouVerboEmResultado == 0:
    
                                    verbo = VerboIgual(palavraFraseTeste.palavra)
                                    verbo.demaisRelacoes = palavraFraseTeste.demaisRelacoes
                                    verbo.substantivo = palavraFraseTeste.substantivo
                                    verbo.substantivoPrincipal = palavraFraseTeste.substantivoPrincipal
                                    verbo.verbos = palavraFraseTeste.verbos
                                    verbo.adjetivos = palavraFraseTeste.adjetivos
    
                                    listaDeVerbos.append(verbo)
    
                                else:
                                    achouVerboEmResultado = 0
                                '''
                                verbo = Classes.VerboIgual(palavraFraseTeste.palavra)
                                verbo.demaisRelacoes = palavraFraseTeste.demaisRelacoes
                                verbo.substantivo = palavraFraseTeste.substantivo
                                verbo.substantivoPrincipal = palavraFraseTeste.substantivoPrincipal
                                verbo.verbos = palavraFraseTeste.verbos
                                verbo.adjetivos = palavraFraseTeste.adjetivos

                                for vb in listaDeVerbos:

                                    if vb.verbo.i == verbo.verbo.i:
                                        listaDeVerbos.remove(vb)

                                listaDeVerbos.append(verbo)

        return listaDeVerbos


    def _AdicionarNosNoGrafo(self, conhecimento, G):
        for objeto in conhecimento:
            txt = objeto.verbo.text + "_" + str(objeto.verbo.i)
            G.add_node(txt, pos=objeto.verbo.pos_, dep=objeto.verbo.dep_)

            for subPrin in objeto.substantivoPrincipal:
                txt = subPrin.text + "_" + str(subPrin.i)
                G.add_node(txt, pos=subPrin.pos_, dep=subPrin.dep_)

            for sub in objeto.substantivo:
                txt = sub.text + "_" + str(sub.i)
                G.add_node(txt, pos=sub.pos_, dep=sub.dep_)

            for demais in objeto.demaisRelacoes:
                txt = demais.text + "_" + str(demais.i)
                G.add_node(txt, pos=demais.pos_, dep=demais.dep_)

            for verbo in objeto.verbos:
                txt = verbo.text + "_" + str(verbo.i)
                G.add_node(txt, pos=verbo.pos_, dep=verbo.dep_)

            for adjetivo in objeto.adjetivos:
                txt = adjetivo.text + "_" + str(adjetivo.i)
                G.add_node(txt, pos=adjetivo.pos_, dep=adjetivo.dep_)

        return G


    def _AdicionarLigacoesNoGrafo(self, conhecimento, G):
        for objeto in conhecimento:
            if objeto.verbo.pos_ == "V" or objeto.verbo.pos_ == "VAUX" or objeto.verbo.pos_ == "PCP":

                for subPrin in objeto.substantivoPrincipal:
                    aux = subPrin.text + "_" + str(subPrin.i)
                    aux2 = objeto.verbo.text + "_" + str(objeto.verbo.i)
                    G.add_edge(aux, aux2)

                for subPos in objeto.substantivo:
                    aux = objeto.verbo.text + "_" + str(objeto.verbo.i)
                    aux2 = subPos.text + "_" + str(subPos.i)
                    G.add_edge(aux, aux2)

                for demais in objeto.demaisRelacoes:
                    aux = objeto.verbo.text + "_" + str(objeto.verbo.i)
                    aux2 = demais.text + "_" + str(demais.i)
                    G.add_edge(aux, aux2)

                for verbo in objeto.verbos:

                    aux2 = verbo.text + "_" + str(verbo.i)

                    if verbo.i > objeto.verbo.i:
                        aux = objeto.verbo.text + "_" + str(objeto.verbo.i)
                        G.add_edge(aux, aux2)

                    if len(objeto.substantivoPrincipal) > 0:
                        aux = objeto.substantivoPrincipal[0].text + "_" + str(objeto.substantivoPrincipal[0].i)
                        G.add_edge(aux, aux2)

                    for sub in objeto.substantivo:
                        aux = sub.text + "_" + str(sub.i)
                        G.add_edge(aux, aux2)

            if objeto.verbo.pos_ == "N" or objeto.verbo.pos_ == "NPROP" or objeto.verbo.pos_ == "PROADJ" or objeto.verbo.pos_ == "PRO-KS" or objeto.verbo.pos_ == "PROPESS" or objeto.verbo.pos_ == "PRO-KS-REL" or objeto.verbo.pos_ == "PROSUB":
                for subPos in objeto.substantivo:
                    aux = objeto.verbo.text + "_" + str(objeto.verbo.i)
                    aux2 = subPos.text + "_" + str(subPos.i)
                    G.add_edge(aux, aux2)

                for demais in objeto.demaisRelacoes:
                    aux = objeto.verbo.text + "_" + str(objeto.verbo.i)
                    aux2 = demais.text + "_" + str(demais.i)
                    G.add_edge(aux, aux2)

                for verbo in objeto.verbos:
                    aux = objeto.verbo.text + "_" + str(objeto.verbo.i)
                    aux2 = verbo.text + "_" + str(verbo.i)
                    G.add_edge(aux, aux2)

            if objeto.verbo.dep_ == "case":
                for subPrin in objeto.substantivoPrincipal:
                    aux = subPrin.text + "_" + str(subPrin.i)
                    aux2 = objeto.verbo.text + "_" + str(objeto.verbo.i)
                    G.add_edge(aux, aux2)

                for subPos in objeto.substantivo:
                    aux = objeto.verbo.text + "_" + str(objeto.verbo.i)
                    aux2 = subPos.text + "_" + str(subPos.i)
                    G.add_edge(aux, aux2)

            if objeto.verbo.pos_ == "ADJ":

                for subPos in objeto.substantivo:
                    aux = objeto.verbo.text + "_" + str(objeto.verbo.i)
                    aux2 = subPos.text + "_" + str(subPos.i)
                    G.add_edge(aux, aux2)

                for verbo in objeto.verbos:
                    for substantivo in objeto.substantivo:
                        aux = substantivo.text + "_" + str(substantivo.i)
                        aux2 = verbo.text + "_" + str(verbo.i)
                        G.add_edge(aux, aux2)

                for demais in objeto.demaisRelacoes:
                    aux = objeto.verbo.text + "_" + str(objeto.verbo.i)
                    aux2 = demais.text + "_" + str(demais.i)
                    G.add_edge(aux, aux2)

        return G


    def ImprimirGrafo(self):
        con = self.Comparacao

        G = nx.Graph()
        G = self._AdicionarNosNoGrafo(con, G)
        G = self._AdicionarLigacoesNoGrafo(con, G)

        print(list(G.edges))
        pos = nx.spring_layout(G)

        substantivos = []
        verbos = []
        cases = []
        outros = []
        adjetivos = []
        adverbios = []

        for node in G.nodes.data():

            if node[1]["dep"] == "case":
                cases.append(node[0])

            elif node[1]["pos"] == "N" or node[1]["pos"] == "NPROP" or node[1]["pos"] == "PROADJ" or node[1][
                "pos"] == "PRO-KS" or node[1]["pos"] == "PROPESS" or node[1]["pos"] == "PRO-KS-REL" or node[1][
                "pos"] == "PROSUB":
                substantivos.append(node[0])

            elif node[1]["pos"] == "V" or node[1]["pos"] == "VAUX" or node[1]["pos"] == "PCP":
                verbos.append(node[0])

            elif node[1]["pos"] == "ADJ":
                adjetivos.append(node[0])
            elif node[1]["pos"] == "ADV":
                adverbios.append(node[0])

            else:
                outros.append(node[0])

        nx.draw_networkx_nodes(G, pos, adverbios, node_color='purple', node_size=700, arrows=True)
        nx.draw_networkx_nodes(G, pos, substantivos, node_color='y', node_size=700, arrows=True)
        nx.draw_networkx_nodes(G, pos, verbos, node_color='red', node_size=500, arrows=True)
        nx.draw_networkx_nodes(G, pos, cases, node_color='blue', node_size=350, arrows=True)
        nx.draw_networkx_nodes(G, pos, adjetivos, node_color='pink', node_size=300, arrows=True)
        nx.draw_networkx_nodes(G, pos, outros, node_color='green', node_size=200, arrows=True)
        nx.draw_networkx_labels(G, pos, font_size=8)
        nx.draw_networkx_edges(G, pos, edge_color='black', arrows=True)

        plt.axis('off')
        plt.show()