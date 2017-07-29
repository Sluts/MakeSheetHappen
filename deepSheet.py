import urllib.request as ur
import re
from tkinter import *
from tkinter import filedialog
import os
names=[]
skus=[]
upcs=[]
prices=[]
images=[]
row=[]
variance={}
sometimesIbreakThings={}

#url="https://www.macphersonart.com/product/137187/Artists-Watercolor.html"
#url='https://www.macphersonart.com/product/149250/Neon-Leather-Paint.html'
#url='https://www.macphersonart.com/product/132191/Artist-Bristle-Mottlers.html'
#url='https://www.macphersonart.com/product/146367/XL-Mix-Media-Pads.html'

def engine(url, save, op):
	chop=re.findall(r'(.*?[c][o][m])[/]', url)

	response=ur.urlopen(url)
	data=response.read().decode("utf-8", errors="ignore")
	imgs=re.findall(r'<a(.*?)>',data)
	divs=re.findall(r'<div>(.*?)</div>', data)
	upc=re.findall(r'<div class="(.*?)</div>', data)
	desc=re.findall(r'<div class="prodDescription">(.*?)</div>', data)
	productName=re.findall(r'<div class="familyTitle">(.*?)</div>', data)
	manufact=re.findall(r'<div class=\"millDescription\">[ \n \v \r\n]*.*?>(.*?)</a>', data)
	mainimgs=[]
	
	labelfin['text']="Ready?"
	
	if not os.path.exists(str(save)+"/"+str(manufact[0])+"/images"):
		try:
			os.mkdir(str(save)+"/"+str(manufact[0]))
			os.mkdir(str(save)+"/"+str(manufact[0])+"/images")
		except Exception as e:
			print(str(e))
			
	for i in imgs:
		src=re.findall(r'href="(.*?)"',i)
		for s in src:
			if "catimg" in s:
				if 'png' in s:
					try:
						images.append(s[14:])
						if op:
							#print(str(chop[0])+str(s))
							ur.urlretrieve(str(chop[0])+str(s), str(save)+"/"+str(manufact[0])+"/images/"+s[14:])
					except Exception as e:
						print(str(e))
				if 'jpg' in s:
					mainimgs.append(s)
					#print(chop)
					ur.urlretrieve(str(chop[0])+str(s.replace('&#46;', '.').replace('&#47;','/')), str(save)+
						"/"+str(manufact[0])+"/images/"+s.replace('/','').replace('&#46;', '.').replace('&#47;','-'))
					#print(s.replace('&#46;', '.').replace('&#47;','/'))

	for d in divs:
		if "<br/>" in d:
			names.append(d.replace('<br/>', ' ').split(', '))
		elif "itemNumColText" in d:
			skus.append(d.replace(' ','')[27:])
		else:
			pass
		
	for u in upc:
		if 'eanCode' in u:
			upcs.append((u[11:], 'ean'))
			#print(u[11:])
		elif 'upcCode' in u:
			upcs.append((u[11:], 'upc'))
			#print(u[11:])
		elif 'RegPrice' in u:
			#print(u[u.find('>')+2:])
			prices.append(u[u.find('>')+2:])
		else:
			pass

	for i in range(0,len(names)):
		#upc -> ean/upc, name, sku, list price, image, manufact
		if len(images) >= 1:
			sometimesIbreakThings[upcs[i][0]]=[upcs[i][1],names[i],skus[i], prices[i], images[i], manufact[0]]
		else:
			sometimesIbreakThings[upcs[i][0]]=[upcs[i][1],names[i],skus[i], prices[i], '', manufact[0]]


	for k in sometimesIbreakThings.keys():
		if len(sometimesIbreakThings[k][1]) > 2:
			#print(k+" -> "+str(sometimesIbreakThings[k])+"\n")
			if not sometimesIbreakThings[k][1][2] in variance:
				variance[sometimesIbreakThings[k][1][2]]=[sometimesIbreakThings[k][1][1]]
			else:
				variance[sometimesIbreakThings[k][1][2]].append(sometimesIbreakThings[k][1][1])
		else:
			#print(k+" -> "+str(sometimesIbreakThings[k])+"\n")
			if not sometimesIbreakThings[k][1][0] in variance:
				variance[sometimesIbreakThings[k][1][0]]=[sometimesIbreakThings[k][1][1]]
			else:
				variance[sometimesIbreakThings[k][1][0]].append(sometimesIbreakThings[k][1][1])

	used=[]

	for c in variance.keys():
		#print(c+" -> "+str(variance[c]))
		for m in sometimesIbreakThings.keys():
			if c in sometimesIbreakThings[m][1]:
				if not m in used:
					used.append(m)
					if len(sometimesIbreakThings[m][1]) > 2:
						row.append("'"+manufact[0]+" "+sometimesIbreakThings[m][1][0]+" "+sometimesIbreakThings[m][1][2]+
							"','"+sometimesIbreakThings[m][1][0]+" "+sometimesIbreakThings[m][1][2]+
							"',"+manufact[0]+","+sometimesIbreakThings[m][1][1]+","+sometimesIbreakThings[m][2]+
							","+m+","+sometimesIbreakThings[m][3]+","+sometimesIbreakThings[m][4]+",'"+desc[0]+"'")
					else:
						row.append(manufact[0]+" "+sometimesIbreakThings[m][1][0]+","+sometimesIbreakThings[m][1][0]+
							","+manufact[0]+","+sometimesIbreakThings[m][1][1]+
							","+sometimesIbreakThings[m][2]+","+m+","+sometimesIbreakThings[m][3]+
							","+sometimesIbreakThings[m][4]+",'"+desc[0]+"'")
				else:
					pass
	# for c in sometimesIbreakThings.keys():
		#print(c+" -> "+str(sometimesIbreakThings[c]))
	fh=open(str(save)+"/"+str(manufact[0])+"/"+str(manufact[0])+".xls","w+")
	for r in row:
		#print(r+"\n")
		fh.write(r+"\n")
	fh.close()
	done()

def done():
	labelfin['text']="Done!"
	return

def browse():
	filename = filedialog.askdirectory(initialdir='.')
	selectedDirectory.set(filename)
	entry2=Entry(sheet, textvariable=entry2var, width=len(filename))
	entry2.grid(row=1, column=1)
	entry2var.set(selectedDirectory.get())
	
sheet=Tk()
sheet.wm_title("You're in Deep Sheet")
entryvar=StringVar()
entry2var=StringVar()
selectedDirectory=StringVar()
imagevar=IntVar()

label=Label(sheet, text="URL")
label.grid(row=0, column=0)
entry=Entry(sheet, textvariable=entryvar)
entry.grid(row=0, column=1)
label2=Label(sheet, text="idk")
#label2.grid(row=1, column=0)
button1=Button(sheet, text="Make Sheet", command=lambda:engine(entryvar.get(), entry2var.get(), imagevar.get()))
button1.grid(row=4, column=2)
button2=Button(sheet, text="browse", command=browse)
button2.grid(row=1, column=0)
label3=Label(sheet, text="Save images?")
label3.grid(row=3, column=0)
radio=Radiobutton(sheet, variable=imagevar, text="yes", value=1)
radio.grid(row=3, column=1)
radio2=Radiobutton(sheet, variable=imagevar, text="no", value=0)
radio2.grid(row=3, column=2)
labelfin=Label(sheet, text="Ready?")
labelfin.grid(row=4, column=0)


sheet.mainloop()
