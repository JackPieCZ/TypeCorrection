### TODO list
# 95,32 , 0,01 0,03 chyba


import re
import difflib
import os

here = os.path.dirname(os.path.abspath(__file__)) #set the current file path

def listToString(s):  #converting list to string
    str1 = " "  
    return (str1.join(s)) 

def find_all(s, ch): #finding all accurences
	occurences=[]
	for i, ltr in (enumerate(s)):
		if ltr == ch:
			occurences.append(i)
	return(occurences)


file1=os.path.join(here, "syn2015_word_utf8.tsv") #set path for vocabulary
vocabulary = open(file1, "r", encoding="utf8")
voc=[]
raw_line = vocabulary.readline()
while raw_line: #reading line by line and taking the second item (after tab)
	split_line=re.split(r'\t+', raw_line)
	voc.append(split_line[1].lower())
	raw_line=vocabulary.readline()
for i in range(0,20000): #adding numbers
	voc.append(str(i))

file2=os.path.join(here,"voda_errors.txt") #path for file to correct
file_chyby = open(file2, "r", encoding="utf8")
na_opravu=[]
raw_line = file_chyby.readline()
while raw_line: #adding every line to list
	na_opravu.append(raw_line)
	raw_line=file_chyby.readline()

user_slovnik = ['abode', 'aquifer', 'aquiferů', 'argyre', 'anody','bazaltovém', 
'canali', 'canals', 'celoplanetárním', 'cerberus',  'crism', "čepiček", 'erodovaných', 'erozivní', 'evaporaci', 'fossae', 'gusev', 
'hesperianu', 'hydrosféry', 'impaktních', 'impaktů', 'kryosféry', 'kryosféře', "m3.s−1", "ma'adim", 'mariner', 'marineris', 
'marsovské', "marsovský",'marsovského', 'meridiani', 'mola', 'montes', 'napovídající', 'nasa', 'naskytuje', 'neutronovým', 'noachianu', 
'noachis', 'oceanus', 'painted', 'palagonit', 'permafrostem', 'planitia', 'polotekuté', 'reconnaissance', 'regolitu', 'roztáním', 
'sedimentovat', 'sesutím', 'sezónního', 'skupenstvích', 'sonda','sojourner', 'spektrometrem', 'spektrometrických', 'spektroskopické', 'sublimoval', 
"sureyor",'surveyor', 'svahového', 'svrchnějších', 'terraformace', 'transportované', 'trojného', 'ustávání', 'vallis', 'vastitas', 
'vysočin', 'vysočinami', 'vysychajících','whewell', 'zarovnány', 'zařezávání', 'zbrázděn', 'zlomkovou'] #special words that are missing in voc
for wd in user_slovnik:
	voc.append(wd)
restricted_slovnik = ["ktoré","proc","al","sita","vz","onda","tri","dísy","peyo","tk","leem","dě","anody"] #removing some confusing words
for wd in restricted_slovnik:
	try:
		voc.remove(wd)
	except:
		pass
voc = list(dict.fromkeys(voc)) #removing duplicates

file3=os.path.join(here,"voda_opraveno.txt") #path for final correct file
file_opraveno = open(file3, "w", encoding="utf8")

file4=os.path.join(here,"script_output.txt") #path for debug output file
file_out = open(file4, "w", encoding="utf8")

veta_now = 0
veta_all = len(na_opravu)

for veta in na_opravu:
    veta_now +=1 #current phrase
    print(str(veta_now)+"/"+str(veta_all), end="\r")
    spravna_veta=[] 
    split_veta=veta.split()
    for slovo in split_veta:
        print(slovo, file=file_out)
        capitals = []
        index_cap = 0
        prefix = ""
        sufix = ""
        spec_znaky = "().,?!;:…„“–-×%=~°'"
        slovo_raw = slovo
        for ch in slovo:
            if ch in spec_znaky:
                prefix=prefix+ch
            else:
                break
        if len(slovo)>1:
            for ch in slovo[::-1]:
                if ch in spec_znaky:
                    sufix=sufix+ch
                else:
                    break
            sufix = sufix[::-1]
        slovo = slovo.replace(prefix,"").replace(sufix,"")
        
        for ch in slovo:
            if ch.istitle():
                capitals.append(index_cap)
            index_cap+=1
        slovo = slovo.lower()
        
        if slovo not in voc:
            if (slovo.isnumeric() is False) and ("×" not in slovo):
                if len(slovo)==0:
                    slovo=""
                else:
                    print("Chyba: "+slovo, file=file_out)
                    oprava = difflib.get_close_matches(slovo, voc, n=1)
                    slovo=oprava[0]
                    print("opraveno: "+slovo, file=file_out)
        
        slovo = prefix + slovo + sufix

        if capitals != []:
            for i in capitals:
                if i == 0:
                    slovo = slovo.title()
                else:
                    if len(slovo)>1:
                        slovo = slovo[:i] + slovo[i].upper() + slovo[i+1:]
        if len(slovo)>=2:
            if slovo_raw[-2] in spec_znaky and slovo_raw[-1].isnumeric():
                slovo = slovo[:-2] + slovo_raw[-2] + slovo[-1]
            if slovo_raw[-2] == ".":
                slovo+="."
            if slovo_raw[-2] == ",":
                slovo+=","

        print(slovo, file=file_out)
        print("", file=file_out)
        spravna_veta.append(slovo)
    
    veta = listToString(spravna_veta)
    print(split_veta, file=file_out)
    print(veta, file=file_out)
    file_opraveno.write(veta+"\n")
file_opraveno.close()
print("done")