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