from Principal.Projeto import Projeto
from Principal.Comparacao import Comparacao
import mysql.connector as mysql
from gensim.models import KeyedVectors


class Main:

    def __init__(self,_QuestaoProfessor):
        self.QuestaoProfessor = _QuestaoProfessor
        self.modelo = KeyedVectors.load_word2vec_format('cbow_s50.txt', binary=False)


    def Iniciar(self):


        for questaoProfessor in self.QuestaoProfessor:

            conhecimento1 = Projeto(questaoProfessor.RespostaDiscursiva)
            for questaoAluno in questaoProfessor.RespostasDosAlunos:

                conhecimento2 = Projeto(questaoAluno.RespostaDiscursiva)

                Comp = Comparacao(conhecimento1,conhecimento2,self.modelo)


                questaoAluno.NotaAluno = Comp.semelhanca


