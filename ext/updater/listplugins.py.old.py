import os, json
from com.xebialabs.deployit.plugin.api.reflect import Type

dir = xlPlugins  #from task in XLR
oldFiles = os.listdir(dir)
dir2 = newPlugins
newFiles = os.listdir(dir2)

jsonDir= '/pluginlog/'

fullPath = dir+jsonDir

if not os.path.exists(fullPath):
    os.makedirs(fullPath)

jsonFile = dir+jsonDir+"plugins.json"
inputJson = jsonFile
phaseName = 'Input Plugin Information'
phase = getCurrentPhase()
nextPhase = "Update Plugins"

release = getCurrentRelease()
releaseId = release.id
#print "Current Release: ", releaseId
#print "Phase ID: ", phase.id

newPhase = phaseApi.searchPhasesByTitle(nextPhase, str(release.id))
targetPhase = str(newPhase[0])

#print "New Phase: ", targetPhase

#print jsonFile

print "\nCurrent Phase: ", getCurrentPhase()
print "\n"

response = []
new = []
old = []

'''
#if plugins.json already exists but is empty remove it
if os.path.isfile(jsonFile) is True and os.stat(jsonFile).st_size == 0: #if plugins.json exists and is empty, remove it
    print "File exists but is empty ... Removing " + jsonFile + "!"
    os.remove(jsonFile)
    # NOT FINISHED: Add some logic to produce the new json file
'''

if os.path.isfile(jsonFile) is True and os.stat(jsonFile).st_size != 0: # if plugins.json exists and is not empty read the file
    print "File exists ... reading plugin data and creating update tasks!\n"

    task = taskApi.newTask("mgmt.JsonCleanup")
    task.title = "Backup Previous Plugin Data"
    taskApi.addTask(targetPhase, task)

    task = taskApi.newTask("xlrelease.Task")
    task.title = "Enter new plugin versions in tasks below"
    taskApi.addTask(targetPhase, task)

    with open(jsonFile) as json_data:
        d = json.load(json_data)
        json_data.close()
        #pprint(d)

        for key in d:
            #print key['fileName']
            plugin = key['plugin']
            curVers = key['currentVersion']
            fName = key['fileName']
            updateType = key['updateType']
            gitRepo = key['gitRepo']
            pluginLocation = key['pluginLocation']
            pluginName = fName
            pluginFile = fName
            newVersion = 'null'

            print "Name: ", fName
            print "\n"
            print "File: ", pluginFile
            print "\n"


        for oldInstalledPlugins in oldFiles:
            #print oldInstalledPlugins
            oldPlugin = oldInstalledPlugins.replace(dir, ' ').rsplit('.', 5)[0].rsplit('-', 1)[0]
            oldFtype = oldInstalledPlugins.replace(dir, ' ').rsplit('.', 1)[-1]
            oldVersion = oldInstalledPlugins.replace(dir, ' ').rsplit('-', 1)[-1].replace('.' + oldFtype, "")

            if (oldPlugin != '') and (oldPlugin != 'readme') and (oldPlugin != 'lm') and (oldPlugin !=''): # ignore any files that are not actually plugins
                old.append(oldPlugin.replace(" /", ''))

                with open(jsonFile) as feedsjson:
                    feeds = json.load(feedsjson)
                    feedsjson.close()

                with open(jsonFile, "w+") as f:
                    json.dump([], f, indent=4)
                    f.close()

                with open(jsonFile, "w+") as feedsjson:
                    entry = {'plugin': pluginName.replace(curVers, newVersion), 'currentVersion' : newVersion,'lastVersion': curVers, 'updateType': updateType, 'fileName': pluginFile.replace(curVers, newVersion), 'gitRepo': gitRepo, 'pluginLocation': pluginLocation}
                    feeds.append(entry)
                    json.dump(feeds, feedsjson, indent=4)
                    feedsjson.close()

            task = taskApi.newTask("mgmt.UpdatePlugins")
            task.title = "Update "+plugin
            task.pythonScript.pluginName = plugin #Plugin name variable
            task.pythonScript.pluginFile = fName #Plugin full file name variable
            task.pythonScript.currentVersion = curVers #currently installed version variable
            task.pythonScript.updateType = updateType #type of update for plugin (local, git, etc.)
            task.pythonScript.gitRepo = gitRepo #the name of the git repo if the plugin release is stored in Git
            task.pythonScript.pluginLocation = pluginLocation #location of the new plugin file either a URL or local or shared path
            taskApi.addTask(targetPhase, task)



#add a check for any plugins not found in the XML and add them to the phase and append to json

