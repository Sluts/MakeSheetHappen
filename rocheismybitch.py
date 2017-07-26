import urllib.request as ur
import re
url='https://lamaisondupastel.com/shop/?cat=4'
response=ur.urlopen(url)
data=response.read().decode("utf-8", errors="ignore")
siteRoot=re.findall(r'(.*?[c][o][m])[/]', url)
divs=re.findall(r'<img src="(.*?)" />', data)
for d in divs:
	ur.urlretrieve(siteRoot[0]+d, "c:/users/james/pictures/henriroche/"+d[13:])
