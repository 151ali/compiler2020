import numpy as np
import pandas as pd
import string
import sys

print("analyse syntaxique ... ")
# =====================================================

def get_reduction_rule(number):
    grammar = {
        0:{"non_terminal" : "PROG", "production" : "begin BODY end"},  
        1:{"non_terminal" : "BODY", "production" : "VARDCLR BODY"},  
        2:{"non_terminal" : "BODY", "production" : "INSTRUCTIONS BODY"},  
        3:{"non_terminal" : "BODY", "production" : ""},  

        4:{"non_terminal" : "INSTRUCTIONS", "production" : "AFF"},  
        5:{"non_terminal" : "INSTRUCTIONS", "production" : "WHILE"},  
        6:{"non_terminal" : "INSTRUCTIONS", "production" : "IF"},  
        7:{"non_terminal" : "INSTRUCTIONS", "production" : "IN"},  
        8:{"non_terminal" : "INSTRUCTIONS", "production" : "OUT"},  

        9:{"non_terminal" : "VARDCLR", "production" : "let IDF STOP"},  
        10:{"non_terminal" : "STOP", "production" : ";"},  
        11:{"non_terminal" : "STOP", "production" : "= idf ;"},  
        12:{"non_terminal" : "STOP", "production" : "= num ;"},  

        13:{"non_terminal" : "EXPR", "production" : "T X"},  
        14:{"non_terminal" : "X", "production" : "+ T X"},  
        15:{"non_terminal" : "X", "production" : "- T X"},  

        16:{"non_terminal" : "X", "production" : ""},  
        17:{"non_terminal" : "T", "production" : "F Z"},  
        18:{"non_terminal" : "Z", "production" : "* F Z"},  
        19:{"non_terminal" : "Z", "production" : "/ F Z"},  
        20:{"non_terminal" : "Z", "production" : ""},  
        21:{"non_terminal" : "F", "production" : "( EXPR )"},  
        22:{"non_terminal" : "F", "production" : "idf"},  
        23:{"non_terminal" : "F", "production" : "num"},  

        24:{"non_terminal" : "AFF", "production" : "IDF = EXPR ;"},  
        25:{"non_terminal" : "WHILE", "production" : "while ( COND ) : BODY ewhile"},  
        26:{"non_terminal" : "COND", "production" : "OPRD OPR OPRD"},  
        27:{"non_terminal" : "OPR", "production" : "~"},  
        28:{"non_terminal" : "OPR", "production" : "<"},  
        29:{"non_terminal" : "OPR", "production" : "<="},  
        30:{"non_terminal" : "OPR", "production" : ">"},  
        31:{"non_terminal" : "OPR", "production" : ">="},  
        32:{"non_terminal" : "OPRD", "production" : "IDF"},  
        33:{"non_terminal" : "OPRD", "production" : "NUM"},  

        34:{"non_terminal" : "IF", "production" : "if ( COND ) : BODY eif else : BODY eelse"},  
        35:{"non_terminal" : "IF", "production" : "if ( COND ) : BODY eif"},  

        36:{"non_terminal" : "IN",  "production" : ">> IDF ;"},  
        37:{"non_terminal" : "OUT", "production" : "<< OPRD ;"},  
        38:{"non_terminal" : "IDF", "production" : "idf"},  
        39:{"non_terminal" : "NUM", "production" : "num"}  

    }
    
    return grammar.get(number,"Pas d'action")
	
# =====================================================

lr_table = pd.read_csv("helper/LR_table.csv")

# =====================================================

def get_action(action):
    if action == "acc"  :
        return {"action": "accept",
                "number":None}
    
    elif action[0] == "r" :
        return {"action": "Reduction",
                "number":action[1:]}
    
    elif action[0] == "s" :
        return {"action": "Shift",
                "number": action[1:]}
    
    elif action == ' ' :
        return {"action": None,
                "number":None}

# =====================================================


def syntaxique(used):
    
    a = [ item["value"] for item in used ]
    chaine = [ item["token_type"] for item in used ]

    chaine += "$"
    Stack = ['#',0]
    #init
    ptr = chaine[0]
    state = Stack[-1] # state = 0
    Do = get_action( lr_table[ptr][0] )

    # then do 
    while (Do["action"] != None and chaine != ['$']):
        haja = []
        if   Do["action"] == "Shift" : 
            # SHIFT ==============================::
            # D4 => S4 => shift_number = 4
            number = int(Do["number"])
            Stack.append( chaine.pop(0) )
            Stack.append(number)     

            # REDUCTION ==========================::
        elif Do["action"] == "Reduction":
            number = int( Do["number"] )        
            regle = get_reduction_rule(number)            
            right_part = regle["production"].split(sep=" ")
            right_part.reverse()
            left_part = regle["non_terminal"]
            #:faire la réducyion:#
            while ( right_part != [] ):
                if right_part == [''] :
                    break
                if Stack[-1] != right_part[0] :
                    Stack.pop()
                elif Stack[-1] == right_part[0]: 
                    Stack.pop()
                    haja += right_part[0]
                    right_part.pop(0)
                else :
                    sys.exit(0)
            # get la relation entre Stack[-1] et le non-terminal 
            rel = lr_table[left_part][Stack[-1]]
            # empiler la partie gauche :
            Stack.append(left_part)
            # empiler la relation
            Stack.append(int(rel)) 
        #print("-------")
        #print(chaine)
        # NEXT ===============================::
        Do = get_action(lr_table[chaine[0]][int(Stack[-1])])

    if(Do["action"] == "accept" and chaine == ['$']) : 
        return "entité syntaxiquement CORRECT"
    else :
        return "entité syntaxiquement FAUSSE"











