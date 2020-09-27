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
                if substantivoPrincipal_FrasePrincipal.text.lower() != "":
                    if substantivo.text.lower() != "":
                        if substantivoPrincipal_FrasePrincipal.text.lower() in self.cbow_model.vocab and substantivo.text.lower() in self.cbow_model.vocab:
                            if substantivo.pos_ == "N" and self.cbow_model.similarity(
                                    substantivoPrincipal_FrasePrincipal.text.lower(),
                                    substantivo.text.lower()) > 0.5 or substantivoPrincipal_FrasePrincipal.text == substantivo.text:

                                if existeCase1 == 1 and existeCase2 == 1:
                                    if str(substantivoComCase1[0].text) + " " + str(
                                            substantivoComCase1[1].text) == str(
                                        substantivoComCase2[0].text) + " " + str(
                                        substantivoComCase2[1].text):
                                        # print("Encontrou: "+str(substantivoComCase1[2].text)+" "+str(substantivoComCase1[0].text)+" "+str(substantivoComCase1[1].text+" "+palavraFraseTeste.palavra.text))

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
                                            substantivoComCase1[0].text) + " " + str(substantivoComCase1[
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
                                                        verbo.substantivoPrincipal.append(substantivoTeste)

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
                                                    if self.cbow_model.similarity(relacaoPrincipal.text.lower(),
                                                                                  relacaoTeste.text.lower()) > 0.5:
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
                                                            verbo.substantivo.append(substantivoPosteriorTeste)


                        else:
                            if substantivoPosteriorTeste.pos_ == "NPROP" and substantivoPosteriorPrincipal.pos_ == "NPROP":
                                if substantivoPosteriorTeste.text == substantivoPosteriorPrincipal:
                                    verbo.substantivo.append(substantivoPosteriorTeste)

                listaDeVerbos.append(verbo)
            else:
                print("Verbos diferentes por um adv negativo")

        continua = 0