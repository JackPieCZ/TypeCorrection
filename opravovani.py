import re
import difflib
import os

here = os.path.dirname(os.path.abspath(__file__))

def listToString(s):  
    str1 = " "  
    return (str1.join(s)) 

def find_all(s, ch):
	occurences=[]
	for i, ltr in (enumerate(s)):
		if ltr == ch:
			occurences.append(i)
	return(occurences)


file1=os.path.join(here, "syn2015_word_utf8.tsv")
vocabulary = open(file1, "r", encoding="utf8")
voc=[]
raw_line = vocabulary.readline()
while raw_line:
	split_line=re.split(r'\t+', raw_line)
	voc.append(split_line[1].lower())
	raw_line=vocabulary.readline()
for i in range(0,20000):
	voc.append(str(i))

file2=os.path.join(here,"voda_errors.txt")
file_chyby = open(file2, "r", encoding="utf8")
na_opravu=[]
raw_line = file_chyby.readline()
while raw_line:
	na_opravu.append(raw_line)
	raw_line=file_chyby.readline()

user_slovnik = ['abode', 'aquifer', 'aquiferů', 'argyre', 'bazaltovém', 
'canali', 'canals', 'celoplanetárním', 'cerberus',  'crism', "čepiček", 'erodovaných', 'erozivní', 'evaporaci', 'fossae', 'gusev', 
'hesperianu', 'hydrosféry', 'impaktních', 'impaktů', 'kryosféry', 'kryosféře', "m3.s−1", "ma'adim", 'mariner', 'marineris', 
'marsovské', "marsovský",'marsovského', 'meridiani', 'mola', 'montes', 'napovídající', 'nasa', 'naskytuje', 'neutronovým', 'noachianu', 
'noachis', 'oceanus', 'painted', 'palagonit', 'permafrostem', 'planitia', 'polotekuté', 'reconnaissance', 'regolitu', 'roztáním', 
'sedimentovat', 'sesutím', 'sezónního', 'skupenstvích', 'sojourner', 'spektrometrem', 'spektrometrických', 'spektroskopické', 'sublimoval', 
"sureyor",'surveyor', 'svahového', 'svrchnějších', 'terraformace', 'transportované', 'trojného', 'ustávání', 'vallis', 'vastitas', 
'vysočin', 'vysočinami', 'vysychajících','whewell', 'zarovnány', 'zařezávání', 'zbrázděn', 'zlomkovou']
for wd in user_slovnik:
	voc.append(wd)

file3=os.path.join(here,"voda_opraveno.txt")
file_opraveno = open(file3, "w", encoding="utf8")

file4=os.path.join(here,"script_output.txt")
file_out = open(file4, "w", encoding="utf8")

