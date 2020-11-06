class Palavra:

    def __init__(self, _palavra):
        self.palavra = _palavra
        self.substantivoPrincipal = []
        self.substantivo = []
        self.demaisRelacoes = []
        self.verbos = []
        self.adjetivos = []


class VerboIgual:

    def __init__(self, _verbo):
        self.palavra = _verbo
        self.substantivoPrincipal = []
        self.substantivoPrincipal_naoEncontrado = []
        self.substantivo = []
        self.substantivo_naoEncontrado = []
        self.demaisRelacoes = []
        self.demaisRelacoes_naoEncontradas = []
        self.verbos = []
        self.verbos_naoEncontrados = []
        self.adjetivos = []
        self.adjetivos_naoEncontrados = []
        self.semelhanca = 0



class TokenAux:

    def __init__(self, _palavra):
        self.text = _palavra
        self.i = 0
        self.pos_ = ""
        self.filhos = []
        self.dep_ = ""
        self.lemma_ = ""
        self.tag_ = []
        self.depStanza_ = ""


class Questoes:

    def __init__(self,_QuestaoId,_Assunto,_Enunciado,_TipoQuestao,_situacao,_RespostaDiscursiva,_Disciplina_DisciplinaId):
        self.QuestaoId = _QuestaoId
        self.Assunto = _Assunto
        self.Enunciado = _Enunciado
        self.TipoQuestao = _TipoQuestao
        self.situacao = _situacao
        self.RespostaDiscursiva = _RespostaDiscursiva
        self.Disciplina_DisciplinaId = _Disciplina_DisciplinaId
        self.RespostasDosAlunos = []



class RespostasAlunos:

    def __init__(self,_RespostaAlunoId,_RespostaDiscursiva,_NotaAluno,_SituacaoCorrecao,_DataHoraInicio,_DataHoraFim,_Aluno_AlunoId,_Questao_QuestaoId,_Prova_ProvaId):
        self.RespostaAlunoId = _RespostaAlunoId
        self.RespostaDiscursiva = _RespostaDiscursiva
        self.NotaAluno = _NotaAluno
        self.SituacaoCorrecao = _SituacaoCorrecao
        self.DataHoraInicio = _DataHoraInicio
        self.DataHoraFim = _DataHoraFim
        self.Aluno_AlunoId = _Aluno_AlunoId
        self.Questao_QuestaoId = _Questao_QuestaoId
        self.Prova_ProvaId = _Prova_ProvaId