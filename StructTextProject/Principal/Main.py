from Principal.Projeto import Projeto
from Principal.Comparacao import Comparacao


frase1 = "Uma mulher foi atropelada por um carro enquanto atravessava a rua"
frase2 = "Um carro atropelou uma mulher que atravessava uma rua, então o carro fugiu do local"
frase3 = "Ao atravessar uma rua a mulher foi atropelada por um carro"
frase4 = "Ontem minha mãe estudou tanto até ficar cansada. Eu lavei a louça então ela me agradeceu."
fraseTeste= "Ontem o cachorro do Jeferson brincou de enterrar o osso e correr no parque, então o cachorro ficou parado"
fraseTeste2= "Ontem o cachorro do Jeferson brincou de enterrar, enquanto o cachorro de Maria corria pelo parque"

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

fraseTeste= "Ontem o cachorro do Jeferson brincou de enterrar o osso e correr no parque, então o cachorro ficou parado"
fraseTeste2= "Ontem o cachorro do Jeferson brincou de enterrar o osso, enquanto o cachorro de Maria corria pelo parque"

fraseTeste3 = "Uma garota bonita, embora tivesse tempo, comprou um cachorro"
fraseTeste4 = "Uma garota bonita, embora não tivesse tempo, comprou um cachorro e foi para casa"

fraseTeste5 = "Maria uma mulher bonita e inteligente, embora não tivesse tempo, comprou um cachorro"
fraseTeste6 = "Maria uma moça bela e inteligente, embora não tivesse tempo, comprou um cachorro"
fraseTeste7 = "Maria ontem estava andando pela rua e foi a uma loja e mesmo que não tivesse dinheiro e seu marido não concordasse, comprou um cachorro muito bonito"

fraseKet = "Morfina. Nos estudos controlados randomizados, os opioides se mostraram capazes de diminuir a dispneia tanto em pacientes com câncer de pulmão quanto em pacientes com DPOC. O oxigênio é útil apenas se o paciente tiver hipoxia. Os benzodiazepínicos não demonstraram redução da dispneia."


'''O que é um mainframe?'''
respostaProfessor_P1 = "plataforma integrada de computadores capaz de processar grandes volumes de informações em curtos espaços de tempo"
resposta1_P1 = "É um computador integrado a outros computadores" #Errada
resposta2_P1 = "É uma plataforma que processa grandes volumes de informações" #Certa


'''O que é o Windwos defender'''
repostaProfessor_P2 = "Um software antispyware incluído no Windows que executa ao iniciar o sistema"
resposta1_P2 = "É um software que tem função antispyware"
resposta2_P2 = "Um software que está incluido no Windows"


#Esse aqui não está legal, necessita de uma verificação
'''Com relação à gestão de projetos, julgue os itens que se seguem'''
respostaProfessor_P3 = "Quanto maior for a maturidade dos processos relacionados ao projeto, menor será a dificuldade e os riscos de executá-lo."
resposta1_P3 = "Um processo mais maduro tem menor dificulade e riscos"
#------------------------------------------------------------------


'''Com relação à gestão de projetos, julgue os itens que se seguem.'''
respostaProfessor_P4= "Quando a complexidade técnica e a relacional são elevadas, as dificuldades e os riscos são maiores, podendo dificultar a execução do projeto."
resposta1_P4 = "Quanto maior a complexidade maior a dificuldade de execução do projeto"

'''O que é hipervisor? Qual a diferença entre o tipo 1 e tipo 2?'''

respostaProfessor_P5 = "Hipervisor é a camada de software que permite a criação (virtualização) de máquinas virtuais e, consequentemente, seu gerenciamento e controle.O Hipervisor tipo 1 é um hipervisor que é instalado diretamente sobre o hardware e onde são instalados os sistemas operacionais.O Hipervisor tipo 2 é implementado para funcionar como se fosse uma aplicação do sistema operacional hospedeiro operando em modo usuário, onde serão criadas as máquinas virtuais. Na prática é um programa do sistema hospedeiro que oferece um ambiente para simular máquinas reais."
resposta1_P5 = "É uma camada de software que permite a virtualização e controle das mesmas, o tipo 1 são instalados no hardware e no sistema operacional, já o hipervisor tipo 2 é um programa que fica no sistema hospedeiro que oferece um ambiente que simula máquinas reais"
resposta2_P5 = "É uma camada de software que permite a virtualização e controle das mesmas"
resposta3_P5 = "É uma camada de software, o hipervisor 1 é um programa hospedeiro e o hipervisor 2 é instalado no hardware"

