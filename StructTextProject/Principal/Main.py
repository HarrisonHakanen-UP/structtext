from Projeto import Projeto
from Comparacao import Comparacao
import mysql.connector as mysql
from gensim.models import KeyedVectors


class Main:

    def __init__(self,_QuestaoProfessor):
        self.QuestaoProfessor = _QuestaoProfessor
        print("Carregando modelo")
        self.modelo = KeyedVectors.load_word2vec_format('cbow_s50.txt', binary=False)


    def Iniciar(self):

        for questaoProfessor in self.QuestaoProfessor:

            conhecimento1 = Projeto(questaoProfessor.RespostaDiscursiva)
            for questaoAluno in questaoProfessor.RespostasDosAlunos:

                conhecimento2 = Projeto(questaoAluno.RespostaDiscursiva)

                Comp = Comparacao(conhecimento1,conhecimento2,self.modelo)
                questaoAluno.NotaAluno = Comp.semelhanca

                print("Carregando banco para atribuir nota")

                try:
                    db = mysql.connect(
                        host="localhost",
                        user="root",
                        password="250389",
                        database="db_testanalyser",
                        auth_plugin='mysql_native_password'
                    )

                    mycursor = db.cursor()

                    mycursor.execute("UPDATE db_testanalyser.respostasalunos SET SituacaoCorrecao = 1, NotaAluno = "+str(questaoAluno.NotaAluno)+" WHERE RespostasAlunoId ="+str(questaoAluno.RespostaAlunoId))

                    db.commit()

                    print(mycursor.rowcount, "record(s) affected")

                    db.close()
                except Exception as e:
                    print(e)
