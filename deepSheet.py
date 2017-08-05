import urllib.request as ur
import re
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
from shutil import copyfile
#fh.write('ProductName\tProductType\tManufacturer\tDistributor\tCategory1\tCategory2\tCategory3\tCategory4\tSection1\tSection2\tSection3\tSection4\tSummary\tDescription\tSEKeywords\tSEDescription\tSETitle\tSKU\tManufacturerPartNumber\tXmlPackage\tColWidth\tSalesPromptID\tPublished\tRequiresRegistration\tRelatedProducts\tMiscText\tTrackInventoryBySizeAndColor\tTrackInventoryBySize\tTrackInventoryByColor\tIsKit\tIsAPack\tPackSize\tImageFilenameOverride\tExtensionData\tSEAltText\treserved1\tVariantName\tVariantIsDefault\tVariantSkuSuffix\tVariantManufacturerPartNumber\tVariantDescription\tVariantSeKeywords\tVariantSeDescription\tVariantSeTitle\tPrice\tPriceSale\tPriceMsrp\tPriceCost\tWeight\tDimensions\tInventory\tDisplayOrder\tColors\tColorSKUModifiers\tSize\tSizeSkuModifier\tIsTaxable\tIsShipSeparately\tIsDownload\tDownloadLocation\tVariantPublished\tVariantImageFilenameOverride\tVariantExtensionData\tVariantSeAltText\tSpecialtyStore\tAmazonProdName\tProductBigImage\tProductImagePath\tProductCode\tIsProp65\tProductSpecFile\tidAttrib\tidProdAttrib\tAttribType\tAttribCode\tAttribName\tThumbImage\tAttribImagePath\tAttribSpecFile\tAmazonImagePath\tAmazonImagePathAlt\tShipCost\tIdAmazonType\tExport\tPaintTypes\tSearchTerms\tUsedFor\tTargetAudiences\tTaxCode\tStartDate\tEndDate\tGUID\tHazardUnitsPerCase\tHazardCostPerCase\tStoreID\tColumn1\n'

names=[]
skus=[]
upcs=[]
prices=[]
images=[]
row=[]
variance={}
sibt={}

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
					if op:
						ur.urlretrieve(str(chop[0])+str(s.replace('&#46;', '.').replace('&#47;','/')), str(save)+
							"/"+str(productName[0])+"/images/"+s.replace('/','').replace('&#46;', '.').replace('&#47;','-'))
						#print(s.replace('&#46;', '.').replace('&#47;','/'))

	for d in divs:
		if "<br/>" in d:
			names.append(d.replace('<br/>', ' ').split(', '))
			#print(names)
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
		sibt[skus[i]]=[upcs[i][1], names[i], upcs[i][0], prices[i]]
		
	for sku in sibt.keys():
		for img in images:
			if str(sku) in img:
				sibt[sku].append(img)
				break
				
	for i in range(0,len(names)):
		if len(sibt[skus[i]]) <= 4:
			sibt[skus[i]].append(' ')
		sibt[skus[i]].append(manufact[0])
		
		
	for k in sibt.keys():
		if len(sibt[k][1]) > 2:
			#print(k+" -> "+str(sibt[k])+"\n")
			if not sibt[k][1][2] in variance:
				variance[sibt[k][1][2]]=[sibt[k][1][1]]
			else:
				variance[sibt[k][1][2]].append(sibt[k][1][1])
		else:
			#print(k+" -> "+str(sibt[k])+"\n")
			if not sibt[k][1][0] in variance:
				variance[sibt[k][1][0]]=[sibt[k][1][1]]
			else:
				variance[sibt[k][1][0]].append(sibt[k][1][1])

	used=[]
