import re
import difflib
import os
import json
import requests

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
voc_file = open(file1, "r", encoding="utf8")
voc_words = []
voc_freq = {}
raw_line = voc_file.readline()
current_line=1
while raw_line: #reading line by line and taking the second item (after tab)
    split_line=re.split(r'\t+', raw_line)
    voc_words.append(split_line[1].lower())
    if split_line[1].lower() not in voc_freq:
        voc_freq.update({split_line[1].lower(): split_line[2]})
    raw_line = voc_file.readline()
voc_words = list(dict.fromkeys(voc_words)) #removing duplicates
for i in range(20000):
    voc_words.append(str(i))

file2=os.path.join(here,"voda_errors.txt") #path for file to correct
file_chyby = open(file2, "r", encoding="utf8")
na_opravu=[]
raw_line = file_chyby.readline()
while raw_line: #adding every line to list
	na_opravu.append(raw_line)
	raw_line=file_chyby.readline()

user_slovnik = ["3d",'abode', 'aquifer', 'aquiferů', 'argyre', 'anody','bazaltovém', 
'canali', 'canals', 'celoplanetárním', 'cerberus',  'crism', "čepiček", "co2",'erodovaných', 'erozivní', 'evaporaci', 'fossae', 'gusev', 
'hesperianu', 'hydrosféry', 'impaktních', 'impaktů', 'km3','kryosféry', 'kryosféře', "m3", "m3.s−1", "ma'adim", 'mariner', 'marineris', 
'marsovské', "marsovský",'marsovského', 'meridiani', 'mola', 'montes', 'napovídající', 'nasa', 'naskytuje', 'neutronovým', 'noachianu', 
'noachis', 'oceanus', 'painted', 'palagonit', 'permafrostem', 'planitia', 'polotekuté', 'reconnaissance', 'regolitu', 'roztáním', 
'sedimentovat', 'sesutím', 'sezónního', 'skupenstvích', 'sonda','sojourner', 'spektrometrem', 'spektrometrických', 'spektroskopické', 'sublimoval', 
"sureyor",'surveyor', 'svahového', 'svrchnějších', 'terraformace', 'transportované', 'trojného', 'ustávání', 'vallis', 'vastitas', 
'vysočin', 'vysočinami', 'vysychajících','whewell', 'zarovnány', 'zařezávání', 'zbrázděn', 'zlomkovou'] #special words that are missing in voc
for wd in user_slovnik:
	voc_words.append(wd)
restricted_slovnik = ["ktoré","proc","al","sita","vz","onda","tri","dísy","peyo","tk","leem","dě","anody"] #removing some confusing words
for wd in restricted_slovnik:
	try:
		voc_words.remove(wd)
	except:
		pass

file3=os.path.join(here,"voda_opraveno.txt") #path for final correct file
file_opraveno = open(file3, "w", encoding="utf8")

file4=os.path.join(here,"script_output.txt") #path for debug output file
file_out = open(file4, "w", encoding="utf8")

veta_now = 0
veta_all = len(na_opravu)
"""
#možnost využít API MFF pro korektor vět
#funguje hůř než současná verze skriptu - proto je odkomentovaná

na_opravu2 = []
for veta in na_opravu:
    veta_now +=1
    print(str(veta_now)+"/"+str(veta_all), end="\r")
    response = requests.get("http://lindat.mff.cuni.cz/services/korektor/api/correct?data="+veta)
    res_json = response.json()
    veta = (res_json.get("result"))
    if veta_now < veta_all:
        file_opraveno.write(veta+"\n")
    else:
        file_opraveno.write(veta+" ")
file_opraveno.close()
print("done")
"""
veta_now = 0
veta_all = len(na_opravu)

for veta in na_opravu:
    veta_now +=1 #current phrase
    print(str(veta_now)+"/"+str(veta_all), end="\r")
    spravna_veta=[] 
    split_veta=veta.split()
    for slovo in split_veta:
        print(slovo, file=file_out)
        capitals = [] #indexy písmen které jsou velkými písmeny
        index_cap = 0
        prefix = ""
        sufix = ""
        spec_znaky = "().,?!;:…„“–-×%=~°'−"
        slovo_raw = slovo
        for ch in slovo:  #odstranění speciálních znaků na začátku slova
            if ch in spec_znaky:
                prefix=prefix+ch
            else:
                break
        if slovo == prefix:
            prefix == ""
        if prefix != "":
            print("prefix: "+prefix, file=file_out)
        slovo = slovo.replace(prefix,"")
        if len(slovo)>1:
            for ch in slovo[::-1]: #odstranění speciálních znaků na konci slova
                if ch in spec_znaky:
                    sufix=sufix+ch
                else:
                    break
            sufix = sufix[::-1]
        if slovo == sufix:
            sufix == ""
        if sufix != "":
            print("sufix: "+sufix, file=file_out)
        slovo = slovo.replace(sufix,"")
        
        for ch in slovo: #hledání velkých písmen
            if ch.istitle():
                capitals.append(index_cap)
            index_cap+=1
        slovo = slovo.lower()
        print("Capitals: "+str(capitals), file=file_out)
        
        if slovo not in voc_words:
            if (slovo.isnumeric() is False) and ("×" not in slovo): #např 3x3, 16x10,...
                slovo_test = slovo.replace(",","")
                if slovo_test.isnumeric() is False: #např 10,8; 3,3;...
                    if len(slovo)==0:
                        slovo=""
                    else:
                        print("Chyba: "+slovo, file=file_out)
                        oprava = difflib.get_close_matches(slovo, voc_words, n=2)
                        try:
                            slovo=oprava[0] #nejvíc vyhovující slovo
                            print(oprava[0]+": "+ voc_freq.get(oprava[0]), file=file_out)
                            print(oprava[1]+": "+ voc_freq.get(oprava[1]), file=file_out) #druhé nejvíc vyhovující slovo
                            """
                            #možnost nahradit slovo druhým nejvíc vyhovujícím slovem pokud je častější (nefunguje dobře ve všech případech)
                            if int(voc_freq.get(oprava[1])) > int(voc_freq.get(oprava[0])):
                                print("Slovo změněno z "+oprava[0]+" na "+oprava[1], file=file_out) 
                                slovo = oprava[1]"""
                        except TypeError:
                            print(oprava[0]+" not in voc_words", file=file_out)
                        except IndexError:
                            pass
                        print("opraveno: "+slovo, file=file_out)
        if capitals != []: #vracení velkých písmen
            for i in capitals:
                if i == 0:
                    slovo = slovo[0].upper() +slovo[1:]
                else:
                    if len(slovo)>1:
                        slovo = slovo[:i] + slovo[i].upper() + slovo[i+1:]

        slovo = prefix + slovo + sufix #vracení speciálních znaků

        print(slovo, file=file_out)
        print("", file=file_out)
        spravna_veta.append(slovo)
    
    veta = listToString(spravna_veta)
    print(split_veta, file=file_out)
    print(veta, file=file_out)

    if veta_now < veta_all:
        file_opraveno.write(veta+"\n")
    else:
        file_opraveno.write(veta+" ")
file_opraveno.close()
print("done")
