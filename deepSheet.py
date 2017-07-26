import urllib.request as ur
import re
names=[]
skus=[]
upcs=[]
prices=[]

sometimesIbreakThings={}
url="https://www.macphersonart.com/product/137187/Artists-Watercolor.html"
#url='https://www.macphersonart.com/product/149250/Neon-Leather-Paint.html'

response=ur.urlopen(url)
data=response.read().decode("utf-8", errors="ignore")

divs=re.findall(r'<div>(.*?)</div>', data)
upc=re.findall(r'<div class="(.*?)</div>', data)

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
		#print(u[-4:])
		#this is wrong - fix
		prices.append(u[-4:])
	else:
		pass
for i in range(0,len(names)):
	#upc -> ean/upc, name, sku, list price
	sometimesIbreakThings[upcs[i][0]]=[upcs[i][1],names[i],skus[i], prices[i]]

print(sometimesIbreakThings)
	
