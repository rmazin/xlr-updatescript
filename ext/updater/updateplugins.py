import os, os.path, shutil, fileinput, sys, json, time, string, pprint, filecmp, glob, fnmatch, sys, urllib2, urllib
from com.xebialabs.xlrelease.domain import Task
from com.xebialabs.deployit.plugin.api.reflect import Type
from java.text import SimpleDateFormat
from xldeploy.XLDeployClientUtil import XLDeployClientUtil


scp_client = XLDeployClientUtil.create_scp_client(scp, username, password)


pluginDir = xlPlugins
pluginFile = pluginFile
currentVersion = currentVersion
pluginName = pluginName
newVersion = newVersion
updateType = updateType
gitRepo = gitRepo
pluginLocation = pluginLocation

savePath = '/tmp/'

jsonDir = '/pluginlog/'

jsonFile = pluginDir+jsonDir+"plugins.json"

print "Creating updated JSON Record!"

if os.path.isfile(jsonFile) is False:
    with open(jsonFile, "w+") as f:
        json.dump([], f, indent=4)
        f.close()

with open(jsonFile) as feedsjson:
    feeds = json.load(feedsjson)
    feedsjson.close()

with open(jsonFile, "w+") as f:
    json.dump([], f, indent=4)
    f.close()

with open(jsonFile, "w+") as feedsjson:
    entry = {'plugin': pluginName.replace(currentVersion, newVersion), 'currentVersion' : newVersion,'lastVersion': currentVersion, 'updateType': updateType, 'fileName': pluginFile.replace(currentVersion, newVersion), 'gitRepo': gitRepo,'newVersion': 'Enter Manually', 'pluginLocation': pluginLocation}
    feeds.append(entry)
    json.dump(feeds, feedsjson, indent=4)
    feedsjson.close()

if (updateType == 'local'):

    print "shutil.copyfile("+pluginLocation+"/"+pluginFile.replace(currentVersion, newVersion)+","+pluginDir+"/"+pluginFile.replace(currentVersion, newVersion)+")" #copy the plugin files
    shutil.copyfile(pluginLocation+pluginFile.replace(currentVersion, newVersion), pluginDir+pluginFile.replace(currentVersion, newVersion)) #copy the plugin files
    #os.remove(pluginLocation+pluginFile)
    os.remove(pluginDir+pluginFile)
    print "Updating the plugin " + pluginName + " from version " + currentVersion + " to version " + newVersion + "!"

elif (updateType == 'git'):  #check git an pull new version if available

    url = "https://api.github.com/repos/" + gitRepo + "/" + pluginName + "/releases/latest"
    response = urllib2.urlopen(url)
    data = response.read()
    values = json.loads(data)

    os.remove(pluginDir+pluginFile)

    dlLoc = values['assets'][0]['browser_download_url']
    newFile = values['assets'][0]['name']
    gitVersion = values['tag_name']

    print "GIT VERSION: ",

    if (newVersion == gitVersion):
        print "There is no update available!"
    else:

        #print "URL: " , url
        #print "\n Values: ", values
        print "Downloading " + newFile + " from " + dlLoc + " to " + pluginDir + "!"

        urllib.urlretrieve(dlLoc, pluginDir + "/" + newFile)


elif (updateType =='scp'):

    print "SCP COMING SOON!!!"

else:
    print "Transfer type is unknown! Your plugin has not been updated!"


#print "JSON: ", entry

#outputFile = open(jsonFile, "w+")

#json_data = json.dumps(response, outputFile, indent=4)
#outputFile.write(json_data)
#outputFile.close()
#os.rename(jsonFile, jsonFile[now])