veta_now = 0
veta_all = len(na_opravu)
for veta in na_opravu:
	veta_now +=1
	print(str(veta_now)+"/"+str(veta_all), end="\r")
	spravna_veta=[]
	split_veta=veta.split()
	for slovo in split_veta:
		print(slovo, file=file_out)
		TITUL = []
		ZAVORKAa = -1
		ZAVORKAb = -1
		TECKA = -1
		CARKA = -1
		OTAZNIK = -1
		VYKRICNIK = -1
		STREDNIK = -1
		DVOJTECKA = -1
		TECKA3 = -1
		UVOZOVKYa = -1
		UVOZOVKYb = -1
		POMLCKA = -1
		KRAT = -1
		PROCENTO = -1
		VLNOVKA = -1
		ROVNASE = -1
		STUPEN = -1

		indexT=0
		for ch in slovo:
			if ch.istitle():
				TITUL.append(indexT)
			indexT+=1
		if "(" in slovo:
			ZAVORKAa = find_all(slovo,"(")
		if ")" in slovo:
			ZAVORKAb = find_all(slovo,")")
		if "." in slovo:
			TECKA = find_all(slovo,".")
		if "," in slovo:
			CARKA = find_all(slovo,",")
		if ";" in slovo:
			STREDNIK = find_all(slovo,";")
		if ":" in slovo:
			DVOJTECKA = find_all(slovo,":")
		if "…" in slovo:
			TECKA3 = find_all(slovo,"…")
		if "„" in slovo:
			UVOZOVKYa = find_all(slovo,"„")
		if "“" in slovo:
			UVOZOVKYb = find_all(slovo,"“")
		if "?" in slovo:
			OTAZNIK = find_all(slovo,"?")
		if "!" in slovo:
			VYKRICNIK = find_all(slovo,"!")
		if "–" in slovo:
			POMLCKA = find_all(slovo,"–")
		if "×" in slovo:
			KRAT = find_all(slovo,"×")
		if "%" in slovo:
			PROCENTO = find_all(slovo,"%")
		if "~" in slovo:
			VLNOVKA = find_all(slovo,"~")
		if "=" in slovo:
			ROVNASE = find_all(slovo,"=")
		if "°" in slovo:
			STUPEN = find_all(slovo,"°")
		
		if TITUL!= []:
			slovo = slovo.lower()
		slovo = slovo.replace("(","")
		slovo = slovo.replace(")","")
		slovo = slovo.replace(".","")
		slovo = slovo.replace(",","")
		slovo = slovo.replace(";","")
		slovo = slovo.replace(":","")
		slovo = slovo.replace("…","")
		slovo = slovo.replace("„","")
		slovo = slovo.replace("“","")
		slovo = slovo.replace("?","")
		slovo = slovo.replace("!","")
		slovo = slovo.replace("–","")
		slovo = slovo.replace("×","")
		slovo = slovo.replace("%","")
		slovo = slovo.replace("~","")
		slovo = slovo.replace("=","")
		slovo = slovo.replace("°","")

		if slovo not in voc:
			if slovo.isnumeric() is False:
				if len(slovo)==0:
					slovo=""
				else:
					print("Chyba: "+slovo, file=file_out)
					oprava = difflib.get_close_matches(slovo, voc, n=1)
					slovo=oprava[0]
					print("opraveno: "+slovo, file=file_out)

		if ZAVORKAa != -1:
			for delitel in ZAVORKAa:
				slovo = slovo[:delitel]+"("+slovo[delitel:]
		if ZAVORKAb != -1:
			for delitel in ZAVORKAb:
				slovo = slovo[:delitel]+")"+slovo[delitel:]
		if TECKA != -1:
			for delitel in TECKA:
				slovo = slovo[:delitel]+"."+slovo[delitel:]
		if CARKA != -1:
			for delitel in CARKA:
				slovo = slovo[:delitel]+","+slovo[delitel:]
		if STREDNIK != -1:
			for delitel in STREDNIK:
				slovo = slovo[:delitel]+";"+slovo[delitel:]
		if DVOJTECKA != -1:
			for delitel in DVOJTECKA:
				slovo = slovo[:delitel]+":"+slovo[delitel:]
		if TECKA3 != -1:
			for delitel in TECKA3:
				slovo = slovo[:delitel]+"…"+slovo[delitel:]
		if UVOZOVKYa != -1:
			for delitel in UVOZOVKYa:
				slovo = slovo[:delitel]+"„"+slovo[delitel:]
		if UVOZOVKYb != -1:
			for delitel in UVOZOVKYb:
				slovo = slovo[:delitel]+"“"+slovo[delitel:]
		if OTAZNIK != -1:
			for delitel in OTAZNIK:
				slovo = slovo+"?"
		if VYKRICNIK != -1:
			for delitel in VYKRICNIK:
				slovo = slovo+"!"
		if VLNOVKA != -1:
			for delitel in VLNOVKA:
				slovo = slovo[:delitel]+"~"+slovo[delitel:]
		if KRAT != -1:
			for delitel in KRAT:
				slovo = slovo[:delitel]+"×"+slovo[delitel:]
		if POMLCKA != -1:
			for delitel in POMLCKA:
				slovo = slovo[:delitel]+"–"+slovo[delitel:]
		if PROCENTO != -1:
			for delitel in PROCENTO:
				slovo = slovo[:delitel]+"%"+slovo[delitel:]
		if ROVNASE != -1:
			for delitel in ROVNASE:
				slovo = slovo[:delitel]+"="+slovo[delitel:]
		if STUPEN != -1:
			for delitel in STUPEN:
				slovo = slovo[:delitel]+"°"+slovo[delitel:]
		if TITUL != []:
			for delitel in TITUL:
				if delitel == 0:
					slovo = slovo.title()
				else:
					if len(slovo)>1:
						slovo = slovo[:delitel] + slovo[delitel].upper() + slovo[delitel+1:]
		
		print(slovo, file=file_out)
		print("", file=file_out)
		spravna_veta.append(slovo)
	
	veta = listToString(spravna_veta)
	print(split_veta, file=file_out)
	print(veta, file=file_out)
	file_opraveno.write(veta+"\n")
file_opraveno.close()
print("done")