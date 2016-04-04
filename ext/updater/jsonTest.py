import json, urllib2, os, shutil, pprint, urllib

'''
curl -i -H "Authorization: token 39eaf724ebfe58b60241c35b71df0f310a086d8c"     -H "Accept: application/vnd.github.manifold-preview"     "https://api.github.com/repos/WianVos/xlr-lm-artifactory-plugin/releases/latest"

'''

pluginName = 'xlr-lm-artifactory-plugin'
savePath = '/tmp/'

url = "https://api.github.com/repos/WianVos/"+ pluginName +"/releases/latest"
response = urllib2.urlopen(url)
data = response.read()
values = json.loads(data)

#print "VALUES: ", values

print "Version: ", values['tag_name']
#print "Assets: ", values['assets']
print "\n"
#print values['assets'][0]
#print "\n"

#pprint(data)

keylist = values.keys()
keylist.sort()

#print "Keylist: ", keylist
#print keylist.sort()
newUrl = values['assets'][0]['browser_download_url']

print "Latest release download: ", newUrl

pluginFile = pluginName + ".jar"
print "FILENAME: ", pluginFile

print "urllib.urlretrieve("+newUrl+","+savePath + pluginFile+")"

urllib.urlretrieve(newUrl, savePath + pluginFile)