#sibt=[upc/ean, name, UPC, list price, img, manufact]
	for c in variance.keys():
		#print(c+" -> "+str(variance[c]))
		for m in sibt.keys():
			#print(sibt[m])
			if c in sibt[m][1]:
				if not m in used:
					used.append(m)
					if len(sibt[m][1]) > 2:
						vname=sibt[m][1][2]+' '+sibt[m][1][1]
					else:
						vname=sibt[m][1][1]
					if sibt[m][4]== ' ':
						ig=' '
					else:
						ig=str(save)+"/"+str(productName[0])+"/images/"+str(sibt[m][4])
					try:		
						row.append('"'+manufact[0]+' '+sibt[m][1][0]+'"\t'+
							str(ptype.get())+'\t'+manufact[0]+'\t'+distributor.get()+'\t'+depart.get()+'\t'+
							'\t\t\t'+depart.get()+'\t\t\t\t\t'+desc[0]+'\t'+sevar.get()+'\t'+desc[0]+'\t'+
							manufact[0]+' '+sibt[m][1][0]+' '+vname+'\t'+skuvar.get()+'\t'+sibt[m][2]+'\t'+
							'\t0\t0\t1\t0\t\t\t0\t0\t0\t0\t0\t0\t'+ig+'\t\t'+manufact[0]+' '+sibt[m][1][0]+'\t\t'+
							vname+'\t0\t'+m+'\t'+sibt[m][2]+'\t"'+
							desc[0]+'"\t'+sevar.get()+'\t'+desc[0]+'\t'+manufact[0]+' '+sibt[m][1][0]+' '+vname+'\t'+
							str(float(sibt[m][3])-(float(discount.get())*float(sibt[m][3])))+'\t0'+
							'\t'+sibt[m][3]+'\t0\t0\t\t'+inv.get()+'\t\t\t'+
							'\t\t\t0\t0\t0\t\t1\t'+ig+'\t\t\t\t'+manufact[0]+' '+sibt[m][1][0]+' '+vname+
							'\t\t\t\t0\t\t\t\t0\t\t\t'+ig+'\t\t\t'+ig+'\t'+ig+'\t0\t0\t\t'+
							paint.get()+'\t'+sevar.get()+'\t\tArtist\'s\tA_GEN_TAX\t\t\t\t\t\t\t\t\n')	
					except Exception as e:
						print(str(e))
				else:
					pass
	# for c in sibt.keys():
		#print(c+" -> "+str(sibt[c]))
	fh=open(str(save)+"/"+str(productName[0])+"/"+str(productName[0])+".xls","w+")
	fh.write('ProductName\tProductType\tManufacturer\tDistributor\tCategory1\t'+
		'Category2\tCategory3\tCategory4\tSection1\tSection2\tSection3\tSection4\t'+
		'Summary\tDescription\tSEKeywords\tSEDescription\tSETitle\tSKU\tManufacturerPartNumber\t'+
		'XmlPackage\tColWidth\tSalesPromptID\tPublished\tRequiresRegistration\tRelatedProducts\t'+
		'MiscText\tTrackInventoryBySizeAndColor\tTrackInventoryBySize\tTrackInventoryByColor\t'+
		'IsKit\tIsAPack\tPackSize\tImageFilenameOverride\tExtensionData\tSEAltText\treserved1\t'+
		'VariantName\tVariantIsDefault\tVariantSkuSuffix\tVariantManufacturerPartNumber\t'+	
		'VariantDescription\tVariantSeKeywords\tVariantSeDescription\tVariantSeTitle\tPrice\t'+
		'PriceSale\tPriceMsrp\tPriceCost\tWeight\tDimensions\tInventory\tDisplayOrder\tColors\t'+
		'ColorSKUModifiers\tSize\tSizeSkuModifier\tIsTaxable\tIsShipSeparately\tIsDownload\t'+
		'DownloadLocation\tVariantPublished\tVariantImageFilenameOverride\tVariantExtensionData\t'+
		'VariantSeAltText\tSpecialtyStore\tAmazonProdName\tProductBigImage\tProductImagePath\t'+
		'ProductCode\tIsProp65\tProductSpecFile\tidAttrib\tidProdAttrib\tAttribType\t'+
		'AttribCode\tAttribName\tThumbImage\tAttribImagePath\tAttribSpecFile\tAmazonImagePath\t'+
		'AmazonImagePathAlt\tShipCost\tIdAmazonType\tExport\tPaintTypes\tSearchTerms\tUsedFor\t'+
		'TargetAudiences\tTaxCode\tStartDate\tEndDate\tGUID\tHazardUnitsPerCase\t'+
		'HazardCostPerCase\tStoreID\tColumn1\n')
		
	fh.write(manufact[0]+' '+productName[0]+'\t'+str(ptype.get())+'\t'+manufact[0]+'\t'+distributor.get()+'\t'+depart.get()+'\t'+
		'\t\t\t'+depart.get()+'\t\t\t\t\t'+desc[0]+'\t'+sevar.get()+'\t'+desc[0]+
		'\t'+manufact[0]+' '+productName[0]+'\t'+skuvar.get()+'\t\t'+xml.get()+'\t0\t0\t1\t0\t\t\t0\t0\t0\t0\t0\t0\t'+str(save)+"/"+str(productName[0])+"/images/"+mainimgs[0].replace('/','').replace('&#46;', '.').replace('&#47;','-')+
		'\t\t'+manufact[0]+' '+productName[0]+'\t\t\t0\t\t\t'+desc[0]+'\t'+sevar.get()+'\t'+desc[0]+'\t'+
		manufact[0]+' '+productName[0]+'\t\t0\t\t0\t0\t\t'+inv.get()+'\t\t\t\t\t\t0\t0\t0\t\t1\t'+
		'\t\t\t\t'+manufact[0]+' '+productName[0]+'\t'+
		str(save)+"/"+str(productName[0])+"/images/"+mainimgs[1].replace('/','').replace('&#46;', '.').replace('&#47;','-')+'\t'+
		'\t\t0\t\t\t\t0\t\t\t'+str(save)+"/"+str(productName[0])+"/images/"+mainimgs[0].replace('/','').replace('&#46;', '.').replace('&#47;','-')+
		'\t\t\t\t\t0\t0\t\t'+paint.get()+'\t'+sevar.get()+'\t\tArtist\'s\tA_GEN_TAX\t\t\t\t\t\t\t\t\n')
	
	for r in row:
		#print(r+"\n")
		try:
			fh.write(r)
		except Exception as e:
			print(str(e))
	fh.close()
	done()

