import re
import difflib

filename='syn2015_word_utf8.tsv'
file = open(filename, "r", encoding="utf8")
voc=[]

def file_len(fname):
    with open(fname, "r", encoding="utf8") as f:
        for i, l in enumerate(f):
            pass
    return i+1
    
for _ in range(file_len(filename)):
	raw_line=file.readline()
	split_line=re.split(r'\t+', raw_line)
	voc.append(split_line[1].lower())
while (True):
	spravna_veta=""
	error=0
	chyby=[]
	veta=input("Vložte větu ke kontrole: ").lower()
	print("Vložená věta: ",veta)
	split_veta=veta.split()

	for slovo in split_veta:
		if slovo in voc:
			spravna_veta=spravna_veta+" "+slovo
		if slovo not in voc:
			error=1
			chyby.append(slovo)
			oprava=difflib.get_close_matches(slovo,voc,1)[0]
			spravna_veta=spravna_veta+" "+oprava
			
	if error==0:
		print("Vše je v pořádku.")
	elif error==1:
		print("Ve větě je chyba ve slovech ",chyby)
		print("Opravená věta je:",spravna_veta)
	print("")
