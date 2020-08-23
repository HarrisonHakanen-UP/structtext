'''Spacy'''
import spacy
import string

from pyparsing import LineStart

nlpPor = spacy.load("pt_core_news_lg")
from Model import Classes
import networkx as nx
import matplotlib.pyplot as plt


'''NLPNET'''
import nlpnet
nlpnet.set_data_dir('../NLPNET')
tagger = nlpnet.POSTagger()


'''Stanza'''
import stanza
nlp = stanza.Pipeline(lang='pt', processors='tokenize,mwt,pos,lemma,depparse')


class Projeto:
    def __init__(self, f):
        self.frase = f
        self.conhecimentoMaster = self._ConhecimentoCalibrado()

    def RetornarConhecimento(self):
        return self.conhecimentoMaster


    def ImprimirConhecimento(self):
        conhecimento = self.conhecimentoMaster

        for palavra in conhecimento:
            print("Palavra: ", palavra.palavra.text, "-", palavra.palavra.i, "-", palavra.palavra.pos_)

            print(
                f"{'Substantivo principal: '}{[substanP.text for substanP in palavra.substantivoPrincipal]}{[substanP.i for substanP in palavra.substantivoPrincipal]}")

            print(f"{'Substantivo posterior: '}{[substan.text for substan in palavra.substantivo]}")

            print(f"{'Demais verbos: '}{[verb.text for verb in palavra.verbos]}")

            print(f"{'Adjetivos: '}{[adj.text for adj in palavra.adjetivos]}")

            print(f"{'Demais relações: '}{[demaisR.text for demaisR in palavra.demaisRelacoes]}")

            print("--------------------------")
            print("\n")
            print("\n")


    def _RemoverPontuacao(self,texto):
        Contador = 0

        Frase_Filtrada = []

        for i in texto:
            for punc in string.punctuation:
                if i == punc:
                    Contador = 1

                    break
            if Contador == 0:
                Frase_Filtrada.append(i)
            Contador = 0
        textoFiltrado = ''.join(Frase_Filtrada)

        return textoFiltrado


    def _TratarTag(self,texto):
        listaDeTags = []
        tagSplit = texto.split("|")

        tagPrimeiraPosicao = tagSplit[0].split("__")

        if len(tagPrimeiraPosicao) == 2:
            tagSplit[0] = tagPrimeiraPosicao[1]

        for tag in tagSplit:

            tagDefinitiva = []
            tagMaster = tag.split("=")

            for tagM in tagMaster:
                tagDefinitiva.append(self._RemoverPontuacao(tagM))

            listaDeTags.append(tagDefinitiva)

        return listaDeTags


    def _ExtrairConhecimento(self,frase):
        vemAntes = 0

        passou = 0

        substantivoP = Classes.TokenAux("kk")

        achouAntes = 0

        achouDepois = 0

        listaDePalavras = []

        existeCase = 0

        fraseAnalisada = frase

        for indexFrase in range(len(fraseAnalisada)):

            tokenAux = Classes.TokenAux(fraseAnalisada[indexFrase].text)
            tokenAux.pos_ = fraseAnalisada[indexFrase].pos_
            tokenAux.i = fraseAnalisada[indexFrase].i
            tokenAux.dep_ = fraseAnalisada[indexFrase].dep_
            tokenAux.lemma_ = fraseAnalisada[indexFrase].lemma_

            tokenAux.tag_.append(fraseAnalisada[indexFrase].tag_)

            tokenAux.tag_.append(fraseAnalisada[indexFrase].tag_)

            if fraseAnalisada[indexFrase].pos_ == "V" or fraseAnalisada[indexFrase].pos_ == "VAUX" or fraseAnalisada[
                indexFrase].pos_ == "PCP":

                verbo = Classes.Palavra(tokenAux)

                for children in fraseAnalisada[indexFrase].filhos:

                    childrenAux = Classes.TokenAux(children.text)
                    childrenAux.pos_ = children.pos_
                    childrenAux.i = children.i
                    childrenAux.dep_ = children.dep_
                    childrenAux.lemma_ = children.lemma_
                    childrenAux.tag_.append(children.tag_)

                    if children.pos_ == "N" or children.pos_ == "NPROP" or children.pos_ == "PROADJ" or children.pos_ == "PRO-KS" or children.pos_ == "PROPESS" or children.pos_ == "PRO-KS-REL" or children.pos_ == "PROSUB":

                        if children.dep_ != "case":

                            if children.i < tokenAux.i:
                                substantivoP = childrenAux
                                verbo.substantivoPrincipal.append(childrenAux)
                                achouAntes = 1

                            else:
                                verbo.substantivo.append(childrenAux)



                    elif children.pos_ == "V" or children.pos_ == "VAUX" or children.pos_ == "PCP":
                        verbo.verbos.append(childrenAux)

                    elif children.pos_ == "ADJ":
                        verbo.adjetivos.append(childrenAux)

                    else:
                        verbo.demaisRelacoes.append(childrenAux)

                    achouAntes = 0
                    achouDepois = 0

                if len(verbo.substantivoPrincipal) == 0 and substantivoP.text != "kk":
                    verbo.substantivoPrincipal.append(substantivoP)

                listaDePalavras.append(verbo)

            if fraseAnalisada[indexFrase].pos_ == "ADJ" or fraseAnalisada[indexFrase].pos_ == "ADV":
                adjetivo = Classes.Palavra(tokenAux)

                '''
                if fraseAnalisada[indexFrase].text == "bonito":
                    print(f"{[child.text for child in fraseAnalisada[indexFrase].filhos]}")
                '''

                for children in fraseAnalisada[indexFrase].filhos:

                    childrenAux = Classes.TokenAux(children.text)
                    childrenAux.pos_ = children.pos_
                    childrenAux.i = children.i
                    childrenAux.dep_ = children.dep_
                    childrenAux.lemma_ = children.lemma_
                    childrenAux.tag_.append(children.tag_)

                    if children.pos_ == "N" or children.pos_ == "NPROP" or children.pos_ == "PROADJ" or children.pos_ == "PRO-KS" or children.pos_ == "PROPESS" or children.pos_ == "PRO-KS-REL" or children.pos_ == "PROSUB":

                        adjetivo.substantivo.append(childrenAux)

                    elif children.pos_ == "VERB" or children.pos_ == "VAUX" or children.pos_ == "PCP":
                        adjetivo.verbos.append(childrenAux)

                    else:
                        adjetivo.demaisRelacoes.append(childrenAux)

                listaDePalavras.append(adjetivo)

            if fraseAnalisada[indexFrase].pos_ == "N" or fraseAnalisada[indexFrase].pos_ == "NPROP" or fraseAnalisada[
                indexFrase].pos_ == "PROADJ" or fraseAnalisada[indexFrase].pos_ == "PRO-KS" or fraseAnalisada[
                indexFrase].pos_ == "PROPESS" or fraseAnalisada[indexFrase].pos_ == "PRO-KS-REL" or fraseAnalisada[
                indexFrase].pos_ == "PROSUB" and fraseAnalisada[indexFrase].dep_ != "case":

                substantivo = Classes.Palavra(tokenAux)

                for children in fraseAnalisada[indexFrase].filhos:

                    childrenAux = Classes.TokenAux(children.text)
                    childrenAux.pos_ = children.pos_
                    childrenAux.i = children.i
                    childrenAux.dep_ = children.dep_
                    childrenAux.lemma_ = children.lemma_
                    childrenAux.tag_.append(children.tag_)

                    if children.pos_ == "V" or children.pos_ == "VAUX" or children.pos_ == "PCP":
                        substantivo.verbos.append(childrenAux)

                    elif children.pos_ == "N" or children.pos_ == "NPROP" or children.pos_ == "PROADJ" or children.pos_ == "PRO-KS" or children.pos_ == "PROPESS" or children.pos_ == "PRO-KS-REL" or children.pos_ == "PROSUB":
                        if children.dep_ != "case":

                            for child2 in children.filhos:

                                childrenAux2 = Classes.TokenAux(child2.text)
                                childrenAux2.pos_ = child2.pos_
                                childrenAux2.i = child2.i
                                childrenAux2.dep_ = child2.dep_
                                childrenAux2.lemma_ = child2.lemma_
                                childrenAux2.tag_.append(child2.tag_)

                                # print(childrenAux2.pos_)

                                if child2.dep_ == "case":
                                    word = Classes.Palavra(childrenAux2)
                                    word.substantivoPrincipal.append(tokenAux)
                                    word.substantivo.append(childrenAux)

                                    listaDePalavras.append(word)
                                    existeCase = 1

                            if existeCase == 0:
                                substantivo.substantivo.append(childrenAux)

                    else:
                        substantivo.demaisRelacoes.append(childrenAux)

                listaDePalavras.append(substantivo)

        return listaDePalavras


    def _RecalibarConhecimento(self,fraseTeste4, conhecimento):
        verbos = 0

        listaDePalavras = ""
        listaDeToken = []

        achou = 0

        ciclo = 1

        for token in fraseTeste4:

            if token.pos_ == "V" or token.pos_ == "VAUX" or token.pos_ == "PCP":
                verbos += 1

            if token.i == len(fraseTeste4) - 1:

                if token.i + 1 < len(fraseTeste4):
                    if fraseTeste4[token.i + 1].pos_ == "PU":
                        listaDePalavras += token.text
                    else:
                        listaDePalavras += token.text + " "
                else:
                    listaDePalavras += token.text

                t = Classes.TokenAux(token.text)
                t.i = token.i
                t.pos_ = token.pos_
                t.dep_ = token.dep_
                t.lemma_ = token.lemma_
                t.tag_.append(token.tag_)
                listaDeToken.append(t)

            if verbos != 2 and token.i != len(fraseTeste4) - 1:
                if fraseTeste4[token.i + 1].pos_ == "PU":
                    listaDePalavras += token.text
                else:
                    listaDePalavras += token.text + " "

                t = Classes.TokenAux(token.text)
                t.i = token.i
                t.pos_ = token.pos_
                t.dep_ = token.dep_
                t.lemma_ = token.lemma_
                t.tag_.append(token.tag_)
                listaDeToken.append(t)



            else:
                listaDePalavras = listaDePalavras.strip()
                listaDePalavras = nlpPor(listaDePalavras)

                for palavraNova in listaDePalavras:

                    for tok in listaDeToken:
                        if palavraNova.text == tok.text:
                            for ch in palavraNova.children:

                                chAux = Classes.TokenAux(ch.text)

                                for tok2 in listaDeToken:
                                    if chAux.text == tok2.text:
                                        chAux.i = tok2.i
                                        break

                                chAux.pos_ = ch.pos_
                                chAux.dep_ = ch.dep_
                                chAux.lemma_ = ch.lemma_
                                chAux.tag_.append(ch.tag_)

                                tok.filhos.append(chAux)

                for palavra in listaDeToken:

                    if palavra.pos_ == "V" or palavra.pos_ == "AUX" or palavra.pos_ == "PCP":

                        for con in conhecimento:

                            if con.palavra.text == palavra.text:
                                for children in palavra.filhos:

                                    if children.pos_ == "V" or children.pos_ == "VAUX" or children.pos_ == "PCP":

                                        for verbo in con.verbos:
                                            if verbo.text == children.text:
                                                achou = 1

                                        if achou == 0:
                                            con.verbos.append(children)

                                        achou = 0

                                    elif children.pos_ == "ADJ":

                                        for adj in con.adjetivos:
                                            if adj.text == children.text:
                                                achou = 1

                                        if achou == 0:
                                            con.adjetivos.append(children)

                                        achou = 0

                                    elif children.pos_ == "N" or children.pos_ == "NPROP" or children.pos_ == "PROADJ" or children.pos_ == "PRO-KS" or children.pos_ == "PROPESS" or children.pos_ == "PRO-KS-REL" or children.pos_ == "PROSUB":

                                        if palavra.i < children.i:

                                            for sub in con.substantivo:
                                                if sub.text == children.text:
                                                    achou = 1

                                            if achou == 0:
                                                con.substantivo.append(children)

                                            achou = 0

                                        else:

                                            if len(con.substantivoPrincipal) <= 0:
                                                con.substantivoPrincipal.append(children)

                verbos = 0
                listaDePalavras = ""
                listaDeToken = []
                t = Classes.TokenAux(token.text)
                t.i = token.i
                t.pos_ = token.pos_
                t.dep_ = token.dep_
                t.lemma_ = token.lemma_
                t.tag_.append(token.tag_)

                t.filhos = token.filhos
                listaDeToken.append(t)

                if token.i + 1 < len(fraseTeste4):
                    if fraseTeste4[token.i + 1].pos_ == "PU":
                        listaDePalavras += token.text
                    else:
                        listaDePalavras += token.text + " "

            ciclo += 1
        return conhecimento


    def _RemoverLigacoes(self,con):
        ListaDeVerbos = []

        for conhecimento in con:
            if conhecimento.palavra.pos_ == "V" or conhecimento.palavra.pos_ == "VAUX" or conhecimento.palavra.pos_ == "PCP":
                ListaDeVerbos.append(conhecimento)

        for verbo in ListaDeVerbos:
            for D_verbo in verbo.verbos:
                for palavra in con:
                    if D_verbo.i == palavra.palavra.i:
                        if len(verbo.substantivoPrincipal) > 0 and len(palavra.substantivoPrincipal) > 0:
                            if verbo.substantivoPrincipal[0].i != palavra.substantivoPrincipal[0].i:
                                verbo.verbos.remove(D_verbo)

        return con


    def _AjustarCases(self,con):
        for objeto in con:
            if objeto.palavra.pos_ == "N" or objeto.palavra.pos_ == "NPROP" or objeto.palavra.pos_ == "PROADJ" or objeto.palavra.pos_ == "PRO-KS" or objeto.palavra.pos_ == "PROPESS" or objeto.palavra.pos_ == "PRO-KS-REL" or objeto.palavra.pos_ == "PROSUB":

                for substantivoPesquisado in objeto.substantivo:

                    for objeto2 in con:

                        if substantivoPesquisado.text == objeto2.palavra.text and substantivoPesquisado.i == objeto2.palavra.i:

                            for case in objeto2.demaisRelacoes:
                                palavra = Classes.Palavra(case)
                                palavra.substantivoPrincipal.append(objeto.palavra)
                                palavra.substantivo.append(objeto2.palavra)
                                con.append(palavra)

        return con

    def _RemoverCasesDuplicados(self, con):
        for conhecimento in con:
            if conhecimento.palavra.dep_ == "case":

                for case in con:
                    if case.palavra.dep_ == "case":

                        if conhecimento.palavra.i != case.palavra.i:

                            if len(conhecimento.substantivoPrincipal) > 0 and len(case.substantivoPrincipal) > 0 and len(
                                    conhecimento.substantivo) > 0 and len(case.substantivo) > 0:
                                if conhecimento.palavra.text == case.palavra.text and conhecimento.substantivoPrincipal[
                                    0].text == \
                                        case.substantivoPrincipal[0].text and conhecimento.substantivo[0].text == \
                                        case.substantivo[
                                            0].text:


                                    voltar = 0

                                    for Index_palavra in range(len(con)):

                                        if Index_palavra == len(con):
                                            break

                                        for v in range(voltar):
                                            Index_palavra -=1
                                            voltar-=1

                                        print(con[Index_palavra].palavra.text)
                                        if con[Index_palavra].palavra.pos_ == "V" or con[Index_palavra].palavra.pos_ == "VAUX":


                                            for sub in con[Index_palavra].substantivoPrincipal:

                                                if sub.i == conhecimento.substantivoPrincipal[0].i:
                                                    con[Index_palavra].substantivoPrincipal[0] = case.substantivoPrincipal[0]

                                                    for substantivoPrincipal in conhecimento.substantivoPrincipal:

                                                        for conhecimento2 in con:

                                                            if substantivoPrincipal.i == conhecimento2.palavra.i:
                                                                con.remove(conhecimento2)
                                                                voltar+=1
                                                                break

                                                    for substantivo in conhecimento.substantivo:

                                                        for conhecimento2 in con:

                                                            if substantivo.i == conhecimento2.palavra.i:
                                                                con.remove(conhecimento2)
                                                                voltar+=1
                                                                break

                                                    if voltar != 0:
                                                        con.remove(conhecimento)


        return con



    def _SubstituirPOS(self,frase):
        fraseSpacy = nlpPor(frase)
        fraseNlpNet = tagger.tag(frase)

        ListaDeTokensAuxiliares = []

        ListaDeTokensDefinitiva = []

        for tokenSpacy in fraseSpacy:
            tokenAuxiliar = Classes.TokenAux(tokenSpacy.text)
            tokenAuxiliar.i = tokenSpacy.i
            tokenAuxiliar.dep_ = tokenSpacy.dep_
            tokenAuxiliar.tag_.append(self._TratarTag(str(tokenSpacy.tag_)))

            ListaDeTokensAuxiliares.append(tokenAuxiliar)

        index = 0
        for indexNlpNet in range(len(fraseNlpNet)):

            for indexPalavraNlpNet in range(len(fraseNlpNet[indexNlpNet])):
                ListaDeTokensAuxiliares[index].pos_ = fraseNlpNet[indexNlpNet][indexPalavraNlpNet][1]
                index += 1

        for tokenSpacy in fraseSpacy:

            for tokenAux in ListaDeTokensAuxiliares:
                if tokenAux.i == tokenSpacy.i:

                    for children in tokenSpacy.children:

                        for childrenEmTokensAuxiliares in ListaDeTokensAuxiliares:

                            if children.i == childrenEmTokensAuxiliares.i:
                                childAux = Classes.TokenAux(children.text)
                                childAux.pos_ = childrenEmTokensAuxiliares.pos_
                                childAux.i = children.i
                                childAux.dep_ = children.dep_
                                childAux.tag_.append(self._TratarTag(str(children.tag_)))
                                tokenAux.filhos.append(childAux)

                    break

            ListaDeTokensDefinitiva.append(tokenAux)
        return ListaDeTokensDefinitiva

    def _CompletarPOS_NER(self,filho,frase):
        spacyTokens = nlpPor(frase)
        tokenF = []
        tokenT = []
        contF = 0
        contT = 0


        for token in spacyTokens:
            if token.i == filho.i:

                if token.text == filho.text:

                    filho.pos_ = token.pos_
                    filho.dep_ = token.dep_
                    filho.lemma_ = token.lemma_
                    filho.tag_ = token.tag_
                    break

                else:
                    for tokenFrente in range(len(spacyTokens)):
                        if spacyTokens[tokenFrente].text == filho.text:
                            tokenF.append(spacyTokens[tokenFrente])
                            break
                        contF += 1

                    for tokenTras in range(len(spacyTokens)):
                        if spacyTokens[-(tokenTras+1)].text == filho.text:
                            tokenT.append(spacyTokens[-(tokenTras+1)])
                            break
                        contT +=1


                    if contF<contT and contF != 0:
                        filho.i = tokenF[0].i
                        filho.pos_ = tokenF[0].pos_
                        filho.dep_ = tokenF[0].dep_
                        filho.lemma_ = tokenF[0].lemma_
                        filho.tag_ = tokenF[0].tag_

                    if contT < contF and contT != 0:
                        filho.i = tokenT[0].i
                        filho.pos_ = tokenT[0].pos_
                        filho.dep_ = tokenT[0].dep_
                        filho.lemma_ = tokenT[0].lemma_
                        filho.tag_ = tokenT[0].tag_


    def _StanfordDependencyParsing(self,frase):
        listaDePalavras = []
        filhos = []
        palavrasQueJaPassaram = []

        header = ""
        idAtual = 0

        fraseStanford = nlp(frase)

        for sent in fraseStanford.sentences:
            for word in sent.words:

                if sent.words[word.head - 1].text + sent.words[word.head - 1].id not in palavrasQueJaPassaram:

                    palavra = Classes.TokenAux(sent.words[word.head - 1].text)

                    filhoAux = Classes.TokenAux(word.text)
                    filhoAux.i = int(word.id) - 1
                    '''Arrumar para que os filhos também tenham tagger e pos'''


                    palavra.filhos.append(filhoAux)

                    palavra.i = int(sent.words[word.head - 1].id) - 1

                    header = sent.words[word.head - 1].text

                    for sent2 in fraseStanford.sentences:
                        for word2 in sent2.words:

                            if word.id != word2.id and sent.words[word.head - 1].text == sent2.words[
                                word2.head - 1].text and sent.words[word.head - 1].id == sent2.words[word2.head - 1].id:
                                filhoAux2 = Classes.TokenAux(word2.text)
                                filhoAux2.i = int(word2.id) - 1
                                '''Arrumar para que os filhos também tenham tagger e pos'''

                                self._CompletarPOS_NER(filhoAux2,frase)

                                palavra.filhos.append(filhoAux2)

                    palavrasQueJaPassaram.append(sent.words[word.head - 1].text + sent.words[word.head - 1].id)

                    listaDePalavras.append(palavra)

        return listaDePalavras


    def _MesclarDependencias(self,ListaSpacy, ListaStanford):
        existe = 0

        for stanford in ListaStanford:
            for spacy in ListaSpacy:

                if stanford.i == spacy.i and stanford.text == spacy.text:

                    for stanFilho in stanford.filhos:

                        for spacyFilho in spacy.filhos:

                            if stanFilho.i == spacyFilho.i:
                                existe = 1
                                break

                        if existe == 0:
                            spacy.filhos.append(stanFilho)

                        existe = 0
        '''
        print("\n\n")
        print("Final")
        for token in ListaSpacy:
            print(token.text)
            print(f"{[child.text for child in token.filhos]}")
        '''
        return ListaSpacy


    def _ConverterTokenEmEntidade(self,frase, ListaDeTokens):

        listaDeId = []
        for ent in nlpPor(frase).ents:

            primeiro = 0

            listTokensEntidade = []

            entidade = Classes.TokenAux(ent.text)

            entidadeSplit = ent.text.split()

            if len(entidadeSplit) > 1:
                for entSplit in entidadeSplit:

                    for token in ListaDeTokens:

                        if entSplit == token.text:
                            if token.i not in listaDeId:

                                if primeiro == 0:
                                    entidade.tag_.append(token.tag_)
                                    entidade.pos_ = token.pos_
                                    entidade.i = token.i
                                    primeiro = 1

                                for filho in token.filhos:

                                    igual = 0

                                    for entSplit2 in entidadeSplit:

                                        if filho.text == entSplit2:
                                            igual = 1
                                            break

                                    if igual != 1:
                                        entidade.filhos.append(filho)

                                    igual = 0

                                for token2 in ListaDeTokens:

                                    for filho2 in token2.filhos:

                                        if filho2.i == token.i:
                                            token2.filhos.append(entidade)
                                            token2.filhos.remove(filho2)

                                ListaDeTokens.remove(token)
                                listaDeId.append(token.i)
                                break

                ListaDeTokens.append(entidade)

                primeiro = 0

            else:

                for token in ListaDeTokens:
                    if token.text == entidadeSplit[0]:
                        listaDeId.append(token.i)
                        break

        return ListaDeTokens


    def _RemoverPontuacoes(self,ListaDeTokens):
        for token in ListaDeTokens:
            for filho in token.filhos:
                if filho.pos_ == "PU":
                    token.filhos.remove(filho)

        return ListaDeTokens

    def _ConhecimentoCalibrado(self):

        frase = self.frase

        ListaDeTokensDefinitiva = self._SubstituirPOS(frase)

        ListaDeTokensStanford = self._StanfordDependencyParsing(frase)

        ListaFinal = self._MesclarDependencias(ListaDeTokensDefinitiva, ListaDeTokensStanford)

        ListaFinal = self._RemoverPontuacoes(ListaFinal)

        ListaFinal = self._ConverterTokenEmEntidade(frase, ListaFinal)

        con = self._ExtrairConhecimento(ListaFinal)

        con = self._RemoverLigacoes(con)

        con = self._AjustarCases(con)

        con = self._RemoverCasesDuplicados(con)

        return con


    def _AdicionarNosNoGrafo(self,conhecimento, G):
        for objeto in conhecimento:
            txt = objeto.palavra.text + "_" + str(objeto.palavra.i)
            G.add_node(txt, pos=objeto.palavra.pos_, dep=objeto.palavra.dep_)

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


    def _AdicionarLigacoesNoGrafo(self,conhecimento, G):
        for objeto in conhecimento:
            if objeto.palavra.pos_ == "V" or objeto.palavra.pos_ == "VAUX" or objeto.palavra.pos_ == "PCP":

                for subPrin in objeto.substantivoPrincipal:
                    aux = subPrin.text + "_" + str(subPrin.i)
                    aux2 = objeto.palavra.text + "_" + str(objeto.palavra.i)
                    G.add_edge(aux, aux2)

                for subPos in objeto.substantivo:
                    aux = objeto.palavra.text + "_" + str(objeto.palavra.i)
                    aux2 = subPos.text + "_" + str(subPos.i)
                    G.add_edge(aux, aux2)

                for demais in objeto.demaisRelacoes:
                    aux = objeto.palavra.text + "_" + str(objeto.palavra.i)
                    aux2 = demais.text + "_" + str(demais.i)
                    G.add_edge(aux, aux2)

                for verbo in objeto.verbos:

                    aux2 = verbo.text + "_" + str(verbo.i)

                    if verbo.i > objeto.palavra.i:
                        aux = objeto.palavra.text + "_" + str(objeto.palavra.i)
                        G.add_edge(aux, aux2)

                    if len(objeto.substantivoPrincipal) > 0:
                        aux = objeto.substantivoPrincipal[0].text + "_" + str(objeto.substantivoPrincipal[0].i)
                        G.add_edge(aux, aux2)

                    for sub in objeto.substantivo:
                        aux = sub.text + "_" + str(sub.i)
                        G.add_edge(aux, aux2)

            if objeto.palavra.pos_ == "N" or objeto.palavra.pos_ == "NPROP" or objeto.palavra.pos_ == "PROADJ" or objeto.palavra.pos_ == "PRO-KS" or objeto.palavra.pos_ == "PROPESS" or objeto.palavra.pos_ == "PRO-KS-REL" or objeto.palavra.pos_ == "PROSUB":
                for subPos in objeto.substantivo:
                    aux = objeto.palavra.text + "_" + str(objeto.palavra.i)
                    aux2 = subPos.text + "_" + str(subPos.i)
                    G.add_edge(aux, aux2)

                for demais in objeto.demaisRelacoes:
                    aux = objeto.palavra.text + "_" + str(objeto.palavra.i)
                    aux2 = demais.text + "_" + str(demais.i)
                    G.add_edge(aux, aux2)

                for verbo in objeto.verbos:
                    aux = objeto.palavra.text + "_" + str(objeto.palavra.i)
                    aux2 = verbo.text + "_" + str(verbo.i)
                    G.add_edge(aux, aux2)

            if objeto.palavra.dep_ == "case":
                for subPrin in objeto.substantivoPrincipal:
                    aux = subPrin.text + "_" + str(subPrin.i)
                    aux2 = objeto.palavra.text + "_" + str(objeto.palavra.i)
                    G.add_edge(aux, aux2)

                for subPos in objeto.substantivo:
                    aux = objeto.palavra.text + "_" + str(objeto.palavra.i)
                    aux2 = subPos.text + "_" + str(subPos.i)
                    G.add_edge(aux, aux2)

            if objeto.palavra.pos_ == "ADJ":

                for subPos in objeto.substantivo:
                    aux = objeto.palavra.text + "_" + str(objeto.palavra.i)
                    aux2 = subPos.text + "_" + str(subPos.i)
                    G.add_edge(aux, aux2)

                for verbo in objeto.verbos:
                    for substantivo in objeto.substantivo:
                        aux = substantivo.text + "_" + str(substantivo.i)
                        aux2 = verbo.text + "_" + str(verbo.i)
                        G.add_edge(aux, aux2)

                for demais in objeto.demaisRelacoes:
                    aux = objeto.palavra.text + "_" + str(objeto.palavra.i)
                    aux2 = demais.text + "_" + str(demais.i)
                    G.add_edge(aux, aux2)

        return G


    def ImprimirGrafo(self):

        con = self.conhecimentoMaster

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