import numpy as np
import pandas as pd
import string
import sys

oprt = ['-','*','+','/','%','=','~','>','<']
sep = ['(',')',';',':']

ADD   = 0    # +
SUB   = 1    # -
MUL   = 2    # *
DIV   = 3    # /
MOD   = 4    # %
AFF   = 5    # =
EQ    = 6    # ~

LE    = 7   # <
LEQ   = 8   # <=

GT    = 9   # >
GTQ   = 10   # >=

READ  = 11   # >>
PRINT = 12   # <<

SEP_OUV = 13 # (
SEP_FER = 14 # )
SEMI    = 15 # ;
DPNT    = 16

ID      = 17 # idf
CONST   = 18

KEY_BEG   =19 # begin
KEY_END   =20 # end

KEY_IF    =21 # if
KEY_EIF   =22
KEY_ELSE  =23 # else
KEY_EELSE = 24

KEY_WH    =25 # while
KEY_EWH =26 # ewhile

KEY_LET   =27  # let


keywords_finit_stats = [5]
keywords_automata = pd.read_csv('helper/keywords.csv')


# ========================================================

def is_keyword(string):
    string += '#'
    i = 0
    current_state = 0
    current_term = string[0]
    
    while current_term != '#' and current_state != -1 :
        current_state = keywords_automata[string[i]][current_state]
        i+=1
        current_term = string[i]        
        
    if current_term == "#" and current_state in keywords_finit_stats:
        return True   # accepted
    else :
        return False  # not accepted

# ========================================================

def is_idf(string):
    i=0
    if(string[i] == '_'):
        return string[1:].isalnum()
    else:
        return False

# ========================================================

def is_const(string):
    i=0
    if(string[i] == '.' or string[len(string) - 1] == '.'):
        return False
    else:
        num = string.replace('.', '')
        return num.isdigit() and ( string.count('.') == 1 or string.count('.') == 0 )

# ========================================================

def error(msg='',sym=' ',ligne=0):
    return "Error :" + msg +" "+ sym + " at ligne :" + str(ligne)

# ========================================================

def tok(token_type,token):
    """
    input : tocken_type , token
    output : dict of token
    """
    return {"token_type" : token_type , "value" : token}

# ========================================================

