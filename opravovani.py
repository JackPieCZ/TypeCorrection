import re
import difflib

filename="D:\programy\SIVT 2020\syn2015_word_utf8.tsv"
file = open(filename, "r", encoding="utf8")
voc=[]

def file_len(fname):
    with open(fname, "r", encoding="utf8") as f:
        for i, l in enumerate(f):
            pass
    return i+1

def listToString(s):  
    str1 = " "  
    return (str1.join(s)) 

def find_all(s, ch):
	occurences=[]
	for i, ltr in (enumerate(s)):
		if ltr == ch:
			occurences.append(i)
	return(occurences)
    
for _ in range(file_len(filename)):
	raw_line=file.readline()
	split_line=re.split(r'\t+', raw_line)
	voc.append(split_line[1].lower())
for i in range(0,10000):
	voc.append(str(i))
user_slovnik = ["fonologii","algebraickou","nematematických","linguistics","Praha","jazykovědnou","hláskosloví","grafematika", "vowel","length",
'samohláskové', 'samohláskové', 'archaismus', 'kamének', 'popř', 'hláskových', 'dešť', 'opásá', 'odvozovací', 'vídává', 'krámského', 
'occurrence', 'phonemes', 'languages', 'possessing', 'identical', 'structure', 'samohláskovou', 'grapheme', 'combinations', 'kombinatorická', 'nejčetnějších', 
'horecký', 'trechčlennyje', 'gruppy', 'soglasnych', 'načale', 'slovackom', 'jazyke', 'souhláskové', 'vypočítávané', 'buzássyová', 'attempt', 'calculus', 
'phonological', 'mluvnickou', 'homonymií', 'těšitelové', 'vyskazyvanija', 'materiale', 'omonimii', 'slovoform', 'imen', 'suščestvitel’nych', 'češskom', 
'mluvnická', 'homonymie', 'slovníková', 'homonymní','nekotorych', 'problemach', 'aktual’nogo', 'členenija', 'skladebních', 'contextual', 'constraints', 
'semantic', 'lexical','aspects', 'categorial', 'transformational', 'grammars','slovosledem', 'přísudkového', 'construct', 'classes', 'přechodníkové', 
'nerozeznávají', 'naloviv', 'slovesně', 'jmenná', 'nalovení', 'strojovému', 'sgalla', 'mluvnického', 'převodním', 'piťhy', 'co-ordinate', 'conjunctions',
'panevové', 'nesoglasovannoje', 'opredelenije', 'točki', 'zrenija', 'analiza', 'dlja', 'mašinnogo', 'perevoda', 'neshodný', 'neshodného', 'cyklostylovaný', 
'korvasová', 'štindlová', 'jazykovědného', 'palka','morfematická', 'štruktúra', 'slovenčiny','jazykovědný', 'morfémů','sborníkem', 'königová','postala', 'saS',
'markovskými', 'čtyřstopý', 'trochej', 'satanela', 'čtyřstopý', 'jamb','sylabotonického', 'čsAV', 'heyduk', 'jařaba', 'pasose', 'uSA','československo-polské', 
'paN','informativními', 'statěmi', 'horeckého', 'jazykoveda', 'shannonův', 'těšitelová', 'těšitelová','čsSR', 'referátovou', 'gramatikách','navazujíc']
for i in user_slovnik:
	voc.append(i)


for _ in range(1):
	veta=input("")
	spravna_veta=[]
	split_veta=veta.split()
	chyby=[]

	for slovo in split_veta:
		TITUL = -1
		ZAVORKAa = -1
		ZAVORKAb = -1
		TECKA = -1
		CARKA = -1
		STREDNIK = -1
		DVOJTECKA = -1
		TECKA3 = -1
		UVOZOVKYa = -1
		UVOZOVKYb = -1

		if (slovo[0].isupper()):
			TITUL = 1
			slovo = slovo[0].lower()+slovo[1:]
		if len(slovo)>1:
			if (slovo[1].isupper()):
				TITUL = 1
				slovo = slovo[0]+slovo[1].lower()+slovo[2:]
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
		
			
		slovo = slovo.replace("(","")
		slovo = slovo.replace(")","")
		slovo = slovo.replace(".","")
		slovo = slovo.replace(",","")
		slovo = slovo.replace(";","")
		slovo = slovo.replace(":","")
		slovo = slovo.replace("…","")
		slovo = slovo.replace("„","")
		slovo = slovo.replace("“","")

		if slovo not in voc:
			try:
				if (slovo[-2].isnumeric() and slovo[-1] == "n") is False:
					chyby.append(slovo)
					oprava=difflib.get_close_matches(slovo,voc,1)[0]
					slovo = oprava
			except:
				pass
		
		if TITUL == 1:
			slovo = slovo.title()
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
				slovo = slovo+","
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
		spravna_veta.append(slovo)
	
	
	veta = listToString(spravna_veta)
	print(veta)
	
