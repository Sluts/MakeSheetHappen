import urllib.request as ur
import re
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
from shutil import copyfile

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
	
	labelfin['text']="Working..."
	
	if not os.path.exists(str(save)+"/"+str(productName[0])+"/images"):
		try:
			os.mkdir(str(save)+"/"+str(productName[0]))
			os.mkdir(str(save)+"/"+str(productName[0])+"/images")
		except Exception as e:
			print(str(e))
			
	for i in imgs:
		src=re.findall(r'href="(.*?)"',i)
		for s in src:
			if "catimg" in s:
				if 'png' in s:
					try:
						images.append(s[14:-3]+"jpg")
						if op:
							#print(str(chop[0])+str(s))
							ur.urlretrieve(str(chop[0])+str(s), str(save)+"/"+str(productName[0])+"/images/"+s[14:-3]+"jpg")
							#copyfile(str(save)+"/"+str(productName[0])+"/images/"+s[14:],str(save)+"/"+str(productName[0])+"/images/"+s[14:-3]+"jpg")
					except Exception as e:
						print(str(e))
				if 'jpg' in s:
					mainimgs.append(s)
					#print(chop)
					if op:
						ur.urlretrieve(str(chop[0])+str(s.replace('&#46;', '.').replace('&#47;','/')), str(save)+
							"/"+str(productName[0])+"/images/"+s.replace('/','').replace('&#46;', '.').replace('&#47;','-'))
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
		#sku -> ean/upc, name, upc, list price
		sometimesIbreakThings[skus[i]]=[upcs[i][1], names[i], upcs[i][0], prices[i]]
		
	for sku in sometimesIbreakThings.keys():
		for img in images:
			if str(sku) in img:
				sometimesIbreakThings[sku].append(img)
				break
				
	for i in range(0,len(names)):
		if len(sometimesIbreakThings[skus[i]]) <= 4:
			sometimesIbreakThings[skus[i]].append(' ')
		sometimesIbreakThings[skus[i]].append(manufact[0])
		
		
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
						if sometimesIbreakThings[m][4]== ' ':							
							row.append('"'+manufact[0]+' '+sometimesIbreakThings[m][1][0]+' '+sometimesIbreakThings[m][1][2]+
								'"\t"'+sometimesIbreakThings[m][1][0]+' '+sometimesIbreakThings[m][1][2]+
								'"\t'+manufact[0]+"\t"+sometimesIbreakThings[m][1][1]+"\t"+sometimesIbreakThings[m][2]+
								"\t"+m+"\t"+sometimesIbreakThings[m][3]+'\t'+sometimesIbreakThings[m][4]+'\t"'+desc[0]+'"')
						else:
							row.append('"'+manufact[0]+" "+sometimesIbreakThings[m][1][0]+" "+sometimesIbreakThings[m][1][2]+
								'"\t"'+sometimesIbreakThings[m][1][0]+" "+sometimesIbreakThings[m][1][2]+
								'"\t'+manufact[0]+"\t"+sometimesIbreakThings[m][1][1]+"\t"+sometimesIbreakThings[m][2]+
								"\t"+m+"\t"+sometimesIbreakThings[m][3]+"\t"+str(save)+"/"+str(productName[0])+"/images/"+
								sometimesIbreakThings[m][4]+'\t"'+desc[0]+'"')
					else:
						if sometimesIbreakThings[m][4]== ' ':							
							row.append('"'+manufact[0]+" "+sometimesIbreakThings[m][1][0]+" "+sometimesIbreakThings[m][1][2]+
								'"\t"'+sometimesIbreakThings[m][1][0]+" "+sometimesIbreakThings[m][1][2]+
								'"\t'+manufact[0]+"\t"+sometimesIbreakThings[m][1][1]+"\t"+sometimesIbreakThings[m][2]+
								"\t"+m+"\t"+sometimesIbreakThings[m][3]+"\t"+sometimesIbreakThings[m][4]+'\t"'+desc[0]+'"')
						else:
							row.append('"'+manufact[0]+" "+sometimesIbreakThings[m][1][0]+'"\t'+sometimesIbreakThings[m][1][0]+
								"\t"+manufact[0]+"\t"+sometimesIbreakThings[m][1][1]+
								"\t"+sometimesIbreakThings[m][2]+"\t"+m+"\t"+sometimesIbreakThings[m][3]+
								"\t"+str(save)+"/"+str(productName[0])+"/images/"+
								sometimesIbreakThings[m][4]+'\t"'+desc[0]+'"')
				else:
					pass
	# for c in sometimesIbreakThings.keys():
		#print(c+" -> "+str(sometimesIbreakThings[c]))
	fh=open(str(save)+"/"+str(productName[0])+"/"+str(productName[0])+".xls","w+")
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
	entry2=ttk.Entry(sheet, textvariable=entry2var, width=len(filename)+5)
	entry2.grid(row=1, column=1)
	entry2var.set(selectedDirectory.get())
	
sheet=Tk()
#sheet.iconbitmap(sheet, default="idk.ico")
sheet.wm_title("You're in Deep Sheet")
entryvar=StringVar()
entry2var=StringVar()
selectedDirectory=StringVar()
imagevar=IntVar()

label=ttk.Label(sheet, text="URL")
label.grid(row=0, column=0)
entry=ttk.Entry(sheet, textvariable=entryvar, width=30)
entry.grid(row=0, column=1, columnspan=2, sticky=W)
label2=ttk.Label(sheet, text="idk")
#label2.grid(row=1, column=0)
button1=ttk.Button(sheet, text="Make Sheet", command=lambda:engine(entryvar.get(), entry2var.get(), imagevar.get()))
button1.grid(row=4, column=2)
button2=ttk.Button(sheet, text="browse", command=browse)
button2.grid(row=1, column=0)
label3=ttk.Label(sheet, text="Save images?")
label3.grid(row=3, column=0)
radio=ttk.Radiobutton(sheet, variable=imagevar, text="yes", value=1)
radio.grid(row=3, column=1)
radio2=ttk.Radiobutton(sheet, variable=imagevar, text="no", value=0)
radio2.grid(row=3, column=2)
labelfin=ttk.Label(sheet, text="Ready...")
labelfin.grid(row=4, column=1)


sheet.mainloop()
