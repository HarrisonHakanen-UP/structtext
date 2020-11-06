import mysql.connector as mysql
from Model import Classes
from Principal.Main import Main

def CompararRespostasDasProvas():
    db = mysql.connect(
        host="localhost",
        user="root",
        password="password",
        database="db_testanalyser",
        auth_plugin='mysql_native_password'
    )

    mycursor = db.cursor(dictionary=True)
    QuestoesProfessor = []

    mycursor.execute("SELECT * FROM db_testanalyser.questoes WHERE RespostaDiscursiva IS NOT NULL AND situacao = 1")
    questoesProfessor = mycursor.fetchall()

    for questao in questoesProfessor:

        questao_professor = Classes.Questoes(questao["QuestaoId"],questao["Assunto"],questao["Enunciado"],questao["TipoQuestao"],questao["situacao"],questao["RespostaDiscursiva"],questao["Disciplina_DisciplinaId"])

        mycursor.execute("SELECT * FROM db_testanalyser.respostasalunos WHERE Questao_QuestaoId ="+str(questao_professor.QuestaoId)+" AND RespostaDiscursiva IS NOT NULL AND SituacaoCorrecao = 0")

        questoesAluno = mycursor.fetchall()

        for questaoAluno in questoesAluno:

            aluno = Classes.RespostasAlunos(questaoAluno["RespostasAlunoId"], questaoAluno["RespostaDiscursiva"], questaoAluno["NotaAluno"], questaoAluno["SituacaoCorrecao"], questaoAluno["DataHoraInicio"], questaoAluno["DataHoraFim"],questaoAluno["Aluno_AlunoId"], questaoAluno["Questao_QuestaoId"], questaoAluno["Prova_ProvaId"])
            questao_professor.RespostasDosAlunos.append(aluno)

        QuestoesProfessor.append(questao_professor)

    Inicio = Main(QuestoesProfessor)
    Inicio.Iniciar()




    print("feito")