'''Thread e processo são conceitos diferentes. Explique a diferença entre o conceito de processo e o conceito de thread. O que as threads acrescentam ao modelo de processo ?'''
respostaProfessor_P6 = "Em SO tradicionais, cada processo tem um único fluxo de execução (o que define uma thread), a unidade de processamento concorrente destinada para ser executada sob as condições de desempenho de um processador da época. Com o surgimento de processadores de mais alto desempenho, uma nova unidade de processamento concorrente pôde ser definida dentro do próprio processo, materializando novas unidades de fluxo de execução e assim pode-se ter múltiplos fluxos de execução (múltiplas threads) num mesmo processo. O que as threads acrescentam ao modelo de processo é permitir que múltiplos fluxos de execução ocorram no mesmo ambiente do processo, com um grau de independência uma das outras. Assim, múltiplas threads executam concorrentemente em um processo, e é análogo a múltiplos processos executando concorrentemente em um único computador. No primeiro caso, threads compartilham o mesmo espaço de endereçamento e recursos do processo onde são executadas e o termo multhreading é usado para descrever a situação em que múltiplas threads são executadas no mesmo processo. Quando um processo com múltiplas threads é executado em um SO com um único processador, as threads são escalonadas para execução, alternando rapidamente entre as threads, dando a ilusão que são executadas em paralelo num processador mais lento que o processador real."
resposta1_P6 = "Os chamados “processos” são módulos executáveis, é uma lista de instruções, a qual informa ao processador que passos devem ser executados e em quais momentos isso acontece."





'''O que são processos'''
respostaProfessor_P7 = "Os chamados processos são módulos executáveis, é uma lista de instruções, a qual informa ao processador que passos devem ser executados e em quais momentos isso acontece."
resposta1_P7 = "Os processos são listas que servem para dizer ao processador o que deve ser feito"

'''Diferença entre programa e processo'''
respostaProfessor_P8 = "Um programa é um software de computador que tem uma lista de processos. Um processo é uma lista de instruções que são enviadas para o processador."
resposta1_P8 = "O processo é uma lista de passos enquanto um programa é um software."
resposta2_P8 = "Um processo é a instância de um software, ou seja, um software é uma lista de comandos"
resposta3_P8 = "Quando falamos em processos, nos referimos a listas de instruções que são enviadas para o processador, enquanto um software é um programa que é feito para um computador"
resposta4_P8 = "Processos são instruções enquanto software é um programa de computador"

'''O que é a camada física do modelo OSI?'''
respostaProfessor_P9 = "A camada física são os dispositivos de rede como modem ou os cabos, é por onde os dados trafegam."
resposta1_P9 = "é a camada onde estão os dispositivos de rede"
resposta2_P9 = "é a camada que verifica os erros dos pacotes"
resposta3_P9 = "é a camda que possibilita a conexão de vários computadores em uma rede"
resposta4_P9 = "ficam os equipamentos de rede, como os cabos e modem"

'''Qual a função do comando ls?'''
respostaProfessor_P10 = "serve para listar os diretórios e arquivos da pasta que o usuário está naquele momento"
resposta1_P10 = "listar os diretórios"
resposta2_P10 = "listar os diretórios e arquivos"
resposta3_P10 = "cria um diretório na pasta que o usuário está"
resposta4_P10 = "Tem como objetivo mostrar os diretórios e arquivo para o usuário"

'''
resposta2_P8 era para ter uma nota baixa - o problema é que são poucas dimensões no modelo word embeddings escolhido.
resposta3_P8 era para ter uma nota alta
resposta4_P10 era para ter uma nota baixa
'''





#conhecimento1 = Projeto(respostaProfessor_P8)
conhecimento2 = Projeto(resposta4_P8)

#conhecimento1.ImprimirGrafo()
#Comp = Comparacao(conhecimento1.RetornarConhecimento(),conhecimento2.RetornarConhecimento())

#Comp.ImprimirConhecimento()
#Comp.ImprimirGrafo()
#projeto.ConhecimentoCalibrado()

#projeto.ImprimirGrafo()







#frase3 não fazendo ligações corretas.
#fraseTeste2 e f3 está duplicando colocando "Jeferson" como um não substantivo ou pronome...sei la pq
#fraseTeste3 Maria e comprou aparecem como relações não catalogadas pelos grafos (deve ser algo quando se criam os nós do grafo)

