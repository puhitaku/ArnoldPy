class ReservedWords:
    def __init__(self):
        self.word = {
            "Main":      "IT'S SHOWTIME",
            "Main_end":  "YOU HAVE BEEN TERMINATED",
            "If":        "BECAUSE I'M GOING TO SAY PLEASE",
            "Else":      "BULLSHIT",
            "If_end":    "YOU HAVE NO RESPECT FOR LOGIC",
            "While":     "STICK AROUND",
            "While_end": "CHILL",

            "Print":          "TALK TO THE HAND",
            "DecVar_name":    "HEY CHRISTMAS TREE",
            "DecVar_value":   "YOU SET US UP",
            "AssignVar_name": "GET TO THE CHOPPER",
            "AssignVar_opr":  "HERE IS MY INVITATION",
            "AssignVar_end":  "ENOUGH TALK",
            "Plus":           "GET UP",
            "Minus":          "GET DOWN",
            "Multiply":       "YOU'RE FIRED",
            "Divide":         "HE HAD TO SPLIT",
            "EqualTo":        "YOU ARE NOT YOU YOU ARE ME",
            "GreaterThan":    "LET OFF SOME STEAM BENNET",
            "Or":             "CONSIDER THAT A DIVORCE",
            "And":            "KNOCK KNOCK"
        }

class WHAT_THE_FUCK_DID_I_DO_WRONG(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