else: #scan the specified plugins folder for all existing plugins and create new tasks to update

    for oldInstalledPlugins in oldFiles:
        #print oldInstalledPlugins
        oldPlugin = oldInstalledPlugins.replace(dir, ' ').rsplit('.', 5)[0].rsplit('-', 1)[0]
        oldFtype = oldInstalledPlugins.replace(dir, ' ').rsplit('.', 1)[-1]
        oldVersion = oldInstalledPlugins.replace(dir, ' ').rsplit('-', 1)[-1].replace('.' + oldFtype, "")

        if (oldPlugin != '') and (oldPlugin != 'readme') and (oldPlugin != 'lm'): # ignore any files that are not actually plugins
            response.append({'plugin': oldPlugin, 'currentVersion' : oldVersion, 'newVersion': 'null','lastVersion': 'NA', 'updateType': 'Enter Manually', 'fileName': oldInstalledPlugins, 'gitRepo': 'Enter Manually', 'pluginLocation': 'Enter Manually'})
            #print "Old: ", oldPlugin
            print "Old " + oldPlugin + " version is "+ oldVersion + " is currently installed!\n"
            #create the task
            task = taskApi.newTask("mgmt.UpdatePlugins")
            task.title = "Update "+oldPlugin
            task.pythonScript.pluginName = oldPlugin #Plugin name variable
            task.pythonScript.pluginFile = oldInstalledPlugins #Plugin full file name variable
            task.pythonScript.currentVersion = oldVersion #currently installed version variable
            taskApi.addTask(targetPhase, task)

    #create json file
    outputFile = open(jsonFile, "w+")
    json_data = json.dumps(response, outputFile, indent=4)
    outputFile.write(json_data)
    outputFile.close()

#get and compile a list of the old plugins without the version number and extension
for oldInstalledPlugins in oldFiles:
    #print oldInstalledPlugins
    oldPlugin = oldInstalledPlugins.replace(dir2, ' ').rsplit('.', 5)[0].rsplit('-', 1)[0]
    #print "Old: ", oldPlugin
    old.append(oldPlugin.replace(" /", ''))

#get and compile a list of the new plugins without the version number and extension
for newInstalledPlugins in newFiles:
    #print newInstalledPlugins
    newPlugin = newInstalledPlugins.replace(dir, ' ').rsplit('.', 5)[0].rsplit('-', 1)[0]
    #print "New: ", newPlugin
    new.append(newPlugin.replace(" /", ''))

compare = set(old) & set(new)

for comp in compare:
    #print "Matched: ", comp
    pattern = comp + "*"
    print "Looking for: ", pattern

    for oldName in oldFiles:
        #print comp
        #print 'Filename: %-25s %s' % (name, fnmatch.fnmatch(name, pattern))
        print "Old Name: ", oldName

        print "MATCH: ",  fnmatch.fnmatch(oldName, pattern)
        print "/n"

        if fnmatch.fnmatch(oldName, pattern) is True:
            print "Found a match with the " + comp + " plugin. Removing " + oldName + " from " + dir2 + "\n"
            #time.sleep(1) #add a pause if needed
            os.remove(dir2 + "/" + oldName) #remove old plugin if a match was found
            #print "os.remove(" + dir2 + "/" + oldName +")"
        else:
            print "Did not find a match, moving on!"
    for newName in newFiles:
        if fnmatch.fnmatch(newName, pattern) is True:
            #print "MATCH: ",  fnmatch.fnmatch(oldName, pattern)
            print "Copying a new version of the " + newName + " plugin to " + dir2 + "/" + newName + "\n"
            #print "New Name: " + newName + " and Old Name: " + oldName
            shutil.copyfile(dir + "/" + newName, dir2 + "/" + newName.replace('plugins', ' ')) #copy new version of plugins
            #print "shutil.copyfile("+ dir1 + "/" + newName + "," + dir2 + "/" + newName.replace('plugins', '') + ")"


        #print "Comparison: ", compare

    #find the difference between the new plugins and old plugins
    different = set(new) - set(old)

    if len(different) == 0:
        different = set(old) - set(new)
        print "No new plugins to add!"

    for diff in different:
        diffPlugin = glob.glob(dir + "/" + diff + '*')
        print "New plugin found: ", diff
        #print "Full: ", diffPlugin
        for name in diffPlugin:
            #print "\n"
            #print "shutil.copyfile("+ name.replace(dir2, dir) + "," + name.replace(dir, dir2) + ")"
            #print "\n"
            shutil.copyfile(name.replace(dir2, dir), name.replace(dir, dir2)) #copy new plugins
            print "Copying the new plugin " + name

            response.append({'plugin': diffPlugin, 'currentVersion' : oldVersion, 'newVersion': 'null','lastVersion': 'NA', 'updateType': 'Enter Manually', 'fileName': newName, 'gitRepo': 'Enter Manually', 'pluginLocation': 'Enter Manually'})
            #print "Old: ", oldPlugin
            print "Plugin " + diffPlugin + " version is "+ oldVersion + " is currently installed!\n"
            #create the task
            task = taskApi.newTask("mgmt.UpdatePlugins")
            task.title = "Update " + diffPlugin
            task.pythonScript.pluginName = diffPlugin #Plugin name variable
            task.pythonScript.pluginFile = diffPlugin #Plugin full file name variable
            task.pythonScript.currentVersion = oldVersion #currently installed version variable
            taskApi.addTask(targetPhase, task)

task = taskApi.newTask("mgmt.RelinkPlugins")
task.title = "Relink Plugins Folder"
taskApi.addTask(targetPhase, task)