def done():
	labelfin['text']="Done!"
	return

def browse():
	filename = filedialog.askdirectory(initialdir='.')
	entry2var.set(filename)
	
sheet=Tk()
#sheet.iconbitmap(sheet, default="idk.ico")
sheet.wm_title("You're in Deep Sheet")
entryvar=StringVar()
entry2var=StringVar()
selectedDirectory=StringVar()
depart=StringVar()
depart.set("")
skuvar=StringVar()
xml=StringVar()
inv=StringVar()
discount=StringVar()
sevar=StringVar()
ptype=StringVar()
paint=StringVar()
ptype.set("1")
distributor=StringVar()
distributor.set('Rochester Art Supply')
imagevar=IntVar()

label=ttk.Label(sheet, text="URL")
label.grid(row=0, column=0, sticky=E)
entry=ttk.Entry(sheet, textvariable=entryvar, width=30)
entry.grid(row=0, column=1)
label2=ttk.Label(sheet, text="Department")
label2.grid(row=3, column=0, sticky=E)
entry3=ttk.Entry(sheet, textvariable=depart, width=30)
entry3.grid(row=3, column=1)
button1=ttk.Button(sheet, text="Make Sheet", command=lambda:engine(entryvar.get(), entry2var.get(), imagevar.get()))
button1.grid(row=0, column=6)
button2=ttk.Button(sheet, text="browse", command=browse)
button2.grid(row=1, column=0)
label3=ttk.Label(sheet, text="Save images?")
label3.grid(row=5, column=0)
radio=ttk.Radiobutton(sheet, variable=imagevar, text="yes", value=1)	
radio.grid(row=5, column=1)
radio2=ttk.Radiobutton(sheet, variable=imagevar, text="no", value=0)
radio2.grid(row=5, column=2)
labelfin=ttk.Label(sheet, text="Ready...")
labelfin.grid(row=0, column=5)
spin1=Spinbox(sheet, from_=0, to=10, textvariable=ptype, width=9)
spin1.grid(row=1, column=3)
label4=ttk.Label(sheet, text="Product Type")
label4.grid(row=1, column=2, sticky=E)
label5=ttk.Label(sheet, text="XML Package")
label5.grid(row=0, column=2, sticky=E)
option1=ttk.OptionMenu(sheet, xml, "Product.VariantsInTableORderFormrf.xml.config", "Product.VariantsInTableORderFormrf.xml.config", "Product.NoVariantRf.Xml.Config", "Product.NoVariantRf2.Xml.Config", "pack4")
option1.grid(row=0, column=3, columnspan=2)
label6=ttk.Label(sheet, text="Sku")
label6.grid(row=2, column=2, sticky=E)
entry4=ttk.Entry(sheet, textvariable=skuvar, width=10)
entry4.grid(row=2, column=3)
label7=ttk.Label(sheet, text="Discount")
label7.grid(row=3, column=2, sticky=E)
option2=ttk.OptionMenu(sheet, discount, "0", "0", ".10", ".15", ".20", ".25", ".30", ".40", ".45", ".50", ".55", ".60", ".65", ".70", ".75", ".80", ".85", ".90")
option2.grid(row=3, column=3, columnspan=2)
label8=ttk.Label(sheet, text="SEKeywords")
label8.grid(row=2, column=0, sticky=E)
entry5=ttk.Entry(sheet, textvariable=sevar, width=30)
entry5.grid(row=2, column=1)
label9=ttk.Label(sheet, text="Inventory")
label9.grid(row=4, column=0, sticky=E)
entry6=ttk.Entry(sheet, textvariable=inv, width=30)
entry6.grid(row=4, column=1)
label10=ttk.Label(sheet, text="Paint Type")
label10.grid(row=4, column=2, sticky=E)
entry7=ttk.OptionMenu(sheet, paint, "", " ", "Oil", "Acrylic", "Specialty", "Watercolor", "Pastel", "Enkaustic", "Leather")
entry7.grid(row=4, column=3)
entry2=ttk.Entry(sheet, textvariable=entry2var, width=30)
entry2.grid(row=1, column=1)




sheet.mainloop()
