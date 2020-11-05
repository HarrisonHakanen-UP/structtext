from Principal.Projeto import Projeto
from Principal.Comparacao import Comparacao
import mysql.connector as mysql
from gensim.models import KeyedVectors


class Main:

    def __init__(self,_QuestaoProfessor):
        self.QuestaoProfessor = _QuestaoProfessor
        self.modelo = KeyedVectors.load_word2vec_format('cbow_s50.txt', binary=False)


    def Iniciar(self):

        conhecimento1 = Projeto(self.QuestaoProfessor.RespostaDiscursiva)
        for questaoAluno in self.QuestaoProfessor.RespostasDosAlunos:

            conhecimento2 = Projeto(questaoAluno.RespostaDiscursiva)

            Comp = Comparacao(conhecimento1,conhecimento2,self.modelo)

            print(Comp.semelhanca)

