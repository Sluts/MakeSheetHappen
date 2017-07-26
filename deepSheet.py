import urllib.request as ur
import re
names=[]
skus=[]
upcs=[]
prices=[]

sometimesIbreakThings={}
#url="https://www.macphersonart.com/product/137187/Artists-Watercolor.html"
#url='https://www.macphersonart.com/product/149250/Neon-Leather-Paint.html'
url='https://www.macphersonart.com/product/132191/Artist-Bristle-Mottlers.html'

response=ur.urlopen(url)
data=response.read().decode("utf-8", errors="ignore")

divs=re.findall(r'<div>(.*?)</div>', data)
upc=re.findall(r'<div class="(.*?)</div>', data)
desc=re.findall(r'<div class="prodDescription">(.*?)</div>', data)
productName=re.findall(r'<div class="familyTitle">(.*?)</div>', data)
manufact=re.findall(r'<a href=".*?">(.*?)</a>', data)

for d in divs:
	if "<br/>" in d:
		names.append(d.replace('<br/>', ' '))
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

# for x in manufact:
	# print(x)
		
for i in range(0,len(names)):
	#upc -> ean/upc, name, sku, list price
	sometimesIbreakThings[upcs[i][0]]=[upcs[i][1],names[i],skus[i], prices[i]]

#print(sometimesIbreakThings)
for k in sometimesIbreakThings.keys():
	print(k+" -> "+str(sometimesIbreakThings[k])+"\n")
