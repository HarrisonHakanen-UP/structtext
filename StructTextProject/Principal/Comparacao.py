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

    def __init__(self,con,con2,model):
        self.con = con
        self.con2 = con2

        self.cbow_model = model
        self.Comparacao = self._CompararConhecimentos(self.con,self.con2)



    def getSemelhanca(self):
        return self.semelhanca

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
            password="password",
            database="WordNet_WordNetBr",
            auth_plugin='mysql_native_password'
        )

        palavrasNaoEncontradas = []

        substantivoComCase1 = []
        substantivoComCase2 = []
        existeCase1 = 0
        existeCase2 = 0

        cursor = db.cursor()

        listaDeSinonimos = []

        jaAdicionouSubstantivo = 0

        listaDeVerbos = []

        ##-----------FUNCIONA PARA VERBOS E SUBSTANTIVOS--------------------

        ListaDeVerbosQueJaPassaram = []
        ListaDeVerbosQueJaPassaramTeste = []

        ListaDeSubstantivosQueJaPassaram = []
        ListaDeSubstantivosQueJaPassaramTeste = []

        # ---------------------------------------------------

        # -----FUNCIONA EXCLUSIVAMENTE PARA VERBOS--------

        # Ligações corretas são ligações que o verbo e o substantivo coicidem
        ListaDeLigacoesCorretas = []
        ListaDeLigacoesCorretasTeste = []

        ListaDeDemaisRelacoesQueJaPassaram = []
        ListaDeDemaisRelacoesQueJaPassaramTeste = []

        ListaDeDemaisVerbosQueJaPassaram = []
        ListaDeDemaisVerbosQueJaPassaramTeste = []
        SubstantivosPosterioresSemPrincipalCorretos = []

        Certezas = []
        CertezasTeste = []
        # ---------------------------------------------------

        listaDeVerbosNegativos = []

        encontrou = 0

        continua = 0

        achouVerbo = 0

        for palavra in con.conhecimentoMaster:

            if palavra.palavra.pos_ == "V" or palavra.palavra.pos_ == "VAUX" or palavra.palavra.pos_ == "PCP" or palavra.palavra.pos_ == "VERB":

                listaDeSinonimos = self._ListarSinonimos(palavra.palavra.lemma_, cursor)

                if palavra.palavra.dep_ != "cop" and palavra.palavra.depStanza_ != "cop":
                    ListaDeVerbosQueJaPassaram.append(palavra)

                if len(palavra.substantivo) > 0:
                    ListaDeLigacoesCorretas.append(palavra)

                for palavraFraseTeste in con2.conhecimentoMaster:

                    if palavraFraseTeste.palavra.pos_ == "V" or palavraFraseTeste.palavra.pos_ == "VAUX" or palavraFraseTeste.palavra.pos_ == "PCP" or palavraFraseTeste.palavra.pos_ == "VERB":

                        if palavraFraseTeste.palavra.lemma_.lower() != "":
                            if palavra.palavra.lemma_.lower() != "":
                                if palavraFraseTeste.palavra.pos_ != "PUNCT":
                                    if palavra.palavra.pos_ != "PUNCT":
                                        if palavraFraseTeste.palavra.pos_ != "NUM":
                                            if palavra.palavra.pos_ != "NUM":

                                                if (
                                                        palavra.palavra.dep_ == "cop" or palavra.palavra.depStanza_ == "cop") and (
                                                        palavraFraseTeste.palavra.dep_ == "cop" or palavraFraseTeste.palavra.depStanza_ == "cop"):

                                                    contCertezas = 0
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
                                                                                                contCertezas += 1

                                                    if contCertezas >= len(palavra.substantivo):
                                                        '''
                                                        print(palavra.palavra.text)
                                                        for subs in palavra.substantivo:
                                                            print(subs.text)
                                                        print("\n")
                                                        print(palavraFraseTeste.palavra.text)
                                                        for subs in palavraFraseTeste.substantivo:
                                                            print(subs.text)
                                                        '''

                                                        Certezas.append(palavra.palavra)

                                                    contCertezas = 0
                                                    # verbo.substantivo.append(substantivoPosteriorTeste)
                                                    # SubstantivosCorretos.append(substantivoPosteriorTeste)



                                                else:

                                                    # Verifica se o verbo da frase principal e o verbo da frase que está sendo testada tem mais de 0.6 de semelhança
                                                    if palavra.palavra.lemma_ != palavraFraseTeste.palavra.lemma_:

                                                        # Verifica se a palavra está na lista de sinônimos
                                                        for sinonimo in listaDeSinonimos:

                                                            if sinonimo[
                                                                0].upper() in palavraFraseTeste.palavra.lemma_.upper():
                                                                continua = 1


                                                    else:
                                                        continua = 1

                                                    if continua == 0:
                                                        if palavra.palavra.lemma_.lower() in self.cbow_model.vocab and palavraFraseTeste.palavra.lemma_.lower() in self.cbow_model.vocab:
                                                            if self.cbow_model.similarity(palavra.palavra.lemma_.lower(),
                                                                                     palavraFraseTeste.palavra.lemma_.lower()) > 0.6 and self.cbow_model.similarity(
                                                                    palavra.palavra.text.lower(),
                                                                    palavraFraseTeste.palavra.text.lower()) > 0.6:
                                                                continua = 1

                                                    if continua == 1:

                                                        DemaisRelacoesCorretos = []
                                                        DemaisVerbosCorretos = []
                                                        SubstantivosCorretos = []

                                                        VerboPrincipalNegativo = 0
                                                        VerboTesteNegativo = 0

                                                        # Verifica se as polaridades dos verbos coicidem
                                                        for relacao in palavra.demaisRelacoes:
                                                            if relacao.pos_ == "ADV":
                                                                for tag in relacao.tag_:
                                                                    if tag[0][0][0] == "Polarity" and tag[0][0][
                                                                        1] == "Neg":
                                                                        VerboPrincipalNegativo = 1

                                                        for relacao in palavraFraseTeste.demaisRelacoes:
                                                            if relacao.pos_ == "ADV":
                                                                for tag in relacao.tag_:
                                                                    if tag[0][0][0] == "Polarity" and tag[0][0][
                                                                        1] == "Neg":
                                                                        VerboTesteNegativo = 1

                                                        # Verificando se o verbo que está sendo analisado é positivo ou negativo

                                                        if VerboPrincipalNegativo == VerboTesteNegativo:

                                                            verbo = Classes.VerboIgual(palavra.palavra)
                                                            # VERIFICAR O SUBSTANTIVO PRINCIPAL
                                                            for substantivoPrincipal_FrasePrincipal in palavra.substantivoPrincipal:

                                                                '''Verificar se existe e qual é o case do substantivo da frase principal.'''

                                                                for pesquisando_substantivo in con.conhecimentoMaster:
                                                                    if pesquisando_substantivo.palavra.i == substantivoPrincipal_FrasePrincipal.i:

                                                                        for substantivoPosterior in pesquisando_substantivo.substantivo:

                                                                            for pesquisando_substantivo_posterior in con.conhecimentoMaster:
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

                                                                        for pesquisando_substantivo in con2.conhecimentoMaster:
                                                                            if pesquisando_substantivo.palavra.i == substantivo.i:

                                                                                for substantivoPosterior in pesquisando_substantivo.substantivo:

                                                                                    for pesquisando_substantivo_posterior in con2.conhecimentoMaster:
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
                                                                                                substantivoComCase2[
                                                                                                    1].text):

                                                                                            verbo.substantivoPrincipal.append(
                                                                                                substantivoComCase1[2])

                                                                                            if jaAdicionouSubstantivo == 0:
                                                                                                substantivo = Classes.VerboIgual(
                                                                                                    substantivoComCase1[
                                                                                                        2])
                                                                                                substantivo.substantivo.append(
                                                                                                    substantivoComCase1[
                                                                                                        1])

                                                                                                substantivo2 = Classes.VerboIgual(
                                                                                                    substantivoComCase1[
                                                                                                        1])
                                                                                                substantivo2.demaisRelacoes.append(
                                                                                                    substantivoComCase1[
                                                                                                        0])

                                                                                                listaDeVerbos.append(
                                                                                                    substantivo)
                                                                                                listaDeVerbos.append(
                                                                                                    substantivo2)

                                                                                                ListaDeLigacoesCorretasTeste.append(
                                                                                                    palavraFraseTeste)

                                                                                                jaAdicionouSubstantivo = 1



                                                                                        elif str(substantivoComCase1[
                                                                                                     0].text) + " " + str(
                                                                                                substantivoComCase1[
                                                                                                    1].text) != str(
                                                                                                substantivoComCase2[
                                                                                                    0].text) + " " + str(
                                                                                                substantivoComCase2[
                                                                                                    1].text):
                                                                                            print(
                                                                                                "Não encontrou: " + str(
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

                                                                                                                                ListaDeLigacoesCorretasTeste.append(
                                                                                                                                    palavraFraseTeste)


                                                                                            else:

                                                                                                if substantivoTeste.pos_ == "NPROP" and substantivoPrincipal.pos_ == "NPROP":
                                                                                                    if substantivoTeste.text == substantivoPrincipal.text:
                                                                                                        verbo.substantivoPrincipal.append(
                                                                                                            substantivoTeste)

                                                                        existeCase2 = 0
                                                                    existeCase1 = 0

                                                            # VERIFICAR DEMAIS RELAÇÕES DO VERBO

                                                            for relacaoPrincipal in palavra.demaisRelacoes:
                                                                ListaDeDemaisRelacoesQueJaPassaram.append(
                                                                    relacaoPrincipal)

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
                                                                    DemaisRelacoesCorretos.append(relacaoTeste)
                                                                    ListaDeDemaisRelacoesQueJaPassaramTeste.append(
                                                                        relacaoTeste)

                                                            # VERIFICAR OS OUTROS VERBOS

                                                            for verboPrincipal in palavra.verbos:
                                                                ListaDeDemaisVerbosQueJaPassaram.append(verboPrincipal)

                                                            achouSinonimo = 0

                                                            for verboTeste in palavraFraseTeste.verbos:
                                                                listaDeSinonimos_ComparandoVerbos = self._ListarSinonimos(
                                                                    verboTeste.lemma_, cursor)
                                                                achouSinonimo = 0
                                                                for verboPrincipal in palavra.verbos:

                                                                    for sinonimo in listaDeSinonimos_ComparandoVerbos:

                                                                        if verboPrincipal.lemma_.upper() == sinonimo[
                                                                            0].upper():
                                                                            achouSinonimo = 1

                                                                    if achouSinonimo == 1:
                                                                        verbo.verbos.append(verboTeste)
                                                                        DemaisVerbosCorretos.append(verboTeste)
                                                                        ListaDeDemaisVerbosQueJaPassaramTeste.append(
                                                                            verboTeste)

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

                                                                                                        if len(
                                                                                                                palavra.substantivoPrincipal) == 0 and len(
                                                                                                                palavraFraseTeste.substantivoPrincipal) == 0:
                                                                                                            SubstantivosPosterioresSemPrincipalCorretos.append(
                                                                                                                substantivoPosteriorTeste)

                                                                                                        SubstantivosCorretos.append(
                                                                                                            substantivoPosteriorTeste)



                                                                    else:
                                                                        if substantivoPosteriorTeste.pos_ == "NPROP" and substantivoPosteriorPrincipal.pos_ == "NPROP":
                                                                            if substantivoPosteriorTeste.text == substantivoPosteriorPrincipal:
                                                                                verbo.substantivo.append(
                                                                                    substantivoPosteriorTeste)

                                                                                if len(
                                                                                        palavra.substantivoPrincipal) == 0 and len(
                                                                                        palavraFraseTeste.substantivoPrincipal) == 0:
                                                                                    SubstantivosPosterioresSemPrincipalCorretos.append(
                                                                                        substantivoPosteriorTeste)

                                                                                SubstantivosCorretos.append(
                                                                                    substantivoPosteriorTeste)

                                                            PVB = 0.6
                                                            PSP = 0.3
                                                            PDM = 0.1

                                                            if len(palavra.verbos) == 0:
                                                                VerbosPrincipalComPeso = 1
                                                            else:
                                                                VerbosPrincipalComPeso = len(palavra.verbos) * PVB

                                                            if len(palavra.substantivo) == 0:
                                                                SubstantivosPrincipalComPeso = 1
                                                            else:
                                                                SubstantivosPrincipalComPeso = len(
                                                                    palavra.substantivo) * PSP

                                                            if len(palavra.demaisRelacoes) == 0:
                                                                DemaisRelacoesPrincipalComPeso = 1
                                                            else:
                                                                DemaisRelacoesPrincipalComPeso = len(
                                                                    palavra.demaisRelacoes) * PDM

                                                            if len(palavra.verbos) == 0:
                                                                VerbosTesteComPeso = 1
                                                            else:
                                                                VerbosTesteComPeso = len(DemaisVerbosCorretos) * PVB

                                                            if len(palavra.substantivo) == 0:
                                                                SubstantivosTesteComPeso = 1
                                                            else:
                                                                SubstantivosTesteComPeso = len(
                                                                    SubstantivosCorretos) * PSP

                                                            if len(palavra.demaisRelacoes):
                                                                DemaisRelacoesTesteComPeso = 1
                                                            else:
                                                                DemaisRelacoesTesteComPeso = len(
                                                                    DemaisRelacoesCorretos) * PDM

                                                            total = VerbosPrincipalComPeso + SubstantivosPrincipalComPeso + DemaisRelacoesPrincipalComPeso
                                                            correto = VerbosTesteComPeso + SubstantivosTesteComPeso + DemaisRelacoesTesteComPeso

                                                            if correto < total:
                                                                verbo.semelhanca = correto * 100 / total
                                                            else:
                                                                verbo.semelhanca = total * 100 / correto

                                                            listaDeVerbos.append(verbo)
                                                            ListaDeVerbosQueJaPassaramTeste.append(verbo)

                                                        continua = 0

                                                    else:
                                                        palavrasNaoEncontradas.append(palavra.palavra)
                                                        listaDeVerbosNegativos.append(palavraFraseTeste.palavra)

            PesoAdjetivos = 0.4
            PesoVerbos = 0.6

            if palavra.palavra.pos_ == "NPROP" or palavra.palavra.pos_ == "N" or palavra.palavra.pos_ == "PROADJ" or palavra.palavra.pos_ == "PRO-KS" or palavra.palavra.pos_ == "PROPESS" or palavra.palavra.pos_ == "PRO-KS-REL" or palavra.palavra.pos_ == "PROSUB" and palavra.palavra.dep_ != "case":

                ListaDeSubstantivosQueJaPassaram.append(palavra)

                for palavraFraseTeste in con2.conhecimentoMaster:

                    substantivosIguais = 0
                    if palavraFraseTeste.palavra.pos_ == "NPROP" or palavraFraseTeste.palavra.pos_ == "N" or palavraFraseTeste.palavra.pos_ == "PROADJ" or palavraFraseTeste.palavra.pos_ == "PRO-KS" or palavraFraseTeste.palavra.pos_ == "PROPESS" or palavraFraseTeste.palavra.pos_ == "PRO-KS-REL" or palavraFraseTeste.palavra.pos_ == "PROSUB" and palavraFraseTeste.palavra.dep_ != "case":

                        if palavra.palavra.text.upper() != palavraFraseTeste.palavra.text.upper():

                            if palavra.palavra.pos_ != "NPROP" and palavraFraseTeste.palavra.pos_ != "NPROP":

                                if palavra.palavra.text.lower() != "":
                                    if palavraFraseTeste.palavra.text.lower() != "":
                                        if palavra.palavra.pos_ != "PUNCT":
                                            if palavraFraseTeste.palavra.pos_ != "PUNCT":
                                                if palavra.palavra.pos_ != "NUM":
                                                    if palavra.palavra.pos_ != "NUM":

                                                        if palavra.palavra.text.lower() in self.cbow_model.vocab and palavraFraseTeste.palavra.text.lower() in self.cbow_model.vocab:
                                                            if self.cbow_model.similarity(palavra.palavra.text.lower(),
                                                                                     palavraFraseTeste.palavra.text.lower()) > 0.6:
                                                                substantivosIguais = 1

                            else:

                                if palavra.palavra.text == palavraFraseTeste.palavra.text:
                                    substantivosIguais = 1

                        if palavra.palavra.text.upper() == palavraFraseTeste.palavra.text.upper():
                            substantivosIguais = 1

                        if substantivosIguais == 1:

                            VerbosCorretos = []
                            AdjetivosCorretos = []
                            Demais_RelacoesCorretos = []
                            Demais_VerbosCorretos = []

                            # Comparar os demais verbos
                            for VerboPrincipal_DemaisVerbos in palavra.verbos:

                                for VerboTeste_DemaisVerbos in palavraFraseTeste.verbos:

                                    if VerboPrincipal_DemaisVerbos.text.lower() != VerboTeste_DemaisVerbos.text.lower():

                                        Sinonimos_VerboPrincipal_DemaisVerbos = self._ListarSinonimos(
                                            VerboPrincipal_DemaisVerbos.lemma_, cursor)

                                        for Sinonimo_VerboPrincipal in Sinonimos_VerboPrincipal_DemaisVerbos:

                                            if VerboTeste_DemaisVerbos.text.lower() in Sinonimo_VerboPrincipal[
                                                0].lower():

                                                if VerboTeste_DemaisVerbos.text.lower() in self.cbow_model.vocab and VerboPrincipal_DemaisVerbos.text.lower() in self.cbow_model.vocab:
                                                    if self.cbow_model.similarity(VerboPrincipal_DemaisVerbos.text.lower(),
                                                                             VerboTeste_DemaisVerbos.text.lower()) > 0.6:

                                                        # Checar polaridades

                                                        PrincipalNeg = 0
                                                        TesteNeg = 0

                                                        for verboPrincipalPolaridade in con.conhecimentoMaster:
                                                            if VerboPrincipal_DemaisVerbos.palavra.i == verboPrincipalPolaridade.palavara.i:

                                                                for relacao in verboPrincipalPolaridade.demaisRelacoes:
                                                                    if relacao.pos_ == "ADV":
                                                                        for tag in relacao.tag_:
                                                                            if tag[0][0][0] == "Polarity" and tag[0][0][
                                                                                1] == "Neg":
                                                                                PrincipalNeg = 1

                                                        for verboTestePolaridade in con2.conhecimentoMaster:
                                                            if VerboTeste_DemaisVerbos.palavra.i == verboTestePolaridade.palavara.i:

                                                                for relacao in verboTestePolaridade.demaisRelacoes:
                                                                    if relacao.pos_ == "ADV":
                                                                        for tag in relacao.tag_:
                                                                            if tag[0][0][0] == "Polarity" and tag[0][0][
                                                                                1] == "Neg":
                                                                                TesteNeg = 1
                                                        # --------------------------------------

                                                        if PrincipalNeg == TesteNeg:
                                                            Demais_VerbosCorretos.append(VerboPrincipal_DemaisVerbos)



                                    else:
                                        Demais_VerbosCorretos.append(VerboPrincipal_DemaisVerbos)

                            # ---------------------------------------------------------------------------

                            # Comparar demais relaçṍes

                            for relacaoPrincipal in palavra.demaisRelacoes:

                                for relacaoTeste in palavraFraseTeste.demaisRelacoes:

                                    if relacaoPrincipal.text != relacaoTeste.text:

                                        if relacaoPrincipal.text.lower() in self.cbow_model.vocab and relacaoTeste.text.lower() in self.cbow_model.vocab:
                                            if self.cbow_model.similarity(relacaoPrincipal.text.lower(),
                                                                     relacaoTeste.text.lower()) > 0.5:
                                                Demais_RelacoesCorretos.append(relacaoPrincipal)

                            # ---------------------------------------------------------------------------

                            # Comparar os adjetivos
                            achouAdjetivo = 0

                            if len(palavra.adjetivos) > 0 and len(palavraFraseTeste.adjetivos) > 0:

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
                                                                        if self.cbow_model.similarity(
                                                                                adjetivoPrincipal.text.lower(),
                                                                                adjetivoTeste.text.lower()) > 0.64:
                                                                            AdjetivosCorretos.append(adjetivoTeste)
                                            else:
                                                AdjetivosCorretos.append(adjetivoTeste)
                            # ---------------------------------------------------------------------------

                            # Comparação se existem verbos ligados diretamente ao substantivo
                            listaDeVerbosPrincipal = []
                            listaDeVerbosTeste = []

                            for verboUtilizado in con.conhecimentoMaster:

                                if verboUtilizado.palavra.pos_ == "V" or verboUtilizado.palavra.pos_ == "VAUX" or verboUtilizado.palavra.pos_ == "VERB":

                                    if len(verboUtilizado.substantivoPrincipal) > 0:

                                        if verboUtilizado.substantivoPrincipal[0].i == palavra.palavra.i:
                                            listaDeVerbosPrincipal.append(verboUtilizado)

                            for verboUtilizado in con2.conhecimentoMaster:
                                if verboUtilizado.palavra.pos_ == "V" or verboUtilizado.palavra.pos_ == "VAUX" or verboUtilizado.palavra.pos_ == "VERB":

                                    if len(verboUtilizado.substantivoPrincipal) > 0:

                                        if verboUtilizado.substantivoPrincipal[0].i == palavraFraseTeste.palavra.i:
                                            listaDeVerbosTeste.append(verboUtilizado)

                            for verboP in listaDeVerbosPrincipal:

                                PrincipalNeg = 0

                                acao = 0

                                for relacao in verboP.demaisRelacoes:
                                    if relacao.pos_ == "ADV":
                                        for tag in relacao.tag_:
                                            if tag[0][0][0] == "Polarity" and tag[0][0][1] == "Neg":
                                                PrincipalNeg = 1

                                for verboT in listaDeVerbosTeste:

                                    TesteNeg = 0

                                    for relacao in verboT.demaisRelacoes:
                                        if relacao.pos_ == "ADV":
                                            for tag in relacao.tag_:
                                                if tag[0][0][0] == "Polarity" and tag[0][0][1] == "Neg":
                                                    TesteNeg = 1

                                    # Comparar polaridades
                                    if PrincipalNeg == TesteNeg:

                                        SinVerboP = self._ListarSinonimos(verboP.palavra.lemma_, cursor)

                                        if verboP.palavra.text.upper() != verboT.palavra.text.upper():

                                            for sinonimoVp in SinVerboP:

                                                if sinonimoVp[0].upper() == verboT.palavra.text.upper():

                                                    if verboP.palavra.text.lower() in self.cbow_model.vocab and verboT.apavra.text.lower() in self.cbow_model.bocab:
                                                        if self.cbow_model.similarity(verboP.palavra.text.lower(),
                                                                                 verboT.palavra.text.lower()) > 0.5:
                                                            achouVerbo = 1
                                                            VerbosCorretos.append(verboT.palavra)

                                        else:
                                            VerbosCorretos.append(verboT.palavra)

                            achouVerboEmResultado = 0
                            # ---------------------------------------------------------------------------

                            # Verificar se os substantivos são realmente iguais
                            if len(VerbosCorretos) >= math.ceil(len(listaDeVerbosPrincipal) * PesoVerbos) and len(
                                    AdjetivosCorretos) >= math.ceil(len(palavra.adjetivos) * PesoAdjetivos):
                                PVB = 0.6
                                PAJ = 0.4
                                PDR = 0.1
                                PDV = 0.1

                                verbo = Classes.VerboIgual(palavraFraseTeste.palavra)
                                verbo.demaisRelacoes = palavraFraseTeste.demaisRelacoes
                                verbo.substantivo = palavraFraseTeste.substantivo
                                verbo.substantivoPrincipal = palavraFraseTeste.substantivoPrincipal

                                for verb in VerbosCorretos:
                                    verbo.verbos.append(verb)

                                for adj in AdjetivosCorretos:
                                    verbo.adjetivos.append(adj)

                                for vb in listaDeVerbos:

                                    if vb.palavra.i == verbo.palavra.i:
                                        listaDeVerbos.remove(vb)

                                if len(listaDeVerbosPrincipal) == 0 and len(palavra.adjetivos) == 0 and len(
                                        palavra.demaisRelacoes) == 0 and len(palavra.verbos) == 0:
                                    verbo.semelhanca = 100

                                else:

                                    if len(palavra.adjetivos) == 0:
                                        AdjetivoPrincipalComPeso = 1
                                    else:
                                        AdjetivoPrincipalComPeso = PAJ * len(palavra.adjetivos)

                                    if len(listaDeVerbosPrincipal) == 0:
                                        VerbosPrincipalComPeso = 1
                                    else:
                                        VerbosPrincipalComPeso = PVB * len(palavra.verbos)

                                    if len(palavra.demaisRelacoes) == 0:
                                        DemaisRelacoesPrincipalComPeso = 1
                                    else:
                                        DemaisRelacoesPrincipalComPeso = PDR * len(palavra.demaisRelacoes)

                                    if len(palavra.verbos) == 0:
                                        DemaisVerbosPrincipalComPeso = 1
                                    else:
                                        DemaisVerbosPrincipalComPeso = PDV * len(palavra.verbos)

                                    total = AdjetivoPrincipalComPeso + VerbosPrincipalComPeso + DemaisRelacoesPrincipalComPeso + DemaisVerbosPrincipalComPeso

                                    if len(palavra.adjetivos) == 0:
                                        AdjetivoComPeso = 1
                                    else:
                                        AdjetivoComPeso = PAJ * len(AdjetivosCorretos)

                                    if len(listaDeVerbosPrincipal) == 0:
                                        VerbosComPeso = 1
                                    else:
                                        VerbosComPeso = PVB * len(VerbosCorretos)

                                    if len(palavra.demaisRelacoes) == 0:
                                        DemaisRelacoesComPeso = 1
                                    else:
                                        DemaisRelacoesComPeso = PDR * len(Demais_RelacoesCorretos)

                                    if len(palavra.verbos) == 0:
                                        DemaisVerbosComPeso = 1
                                    else:
                                        DemaisVerbosComPeso = PDV * len(Demais_VerbosCorretos)

                                    correto = AdjetivoComPeso + VerbosComPeso + DemaisRelacoesComPeso + DemaisVerbosComPeso

                                    verbo.semelhanca = correto * 100 / total

                                    '''
                                    print("Correto: ",correto," | Total: ",total," | Semelhança: ",verbo.semelhanca)
                                    print("\n")
                                    '''

                                    listaDeVerbos.append(verbo)

                                    ListaDeSubstantivosQueJaPassaramTeste.append(verbo)
                            else:

                                palavrasNaoEncontradas.append(palavra.palavra)

                            # ---------------------------------------------------------------------------

            # Removendo relações com verbos que tem polaridade diferentes
            for verboNegativo in listaDeVerbosNegativos:

                for palavra in listaDeVerbos:

                    for dr in palavra.demaisRelacoes:

                        if dr.i == verboNegativo.i:
                            palavra.demaisRelacoes.remove(dr)

                    for vb in palavra.verbos:

                        if vb.i == verboNegativo.i:
                            palavra.verbos.remove(vb)

            comRelacionamento = 0
            for palavra in listaDeVerbos:

                if len(palavra.demaisRelacoes) == 0 and len(palavra.substantivo) == 0 and len(
                        palavra.substantivoPrincipal) == 0 and len(palavra.verbos) == 0 and len(palavra.adjetivos) == 0:

                    for palavra2 in listaDeVerbos:

                        if palavra2.palavra.i != palavra.palavra.i:

                            for dr in palavra2.demaisRelacoes:
                                if dr.i == palavra.palavra.i:
                                    comRelacionamento = 1

                            for sb in palavra2.substantivo:
                                if sb.i == palavra.palavra.i:
                                    comRelacionamento = 1

                            for sbp in palavra2.substantivoPrincipal:
                                if sbp.i == palavra.palavra.i:
                                    comRelacionamento = 1

                            for vb in palavra2.verbos:
                                if vb.i == palavra.palavra.i:
                                    comRelacionamento = 1

                            for adj in palavra2.adjetivos:
                                if adj.i == palavra.palavra.i:
                                    comRelacionamento == 1

                    if comRelacionamento == 0:
                        listaDeVerbos.remove(palavra)

            # ---------------------------------------------------------------------------

        PesoVerbos = 0.2
        PesoSubstantivos = 0.1
        VerbosComSubstantivosCorretos = 0.294
        PesoCertezas = 0.42
        PesoSubstantivosSemPrincipais = 0.42

        VerboOriginal = len(ListaDeVerbosQueJaPassaram)
        VerboTeste = len(ListaDeVerbosQueJaPassaramTeste)
        SubstantivoOriginal = len(ListaDeSubstantivosQueJaPassaram)
        SubstantivoTeste = len(ListaDeSubstantivosQueJaPassaramTeste)
        VerboComSubstantivoOriginal = len(ListaDeLigacoesCorretas)
        VerboComSubstantivoTeste = len(ListaDeLigacoesCorretasTeste)
        CertezasUnica = len(Certezas)
        SubstantivoSemPrincipal = len(SubstantivosPosterioresSemPrincipalCorretos)

        if VerboTeste > VerboOriginal:
            VerboTeste = VerboOriginal

        if SubstantivoTeste > SubstantivoOriginal:
            SubstantivoTeste = SubstantivoOriginal

        if VerboComSubstantivoTeste > VerboComSubstantivoOriginal:
            VerboComSubstantivoTeste = VerboComSubstantivoOriginal

        TotalOriginal = (SubstantivoOriginal * PesoSubstantivos) + (VerboOriginal * PesoVerbos) + (
                    VerboComSubstantivoOriginal * VerbosComSubstantivosCorretos)

        TotalCorretos = (SubstantivoTeste * PesoSubstantivos) + (VerboTeste * PesoVerbos) + (
                    VerboComSubstantivoTeste * VerbosComSubstantivosCorretos) + (len(Certezas) * PesoCertezas) + (
                                    len(SubstantivosPosterioresSemPrincipalCorretos) * PesoSubstantivosSemPrincipais)

        if TotalOriginal > TotalCorretos:
            Semelhanca = TotalCorretos * 100 / TotalOriginal

        else:
            Semelhanca = TotalOriginal * 100 / TotalCorretos

        '''
        print("Original")
        print(TotalOriginal)
        print("\n\n")
        print("Correção")
        print(TotalCorretos)
        print("\n\n")
        print(len(ListaDeSubstantivosQueJaPassaramTeste))
        print("-------------------------")
        '''

        self.semelhanca = Semelhanca


        '''
        print("Demais verbos que já passaram")
        print("Original ", len(ListaDeDemaisVerbosQueJaPassaram))
        print("Teste ", len(ListaDeDemaisVerbosQueJaPassaramTeste))
        print("\n")
        print("Demais relações que já passaram")
        print("Original ", len(ListaDeDemaisRelacoesQueJaPassaram))
        print("Teste ", len(ListaDeDemaisRelacoesQueJaPassaramTeste))
        print("\n")
        print("Ligações corretas")
        print("Original ", len(ListaDeLigacoesCorretas))
        print("Teste ", len(ListaDeLigacoesCorretasTeste))
        print("\n")
        print("Verbos")
        print("Original ", VerboTeste)
        print("Teste ", VerboOriginal)
        print("\n")
        print("Substantivos")
        print(SubstantivoOriginal)
        print(SubstantivoTeste)

        print("Substantivos sem substantivo principal")
        print(len(SubstantivosPosterioresSemPrincipalCorretos))
        print("\n")
        print("-------------------------")
        '''
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