def lexical(code):
    i = 0
    num_ligne = 0
    tokens_table = []
    used_table = [] 
    while i < len(code):
        # calcule de lign ::::::::::::::::::::::::::::::::
        if(code[i] == '\n') : num_ligne += 1
        # print(num_ligne)

        # comments  ::::::::::::::::::::::::::::::::::::::
        if code[i]=='&':
            while code[i] != '\n':
                i+=1
            num_ligne += 1


        # skip spaces  :::::::::::::::::::::::::::::::::::
        elif code[i].isspace():
            pass


        # operateur  :::::::::::::::::::::::::::::::::::::
        elif code[i] in oprt:
            if  code[i] == '+' : 
                tokens_table.append(tok(ADD,None))
                used_table.append(tok(code[i],None))
                #print(code[i])
            elif code[i]== '-' : 
                tokens_table.append(tok(SUB,None))
                used_table.append(tok(code[i],None))
                #print(code[i])
            elif code[i]== '*' : 
                tokens_table.append(tok(MUL,None))
                used_table.append(tok(code[i],None))
                #print(code[i])
            elif code[i]== '/' : 
                tokens_table.append(tok(DIV,None))
                used_table.append(tok(code[i],None))
                #print(code[i])
            elif code[i]== '%' : 
                tokens_table.append(tok(MOD,None))
                used_table.append(tok(code[i],None))
                #print(code[i])
            elif code[i]== '=' : 
                tokens_table.append(tok(AFF,None))
                used_table.append(tok(code[i],None))
                #print(code[i])
            elif code[i]== '~' : 
                tokens_table.append(tok(EQ,None))
                used_table.append(tok(code[i],None))
                #print(code[i])

            elif code[i]== '<' :
                if code[i+1] == '<':
                    tokens_table.append(tok(PRINT,None))
                    #print(code[i]+code[i+1])
                    used_table.append(tok(code[i]+code[i+1],None))
                    i+=1
                elif code[i+1] == '=':
                    tokens_table.append(tok(LEQ,None)) # <=
                    used_table.append(tok(code[i]+code[i+1],None))
                    #print(code[i]+code[i+1])
                    i+=1
                else :
                    tokens_table.append(tok(LE,None))  # <
                    used_table.append(tok(code[i],None))
                    #print(code[i])


            elif code[i]== '>' :
                if code[i+1] == '>':
                    tokens_table.append(tok(READ,None))
                    used_table.append(tok(code[i]+code[i+1],None))
                    #print(code[i]+code[i+1])
                    i+=1

                elif code[i+1] == '=':
                    tokens_table.append(tok(GTQ,None)) # <=
                    used_table.append(tok(code[i]+code[i+1],None))
                    #print(code[i]+code[i+1])
                    i+=1

                else :
                    tokens_table.append(tok(GT,None)) # <
                    used_table.append(tok(code[i],None))
                    #print(code[i])


        # separateur :::::::::::::::::::::::::::::::::::::       
        elif code[i] in sep :
            if code[i] == '(': 
                tokens_table.append(tok(SEP_OUV,None))
                used_table.append(tok(code[i],None))
            elif code[i] == ')':
                tokens_table.append(tok(SEP_OUV,None))
                used_table.append(tok(code[i],None))
            elif code[i] == ';':
                tokens_table.append(tok(SEMI,None))
                used_table.append(tok(code[i],None))
            elif code[i] == ':':
                tokens_table.append(tok(DPNT,None))
                used_table.append(tok(code[i],None))
            #print(code[i]) # afficher supp      


        # idf ::::::::::::::::::::::::::::::::::::::::::::
        elif code[i] == '_':
            idf=''
            while (not code[i].isspace())and(code[i] not in oprt)and(code[i] not in sep):
                idf += code[i]
                i+=1
            if is_idf(idf):
                tokens_table.append(tok(ID,idf))
                used_table.append(tok("idf",idf))
                # print(idf)
            else :
                return error("INVALIDE IDF",idf,num_ligne),None,None
            i-=1   


        # keywords :::::::::::::::::::::::::::::::::::::::
        elif code[i].isalpha():
            word = ''
            while not code[i].isspace() and  code[i] not in sep:
                word += code[i]
                i+=1
            #print(word)
            if is_keyword(word):
                if   word == "begin" :
                    tokens_table.append(tok(KEY_BEG,word))
                    used_table.append(tok(word,None))
                elif word == "end" :
                    tokens_table.append(tok(KEY_END,word))
                    used_table.append(tok(word,None))
                elif word == "if" :
                    tokens_table.append(tok(KEY_IF,word))
                    used_table.append(tok(word,None))
                elif word == "eif" :
                    tokens_table.append(tok(KEY_EIF,word))
                    used_table.append(tok(word,None))
                elif word == "else" :
                    tokens_table.append(tok(KEY_ELSE,word))
                    used_table.append(tok(word,None))
                elif word == "eelse" :
                    tokens_table.append(tok(KEY_EELSE,word))
                    used_table.append(tok(word,None))
                elif word == "while" :
                    tokens_table.append(tok(KEY_WH,word))
                    used_table.append(tok(word,None))
                elif word == "ewhile" :
                    tokens_table.append(tok(KEY_EWH,word))
                    used_table.append(tok(word,None))
                elif word == "let" :
                    tokens_table.append(tok(KEY_LET,word))
                    used_table.append(tok(word,None))
                i-=1 # TODO : rani zedha bash na7it problem while(
            else :
                return error("INVALIDE KEYWORD",word,num_ligne),None,None # : error ligne number !

            # const (numero) :::::::::::::::::::::::::::::
        elif code[i].isnumeric():
            num = ''
            while not code[i].isspace() and code[i] not in sep: # add not in oprt
                num += code[i]
                i+=1
            #print(num)
            i-=1 # <----
            if is_const(num):
                tokens_table.append(tok(CONST,num))
                used_table.append(tok("num",num))
            else :
                return error("INVALIDE CONST",num,num_ligne),None,None

        else:
            # num_ligne = 120
            return error("INVALIDE SYMBOLE",code[i],num_ligne),None,None 
        i+=1
    return None,tokens_table , used_table