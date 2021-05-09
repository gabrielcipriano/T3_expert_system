#%%
from experta import *

# Funçao auxiliar para receber inputs do teclado
def ask(question, true_value='S', false_value='N'):
    while True:
        answer = input(question + "(S/N)").upper()
        if (answer == 'S'): return true_value
        if (answer == 'N'): return false_value
        print("Responda com 'S' para Sim ou 'N' para Não.")

def ask_feature(question, true_value='S', false_value='N'):
    return ask("O animal " + question, true_value, false_value)



class Classe(Fact):
    pass

class Feature(Fact):
    pass

class Animal(Fact):
    pass

class DefineAnimalClass(KnowledgeEngine):
    # @DefFacts()
    # def _initial_action(self):
    #     yield Animal("Tartaruga")

    # FEATURES PARA DEFINIR CLASSE

    @Rule(NOT(Classe(W())))
    def ask_amamenta(self):
        self.declare(Feature(amamenta=ask_feature("é amamentado?")))

    @Rule(NOT(Classe(W())))
    def ask_branqueas(self):
        self.declare(Feature(branqueas=ask_feature("possui brânqueas (Guelras)?")))
    
    @Rule(NOT(Classe(W())))
    def ask_ovo_casca(self):
        self.declare(Feature(ovo_casca=ask_feature("bota ovos com casca rígida?")))
    
    @Rule(NOT(Classe(W())))
    def ask_duas_fases(self):
        self.declare(Feature(duas_fases=ask_feature("passa o começo da vida na água, e depois vive na terra?")))

    # DEFININDO CLASSE

    @Rule(Feature(amamenta='S'), salience=2)
    def is_mamal(self):
        self.declare(Classe('Mamífero'))

    @Rule(Feature(branqueas='S'), salience=2)
    def is_fish(self):
        self.declare(Classe('Peixe'))
    
    @Rule(Feature(duas_fases='S'), salience=2)
    def is_amphibian(self):
        self.declare(Classe('Anfibio'))
    
    @Rule(Feature(ovo_casca='S'), salience=2)
    def is_aves_or_reptile(self):
        self.declare(Classe(ask_feature("possui penas?", "Ave", "Réptil")))

    # COLETANDO FEATURES EM COMUM

    @Rule(AND(
                NOT(Animal(W())),
                OR(
                    Classe("Ave"), 
                    Classe("Réptil"), 
                    Classe("Mamífero")
                )
            )
        )
    def ask_carnivoro(self):
        self.declare(Feature(canivoro=ask_feature("é carnívoro?")))

    # @Rule(AND(
    #             NOT(Animal(W())),
    #             OR(
    #                 Classe("Ave"), 
    #                 Classe("Réptil"), 
    #                 Classe("Mamífero")
    #             )
    #         )
    #     )
    # def ask_aquatico_ou_semi(self):
    #     self.declare(Feature(aquatico_ou_semi=ask_feature("é aquatico ou gosta de viver bem perto da água?")))

    # @Rule(Classe("Ave"), Classe("Mamífero"), salience=1)
    # def ask_voa(self):
    #     self.declare(Feature(voa=ask_feature("é capaz de voar?")))

    # DIFERENCIANDO RÉPTEIS

    @Rule(AND(
            Classe("Réptil"), 
            Feature(carnivoro='S')
        ), salience=1)
    def is_jacare(self):
        self.declare(Animal("Jacaré"))

    @Rule(Animal(MATCH.name))
    def guess_animal(self, name):
        print("O seu animal é um(a) %s" % (name))
# %%

engine = DefineAnimalClass()
engine.reset()
engine.run()

# %%
