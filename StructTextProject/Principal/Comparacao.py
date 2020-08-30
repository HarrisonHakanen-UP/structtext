'''WordEmbeddings'''
from gensim.models import KeyedVectors
from gensim.models import Word2Vec
import sys
from IPython.display import display, HTML
from IPython.display import Image
from jinja2 import Template
import mysql.connector as mysql

from Model import Classes

class Comparacao:
    # skip_gram_model = KeyedVectors.load_word2vec_format('skip_s50.txt',binary=False)
    # print("skip-gram pronto")

    def __init__(self,con,con2):
        self.con = con
        self.con2 = con2
        self.cbow_model =KeyedVectors.load_word2vec_format('cbow_s100.txt', binary=False)
        self.Comparacao = self._CompararConhecimentos()

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

    def _ListarSinonimos(palavra, cursor):
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

    def CompararConhecimentos(self,con, con2):

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

                        # Verifica se o verbo da frase principal e o verbo da frase que está sendo testada tem mais de 0.6 de semelhança
                        if self.cbow_model.similarity(palavra.palavra.lemma_, palavraFraseTeste.palavra.lemma_) > 0.6:

                            if palavra.palavra.lemma_ != palavraFraseTeste.palavra.lemma_:

                                # Verifica se a palavra está na lista de sinônimos
                                for sinonimo in listaDeSinonimos:

                                    if sinonimo[0].upper() == palavraFraseTeste.palavra.lemma_.upper():
                                        continua = 1

                            else:
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
                                if VerboPrincipalNegativo == 1 and VerboTesteNegativo == 1 or VerboPrincipalNegativo == 0 and VerboTesteNegativo == 0:

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
                                                                    substantivoComCase1.append(relacao)
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
                                                                            substantivoComCase2.append(relacao)
                                                                            substantivoComCase2.append(
                                                                                pesquisando_substantivo_posterior.palavra)
                                                                            substantivoComCase2.append(substantivo)

                                                                            existeCase2 = 1

                                            if substantivo.pos_ == "N" and self.cbow_model.similarity(
                                                    substantivoPrincipal_FrasePrincipal.text,
                                                    substantivo.text) > 0.5 or substantivoPrincipal_FrasePrincipal.text == substantivo.text:

                                                if existeCase1 == 1 and existeCase2 == 1:
                                                    if str(substantivoComCase1[0].text) + " " + str(
                                                            substantivoComCase1[1].text) == str(
                                                            substantivoComCase2[0].text) + " " + str(
                                                            substantivoComCase2[1].text):
                                                        print("Encontrou: " + str(
                                                            substantivoComCase1[2].text) + " " + str(
                                                            substantivoComCase1[0].text) + " " + str(
                                                            substantivoComCase1[
                                                                1].text + " " + palavraFraseTeste.palavra.text))

                                                        # verbo = VerboIgual(palavraFraseTeste.palavra)
                                                        verbo.substantivoPrincipal.append(substantivoComCase1[2])

                                                        if jaAdicionouSubstantivo == 0:
                                                            substantivo = Classes.VerboIgual(substantivoComCase1[2])
                                                            substantivo.substantivo.append(substantivoComCase1[1])

                                                            substantivo2 = Classes.VerboIgual(substantivoComCase1[1])
                                                            substantivo2.demaisRelacoes.append(substantivoComCase1[0])

                                                            listaDeVerbos.append(substantivo)
                                                            listaDeVerbos.append(substantivo2)

                                                            jaAdicionouSubstantivo = 1

                                                        # listaDeVerbos.append(verbo)

                                                    elif str(substantivoComCase1[0].text) + " " + str(
                                                            substantivoComCase1[1].text) != str(
                                                            substantivoComCase2[0].text) + " " + str(
                                                            substantivoComCase2[1].text):
                                                        print("Não encontrou: " + str(
                                                            substantivoComCase1[2].text) + " " + str(
                                                            substantivoComCase1[0].text) + " " + str(
                                                            substantivoComCase1[
                                                                1].text + " " + palavraFraseTeste.palavra.text))

                                                    else:
                                                        if str(substantivoComCase1[0].text) + " " + str(
                                                                substantivoComCase1[1].text) == str(
                                                                substantivoComCase2[0].text) + " " + str(
                                                                substantivoComCase2[1].text) and str(
                                                                substantivoComCase1[0].text) + " " + str(
                                                                substantivoComCase1[1].text) == "":
                                                            print("ok")

                                                # Caso o substantivo principal do verbo não tenha cases ele adiciona somente o substantivo principal na comparação extraida
                                                if existeCase1 == 0 and existeCase2 == 0:

                                                    print(palavraFraseTeste.palavra.text)
                                                    print(palavra.palavra.text)

                                                    for substantivoTeste in palavraFraseTeste.substantivoPrincipal:

                                                        for substantivoPrincipal in palavra.substantivoPrincipal:

                                                            if substantivoTeste.pos_ != "NPROP" and substantivoPrincipal.pos_ != "NPROP":

                                                                if self.cbow_model.similarity(substantivoTeste.text,
                                                                                         substantivoPrincipal.text) > 0.5:
                                                                    # verbo = VerboIgual(palavraFraseTeste.palavra)
                                                                    verbo.substantivoPrincipal.append(substantivoTeste)
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

                                            if self.cbow_model.similarity(relacaoPrincipal.text, relacaoTeste.text) > 0.5:
                                                achouRelacao = 1

                                        if achouRelacao == 1:
                                            verbo.demaisRelacoes.append(relacaoTeste)

                                    # VERIFICAR OS OUTROS VERBOS
                                    achouSinonimo = 0

                                    for verboTeste in palavraFraseTeste.verbos:
                                        listaDeSinonimos_ComparandoVerbos = self._ListarSinonimos(verboTeste.lemma_, cursor)
                                        achouSinonimo = 0
                                        for verboPrincipal in palavra.verbos:

                                            for sinonimo in listaDeSinonimos_ComparandoVerbos:

                                                if verboPrincipal.lemma_.upper() == sinonimo[0].upper():
                                                    achouSinonimo = 1

                                            if achouSinonimo == 1:
                                                verbo.verbos.append(verboTeste)

                                    # VERIFICAR OS SUBSTANTIVOS POSTERIORES

                                    for substantivoPosteriorTeste in palavraFraseTeste.substantivo:

                                        for substantivoPosteriorPrincipal in palavra.substantivo:

                                            if substantivoPosteriorTeste.pos_ != "NPROP" and substantivoPosteriorPrincipal.pos_ != "NPROP":
                                                if self.cbow_model.similarity(substantivoPosteriorTeste.text,
                                                                         substantivoPosteriorPrincipal.text) > 0.5:
                                                    verbo.substantivo.append(substantivoPosteriorTeste)

                                            else:
                                                if substantivoPosteriorTeste.pos_ == "NPROP" and substantivoPosteriorPrincipal.pos_ == "NPROP":
                                                    if substantivoPosteriorTeste.text == substantivoPosteriorPrincipal:
                                                        verbo.substantivo.append(substantivoPosteriorTeste)

                                    listaDeVerbos.append(verbo)
                                else:
                                    print("Verbos diferentes por um adv negativo")

                            continua = 0

            # Ainda não estou testando NPROP
            PesoAdjetivos = 0.4
            PesoVerbos = 0.6

            if palavra.palavra.pos_ == "N" or palavra.palavra.pos_ == "PROADJ" or palavra.palavra.pos_ == "PRO-KS" or palavra.palavra.pos_ == "PROPESS" or palavra.palavra.pos_ == "PRO-KS-REL" or palavra.palavra.pos_ == "PROSUB" and palavra.palavra.dep_ != "case":

                for palavraFraseTeste in con2:

                    substantivosIguais = 0
                    if palavraFraseTeste.palavra.pos_ == "N" or palavraFraseTeste.palavra.pos_ == "PROADJ" or palavraFraseTeste.palavra.pos_ == "PRO-KS" or palavraFraseTeste.palavra.pos_ == "PROPESS" or palavraFraseTeste.palavra.pos_ == "PRO-KS-REL" or palavraFraseTeste.palavra.pos_ == "PROSUB" and palavraFraseTeste.palavra.dep_ != "case":

                        if palavra.palavra.text.upper() != palavraFraseTeste.palavra.text.upper():

                            if self.cbow_model.similarity(palavra.palavra.text, palavraFraseTeste.palavra.text) > 0.5:
                                # verbo = VerboIgual(palavraFraseTeste.palavra)
                                substantivosIguais = 1

                        if palavra.palavra.text.upper() == palavraFraseTeste.palavra.text.upper():
                            # verbo = VerboIgual(palavraFraseTeste.palavra)
                            substantivosIguais = 1

                        if substantivosIguais == 1:

                            verbo = Classes.VerboIgual(palavraFraseTeste.palavra)

                            # Conferir se os substantivos realmente são iguais analisando os adjetivos e a quais verbos eles estão ligados

                            if len(palavra.adjetivos) > 0:

                                for adjetivoPrincipal in palavra.adjetivos:

                                    achouAdjetivo = 0

                                    for adjetivoTeste in palavraFraseTeste.adjetivos:

                                        if adjetivoPrincipal.text.upper() != adjetivoTeste.text.upper():

                                            if self.cbow_model.similarity(adjetivoPrincipal.text, adjetivoTeste.text) > 0.5:
                                                achouAdjetivo += 1

                                        else:

                                            achouAdjetivo += 1



        return listaDeVerbos