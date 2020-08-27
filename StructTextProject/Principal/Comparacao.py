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

    def CompararConhecimentos(self, con, con2):

        db = mysql.connect(
            host="localhost",
            user="root",
            password="testeTCC",
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

                                    if sinonimo[0] == palavraFraseTeste.palavra.lemma_:
                                        continua = 1

                            else:
                                continua = 1

                            if continua == 1:

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

                                                                    # Verificar as demais relações do substantivo
                                                                    # ...

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

                                                                            # Verificar as demais relações do substantivo
                                                                            # ...

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

                                                        verbo = Classes.VerboIgual(palavraFraseTeste.palavra)
                                                        verbo.substantivoPrincipal.append(substantivoComCase1[2])

                                                        if jaAdicionouSubstantivo == 0:
                                                            substantivo = Classes.VerboIgual(substantivoComCase1[2])
                                                            substantivo.substantivo.append(substantivoComCase1[1])

                                                            substantivo2 = Classes.VerboIgual(substantivoComCase1[1])
                                                            substantivo2.demaisRelacoes.append(substantivoComCase1[0])

                                                            listaDeVerbos.append(substantivo)
                                                            listaDeVerbos.append(substantivo2)

                                                            jaAdicionouSubstantivo = 1

                                                        listaDeVerbos.append(verbo)

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

                                                if existeCase1 == 0 and existeCase2 == 0:

                                                    # O objeto palavra refere ao original.
                                                    # O objeto substantivoPrincipal_FrasePrincipal se refere ao original

                                                    # O objeto palavraFraseTeste se refere ao testado
                                                    # O objeto substantivo se refere ao testado.

                                                    # Verificando outros substantivos no mesmo substantivo.
                                                    '''
                                                    Substantivo_Principal_Conhecimento = []
                                                    Substantivo_Teste_Conhecimento = []

                                                    for subFrasePrincipal in con:

                                                        if subFrasePrincipal.palavra.i == substantivoPrincipal_FrasePrincipal.i:
                                                            Substantivo_Principal_Conhecimento = subFrasePrincipal
                                                            break


                                                    for subFraseTeste in con2:

                                                        if substantivo.i == subFraseTeste.palavra.i:
                                                            Substantivo_Teste_Conhecimento
                                                    '''

                                                    for subFrasePrincipal in con:
                                                        if substantivoPrincipal_FrasePrincipal.i == subFrasePrincipal.palavra.i:

                                                            # Comparando os substantivos de um substantivo
                                                            for SubstantivoPosterior_Principal in subFrasePrincipal.substantivo:

                                                                for subFraseTeste in con2:
                                                                    if substantivo.i == subFraseTeste.palavra.i:

                                                                        for SubstantivoPosterior_Teste in subFraseTeste.substantivo:

                                                                            if SubstantivoPosterior_Principal.pos_ == "N" and SubstantivoPosterior_Teste.pos_ == "N":
                                                                                if self.cbow_model.similarity(
                                                                                        SubstantivoPosterior_Principal.text,
                                                                                        SubstantivoPosterior_Teste.text) < 0.5:
                                                                                    print(
                                                                                        SubstantivoPosterior_Teste.text)
                                                                                    subFraseTeste.substantivo.remove(
                                                                                        SubstantivoPosterior_Teste)

                                                                            if SubstantivoPosterior_Principal.text != SubstantivoPosterior_Teste.text:
                                                                                print(SubstantivoPosterior_Teste.text)
                                                                                subFraseTeste.substantivo.remove(
                                                                                    SubstantivoPosterior_Teste)

                                                            for SubstantivoPosterior_Principal in subFrasePrincipal.demaisRelacoes:

                                                                for subFraseTeste in con2:
                                                                    if substantivo.i == subFraseTeste.palavra.i:

                                                                        for SubstantivoPosterior_Teste in subFraseTeste.demaisRelacoes:

                                                                            if self.cbow_model.similarity(
                                                                                    SubstantivoPosterior_Principal.text,
                                                                                    SubstantivoPosterior_Teste.text) < 0.5:
                                                                                print(SubstantivoPosterior_Teste.text)
                                                                                subFraseTeste.substantivo.remove(
                                                                                    SubstantivoPosterior_Teste)

                                                                            if SubstantivoPosterior_Principal.text != SubstantivoPosterior_Teste.text:
                                                                                print(SubstantivoPosterior_Teste.text)
                                                                                subFraseTeste.substantivo.remove(
                                                                                    SubstantivoPosterior_Teste)

                                                            for SubstantivoPosterior_Principal in subFrasePrincipal.adjetivos:

                                                                for subFraseTeste in con2:
                                                                    if substantivo.i == subFraseTeste.palavra.i:

                                                                        for SubstantivoPosterior_Teste in subFraseTeste.adjetivos:

                                                                            if self.cbow_model.similarity(
                                                                                    SubstantivoPosterior_Principal.text,
                                                                                    SubstantivoPosterior_Teste.text) < 0.5:
                                                                                print(SubstantivoPosterior_Teste.text)
                                                                                subFraseTeste.substantivo.remove(
                                                                                    SubstantivoPosterior_Teste)

                                                                            if SubstantivoPosterior_Principal.text != SubstantivoPosterior_Teste.text:
                                                                                print(SubstantivoPosterior_Teste.text)
                                                                                subFraseTeste.substantivo.remove(
                                                                                    SubstantivoPosterior_Teste)

                                                            for SubstantivoPosterior_Principal in subFrasePrincipal.verbos:

                                                                for subFraseTeste in con2:
                                                                    if substantivo.i == subFraseTeste.palavra.i:

                                                                        for SubstantivoPosterior_Teste in subFraseTeste.verbos:

                                                                            if self.cbow_model.similarity(
                                                                                    SubstantivoPosterior_Principal.text,
                                                                                    SubstantivoPosterior_Teste.text) < 0.5:
                                                                                print(SubstantivoPosterior_Teste.text)
                                                                                subFraseTeste.substantivo.remove(
                                                                                    SubstantivoPosterior_Teste)

                                                                            if SubstantivoPosterior_Principal.text != SubstantivoPosterior_Teste.text:
                                                                                print(SubstantivoPosterior_Teste.text)
                                                                                subFraseTeste.substantivo.remove(
                                                                                    SubstantivoPosterior_Teste)

                                                    verbo = Classes.VerboIgual(palavra.palavra)
                                                    verbo.substantivoPrincipal.append(
                                                        substantivoPrincipal_FrasePrincipal)
                                                    listaDeVerbos.append(verbo)

                                        existeCase2 = 0
                                    existeCase1 = 0

                                    substantivoComCase1 = []
                                    substantivoComCase2 = []

                                    # VERIFICAR DEMAIS RELAÇÕES DO VERBO
                                    # ...

                                else:
                                    print("Verbos diferentes por um adv negativo")
                            continua = 0

        return listaDeVerbos