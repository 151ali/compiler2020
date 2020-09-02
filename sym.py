def generate_c_code(used):

    a      = [ item["value"] for item in used ]
    source = [ item["token_type"] for item in used ]



    c_source = ""
    while source != []:
        item  = source.pop(0)
        item2 =a.pop(0)
        
        if item == "begin":
            c_source += "#include<stdio.h>\nint main(){\n"
        if item == "end":
            c_source += "return 0;}"
        if item =="if":
            c_source += "if"
        if item =="eif":
            c_source += "}"
        if item =="else":
            c_source += "else}"
        if item =="eelse":
            c_source += "}"
        if item =="while":
            c_source += "while"       
        if item =="ewhile":
            c_source += "}"
        # declaration
        if item =="let":
            c_source += "int "
        if item =="idf":
            c_source +="v"+item2 
        if item =="num":
            c_source +=item2 
        # ecriture ;
        if item =="<<":
            source.pop(0)
            c_source += 'printf("%d\\n",' + 'v' + a.pop(0) + ")"
        # lire ;
        if item ==">>":
            source.pop(0)
            var_name = a.pop(0)
            c_source += 'printf("enter '+var_name+'\\n");'
            c_source += 'scanf("%d",&' + 'v' + var_name + ")"
        # sep 
        if item ==";":
            c_source += ";\n"
        if item ==":":
            c_source += "{\n"
        if item =="(":
            c_source += "("
        if item ==")":
            c_source += ")"
        # opérations mathematiques
        if item =="=":
            c_source += "="
        if item =="+":
            c_source += "+"
        if item =="-":
            c_source += "-"
        if item =="/":
            c_source += "/"
        if item =="*":
            c_source += "*"
        if item =="%":
            c_source += "%"
            # comparaison :
        if item =="<":
            c_source += "<"
        if item ==">":
            c_source += ">"
        if item =="~":
            c_source += "=="
        if item =="<=":
            c_source += "<="
        if item ==">=":
            c_source += ">="
    f = open("c_souce.c","w")
    f.write(c_source)
    f.close()
# gcc c_souce.c -o output
def code_run():
    import os
    os.system("gnome-terminal -e 'bash -c \" gcc c_souce.c -o output ;./output ; exec bash\"'")