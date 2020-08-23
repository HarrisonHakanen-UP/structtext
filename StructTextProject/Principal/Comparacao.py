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


    def _CompararConhecimentos(self):
        con = self.con
        con2 = self.con2

        db = mysql.connect(
            host="localhost",
            user="root",
            password="Eunaosei1997",
            database="WordNet_WordNetBr"
        )

        cursor = db.cursor()

        listaDeSinonimos = []

        listaDeVerbos = []

        listaDeVerbosNaoExistentes = []

        encontrou = 0

        continua = 0

        achouVerbo = 0

        for palavra in con:
            if palavra.palavra.pos_ == "VERB":

                listaDeSinonimos = self._ListarSinonimos(palavra.palavra.lemma_, cursor)

                for palavraFraseTeste in con2:

                    if palavraFraseTeste.palavra.pos_ == "VERB":

                        # Verifica se o verbo da frase principal e o verbo da frase que está sendo testada tem mais de 0.6 de semelhança
                        if self.cbow_model.similarity(palavra.palavra.text, palavraFraseTeste.palavra.text) > 0.6:

                            if palavra.palavra.lemma_ != palavraFraseTeste.palavra.lemma_:

                                for sinonimo in listaDeSinonimos:

                                    if sinonimo[0] == palavraFraseTeste.palavra.lemma_:
                                        continua = 1

                            else:
                                continua = 1

                            if continua == 1:
                                verbo = Classes.VerboIgual(palavraFraseTeste.palavra)

                                # VERIFICAR O SUBSTANTIVO PRINCIPAL
                                for substantivoPrincipal_FrasePrincipal in palavra.substantivoPrincipal:

                                    '''Trasnformar isso em método'''
                                    if len(palavraFraseTeste.substantivoPrincipal) > 0:
                                        for substantivo in palavraFraseTeste.substantivoPrincipal:

                                            if substantivoPrincipal_FrasePrincipal.text == substantivo.text:
                                                verbo.substantivoPrincipal.append(substantivo)

                                            else:

                                                if self.cbow_model.similarity(substantivoPrincipal_FrasePrincipal.text,
                                                                         substantivo.text) > 0.5:
                                                    verbo.substantivoPrincipal.append(substantivo)
                                                else:
                                                    verbo.substantivoPrincipal_naoEncontrado.append(0)

                                    '''-----------------------------------------------'''

                                # VERIFICAR OS SUBSTANTIVOS POSTERIORES
                                for substantivoPosterior_FrasePrincipal in palavra.substantivo:

                                    '''Trasnformar isso em método'''
                                    if len(palavraFraseTeste.substantivo) > 0:
                                        for substantivoPosteriorTeste in palavraFraseTeste.substantivo:

                                            if substantivoPosterior_FrasePrincipal.text == substantivoPosteriorTeste.text:
                                                verbo.substantivo.append(substantivoPosteriorTeste)
                                                encontrou = 1

                                            else:
                                                if self.cbow_model.similarity(substantivoPosterior_FrasePrincipal.text,
                                                                         substantivoPosteriorTeste.text) > 0.5:
                                                    verbo.substantivo.append(substantivoPosteriorTeste)
                                                    encontrou = 1

                                        if encontrou == 0:
                                            verbo.substantivo_naoEncontrado.append(substantivoPosterior_FrasePrincipal)
                                        else:
                                            encontrou = 0
                                    '''-----------------------------------------------'''
                                # VERIFICAR OS VERBOS
                                for verbo_FrasePrincipal in palavra.verbos:

                                    listaDeSinonimosVerbos = self._ListarSinonimos(verbo_FrasePrincipal.lemma_, cursor)

                                    if len(palavraFraseTeste.verbos) > 0:

                                        for verbo_FraseTeste in palavraFraseTeste.verbos:

                                            print(verbo_FraseTeste.text)
                                            for sin in listaDeSinonimosVerbos:
                                                if verbo_FraseTeste.text == sin[0]:
                                                    achouVerbo = 1

                                            if achouVerbo == 0:

                                                verbo.verbos_naoEncontrados.append(verbo_FrasePrincipal)

                                            else:
                                                achouVerbo = 0

                                        for sin in listaDeSinonimosVerbos:
                                            if verbo_FrasePrincipal.lemma_ == sin[0]:
                                                achouVerbo = 1
                                    else:
                                        verbo.verbos_naoEncontrados.append(verbo_FrasePrincipal)

                                # VERIFICAR OS ADJETIVOS
                                for adjetivo_FrasePrincipal in palavra.adjetivos:

                                    '''Trasnformar isso em método'''
                                    if len(palavraFraseTeste.adjetivos) > 0:
                                        for adjetivoTeste in palavraFraseTeste.adjetivos:

                                            if adjetivo_FrasePrincipal.text == adjetivoTeste.text:
                                                verbo.adjetivos.append(adjetivoTeste)
                                                encontrou = 1
                                            else:
                                                if self.cbow_model.similarity(adjetivo_FrasePrincipal.text,
                                                                         adjetivoTeste.text) > 0.5:
                                                    verbo.adjetivos.append(adjetivoTeste)
                                                    encontrou = 1

                                    if encontrou == 0:
                                        verbo.adjetivos_naoEncontrados.append(adjetivo_FrasePrincipal)
                                    else:
                                        encontrou = 0
                                    '''-----------------------------------------------'''

                                # VERIFICAR AS DEMAIS RELAÇÕES
                                for relacao_FrasePrincipal in palavra.demaisRelacoes:
                                    # print(relacao_FrasePrincipal.text)

                                    '''Trasnformar isso em método'''
                                    if len(palavraFraseTeste.demaisRelacoes) > 0:
                                        for relacaoTeste in palavraFraseTeste.demaisRelacoes:

                                            if relacao_FrasePrincipal.text == relacaoTeste.text:
                                                verbo.demaisRelacoes.append(relacaoTeste)
                                                encontrou = 1

                                            else:
                                                if self.cbow_model.similarity(relacao_FrasePrincipal.text, relacaoTeste.text) > 0.5:
                                                    verbo.demaisRelacoes.append(relacaoTeste)
                                                    encontrou = 1

                                    if encontrou == 0:
                                        verbo.demaisRelacoes_naoEncontradas.append(relacao_FrasePrincipal)
                                    else:
                                        encontrou = 0
                                    '''-----------------------------------------------'''

                                listaDeVerbos.append(verbo)

                            continua = 0

        return listaDeVerbos
