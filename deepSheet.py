import urllib.request as ur
import re

names=[]
skus=[]
upcs=[]
prices=[]
images=[]
row=[]
variance={}
sometimesIbreakThings={}

url="https://www.macphersonart.com/product/137187/Artists-Watercolor.html"
#url='https://www.macphersonart.com/product/149250/Neon-Leather-Paint.html'
#url='https://www.macphersonart.com/product/132191/Artist-Bristle-Mottlers.html'
#url='https://www.macphersonart.com/product/146367/XL-Mix-Media-Pads.html'

chop=re.findall(r'(.*?[c][o][m])[/]', url)

response=ur.urlopen(url)
data=response.read().decode("utf-8", errors="ignore")
imgs=re.findall(r'<a(.*?)>',data)
divs=re.findall(r'<div>(.*?)</div>', data)
upc=re.findall(r'<div class="(.*?)</div>', data)
desc=re.findall(r'<div class="prodDescription">(.*?)</div>', data)
productName=re.findall(r'<div class="familyTitle">(.*?)</div>', data)
manufact=re.findall(r'<div class=\"millDescription\">[ \n \v \r\n]*.*?>(.*?)</a>', data)


for i in imgs:
	src=re.findall(r'href="(.*?)"',i)
	for s in src:
		if "catimg" in s:
			if 'png' in s:
				try:
					images.append(s[14:])
					#print(str(chop)+str(s))
					#ur.urlretrieve(str(chop)+str(s), str(save)+s[14:])
				except Exception as e:
					print(str(e))


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
		if not sometimesIbreakThings[k][1][0] in variance:
			variance[sometimesIbreakThings[k][1][0]]=[sometimesIbreakThings[k][1][1]]
		else:
			variance[sometimesIbreakThings[k][1][0]].append(sometimesIbreakThings[k][1][1])



for c in variance.keys():
	# print(c+" -> "+str(variance[c]))
	for m in sometimesIbreakThings.keys():
		if c in sometimesIbreakThings[m][1]:
			if len(sometimesIbreakThings[m][1]) > 2:
				row.append(manufact[0]+" "+sometimesIbreakThings[m][1][0]+" "+sometimesIbreakThings[m][1][2]+
					","+sometimesIbreakThings[m][1][0]+" "+sometimesIbreakThings[m][1][2]+
					","+manufact[0]+","+sometimesIbreakThings[m][1][1]+","+sometimesIbreakThings[m][2]+
					","+m+","+sometimesIbreakThings[m][3]+","+sometimesIbreakThings[m][4])
			else:
				row.append(manufact[0]+" "+sometimesIbreakThings[m][1][0]+","+sometimesIbreakThings[m][1][0]+
					","+manufact[0]+","+sometimesIbreakThings[m][1][1]+
					","+sometimesIbreakThings[m][2]+","+m+","+sometimesIbreakThings[m][3]+
					","+sometimesIbreakThings[m][4])

# for c in sometimesIbreakThings.keys():
	#print(c+" -> "+str(sometimesIbreakThings[c]))
fh=open("test.xls","w+")
for r in row:
	print(r)
	fh.write(r+"\n")
fh.close()
