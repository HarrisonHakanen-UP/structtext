from Principal.Projeto import Projeto
from Principal.Comparacao import Comparacao


frase1 = "Uma mulher foi atropelada por um carro enquanto atravessava a rua"
frase2 = "Um carro atroupelou uma mulher que atravessava uma rua, então o carro fugiu do local"
frase3 = "Ao atravessar uma rua a mulher foi atropelada por um carro"
frase4 = "Ontem minha mãe estudou tanto até ficar cansada. Eu lavei a louça então ela me agradeceu."
fraseTeste= "Ontem o cachorro do Jeferson brincou de enterrar o osso enquanto o cachorro de Maria corria pelo parque, então o cachorro do Jeferson ficou cansado"
fraseTeste2= "Ontem o cachorro do Jeferson brincou de enterrar o osso, então o cachorro ficou parado"
fraseTeste3 = "Maria embora não tivesse tempo, comprou um cachorro"
fraseTeste4 = "Quando chegou das férias, Maria que gosta muito de animais, embora não tivesse dinheiro, adquiriu, escondendo do marido, um cachorro"
fraseTeste_substantivo_complexo_com_substantivo = "Para implementar um web service de baixo overhead que tenha recursos identificáveis e localizáveis por meio de uma URI (Uniform Resource Identifier) mediante o protocolo HTTP, pode-se utilizar o REST (Representational State Transfer)."
f = "Diego estava andando pela cidade, então comprou, pensando em sua namorada, uma bota"
f1 = "Diego estava andando na cidade então comprou uma bota pensando em sua namorada "
f2 = "Diego comprou uma bota pensando em sua namorada enquanto andava pela cidade"
f3 = "Ontem o cachorro do Jeferson brincou de enterrar o osso enquanto o cachorro de Maria corria pelo parque, então o cachorro do Jeferson Carlos ficou cansado."
f4 = "Ontem Roberto estava com sua cachorrinha, então ela muito querida lhe pediu um docinho, Roberto então foi pegar um doce para ela, porém a mãe de Roberto falou que não poderia dar um doce para a cachorrinha"
f5 = "O sapado do homem estava desamarrado, então outro homem o avisou"
f6 = "Um carro atroupelou uma mulher que atravessava uma rua, então o carro que atroupelou a mulher fugiu do local"
fraseComPronomeComplexo = "Os serviços Web RESTful utilizam o HTTP como um meio de comunicação entre cliente e servidor."
fraseComPronomeComplexo2 = "Para implementar um web service de baixo overhead que tenha recursos identificáveis e localizáveis por meio de uma URI (Uniform Resource Identifier) mediante o protocolo HTTP, pode-se utilizar o REST (Representational State Transfer)."

entidades = "Salvador Dalí i Domènech, foi o 1º Marquês de Dalí de Púbol, um importante pintor espanhol, conhecido pelo seu trabalho surrealista."

adjetivo = "Marcelo é bonito e muito gentil, ontem ele não pode ir ao jogo de futebol mas ficou em casa. Marcos um rapaz muito prestativo estudou matemática"

fraseTeste6 = "Maria uma moça bela e inteligente, embora não tivesse tempo, comprou um cachorro"
fraseTeste7 = "Maria ontem estava andando pela rua e foi a uma loja e mesmo que não tivesse dinheiro e seu marido não concordasse, comprou um cachorro muito bonito"

testandofrase = "Fui para casa da minha avó ontem estudar matemática"

'''O que são processos'''
respostaProfessor_P7 = "Os chamados processos são módulos executáveis, é uma lista de instruções, a qual informa ao processador que passos devem ser executados e em quais momentos isso acontece."
resposta1_P7 = "Os processos são listas que servem para dizer ao processador o que deve ser feito"

conhecimento1 = Projeto(respostaProfessor_P7)
conhecimento2 = Projeto(resposta1_P7)

#conhecimento1.ImprimirGrafo()
Comp = Comparacao(conhecimento1.RetornarConhecimento(),conhecimento2.RetornarConhecimento())

#Comp.ImprimirConhecimento()
Comp.ImprimirGrafo()
#projeto.ConhecimentoCalibrado()

#projeto.ImprimirGrafo()







#frase3 não fazendo ligações corretas.
#fraseTeste2 e f3 está duplicando colocando "Jeferson" como um não substantivo ou pronome...sei la pq
#fraseTeste3 Maria e comprou aparecem como relações não catalogadas pelos grafos (deve ser algo quando se criam os nós do grafo)

