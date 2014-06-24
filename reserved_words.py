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
        }

        self.operator = {
            "GET UP": "+"
            "GET DOWN": "-"
            "YOU'RE FIRED": "*"
            "HE HAD TO SPLIT": "/"
            "YOU ARE NOT YOU YOU ARE ME": "=="
            "LET OFF SOME STEAM BENNET": ">"
            "CONSIDER THAT A DIVORCE": "|"
            "KNOCK KNOCK": "&"
        }

class WhatTheFuckDidIDoWrong(Exception):
    def __init__(self, line, value):
        self.value = "line " str(line) + ": " + value
    def __str__(self):
        return repr(self.value)
