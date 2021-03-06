import os, json, os.path, time, shutil, fileinput, string, pprint, filecmp, glob, fnmatch, sys
from com.xebialabs.deployit.plugin.api.reflect import Type

dir = xlPlugins  #from task in XLR Old plugins
oldFiles = os.listdir(dir)
dir2 = newPlugins #from task in XLR New Plugins
newFiles = os.listdir(dir2)

jsonDir= 'pluginlog/'

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

if os.path.isfile(jsonFile) is True and os.stat(jsonFile).st_size != 0: # if plugins.json exists and is not empty read the file
    print "File exists ... reading plugin data and creating update tasks!\n"

    task = taskApi.newTask("xlrelease.Task")
    task.title = "1-Enter new plugin versions in tasks below"
    taskApi.addTask(targetPhase, task)

    task = taskApi.newTask("mgmt.JsonCleanup")
    task.title = "Backup Previous Plugin Data"
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
            newVersion = key['newVersion']

            #print "FILE: ", fName
            #print "\n"


            task = taskApi.newTask("mgmt.UpdatePlugins")
            task.title = "Update " + plugin
            task.pythonScript.pluginName = plugin #Plugin name variable
            task.pythonScript.pluginFile = fName #Plugin full file name variable
            task.pythonScript.currentVersion = curVers #currently installed version variable
            task.pythonScript.updateType = updateType #type of update for plugin (local, git, etc.)
            task.pythonScript.gitRepo = gitRepo #the name of the git repo if the plugin release is stored in Git
            task.pythonScript.pluginLocation = pluginLocation #location of the new plugin file either a URL or local or shared path
            taskApi.addTask(targetPhase, task)


    #add a check for any plugins not found in the XML and add them to the phase and append to json

        #get and compile a list of the old plugins without the version number and extension
        for oldInstalledPlugins in oldFiles:
            #print "OLD: ", oldInstalledPlugins
            oldPlugin = oldInstalledPlugins.replace(dir, ' ').rsplit('.', 5)[0].rsplit('-', 1)[0]
            #print "Old: ", oldPlugin
            old.append(oldPlugin.replace(" /", ''))

        #get and compile a list of the new plugins without the version number and extension
        for newInstalledPlugins in newFiles:
            #print newInstalledPlugins
            newPlugin = newInstalledPlugins.replace(dir2, ' ').rsplit('.', 5)[0].rsplit('-', 1)[0]
            #print "New: ", newPlugin
            new.append(newPlugin.replace(" /", ''))


        #find the difference between the new plugins and old plugins
        different = set(old) - set(new)
        print "DIFFERENT: ", different
        print "LEN: ", len(different)

        '''
        if len(different) == 0:
            different = set(new) - set(old)
            print "No new plugins to add!"
            print "New Different: ", different
            print "New LEN: ", len(different)
        '''

        print "OF Dir: ", dir
        print oldFiles
        print "\n"
        print newFiles

        for diff in different:
            if (diff != '') and (diff != 'readme') and (diff != 'pluginlog') and (diff != '.DS_Store'): # ignore any files that are not actually plugins
                print "New plugin found: ", diff
                pattern = diff + "*"
                print "Looking for: ", pattern

                for newPlug in oldFiles:
                    match = fnmatch.fnmatch(newPlug, pattern)
                    if match is True:
                        print newPlug
                        #print "True"

                        if fnmatch.fnmatch(diff, pattern) is True:
                            #print "Match"

                            print "Found a match with the " + diff + " plugin in " + dir2 + " with a filename of " + newPlug +"\n"
                            #print "N: ", pFile
                            oldFtype = newPlug.replace(dir, ' ').rsplit('.', 1)[-1]
                            #print oldFtype
                            #curVers = newPlug..replace(dir, ' ').rsplit('-', 1)[-1].replace('.' + oldFtype, "")
                            curVers = newPlug.replace(dir, ' ').rsplit('-', 1)[-1].replace('.' + oldFtype, "")
                            #curVers = 'null'
                            updateType = 'Enter Manually'
                            gitRepo = 'Enter Manually'
                            pluginLocation = 'Enter Manually'

                            with open(jsonFile) as feedsjson:
                                feeds = json.load(feedsjson)
                                feedsjson.close()

                            with open(jsonFile, "w+") as feedsjson:
                                entry = {'plugin': diff, 'currentVersion' : curVers, 'newVersion': 'Enter Manually', 'lastVersion': curVers, 'updateType': updateType, 'fileName': newPlug, 'gitRepo': gitRepo, 'pluginLocation': pluginLocation}
                                feeds.append(entry)
                                json.dump(feeds, feedsjson, indent=4)
                                feedsjson.close()

                            task = taskApi.newTask("mgmt.UpdatePlugins")
                            task.title = "Update " + diff
                            task.pythonScript.pluginName = diff #Plugin name variable
                            task.pythonScript.pluginFile = newPlug #Plugin full file name variable
                            task.pythonScript.currentVersion = curVers #currently installed version variable
                            task.pythonScript.updateType = updateType #type of update for plugin (local, git, etc.)
                            task.pythonScript.gitRepo = gitRepo #the name of the git repo if the plugin release is stored in Git
                            task.pythonScript.pluginLocation = pluginLocation #location of the new plugin file either a URL or local or shared path
                            taskApi.addTask(targetPhase, task)

else: #scan the specified plugins folder for all existing plugins and create new tasks to update

    task = taskApi.newTask("xlrelease.Task")
    task.title = "Enter new plugin versions in tasks below"
    taskApi.addTask(targetPhase, task)

    for oldInstalledPlugins in oldFiles:
        #print oldInstalledPlugins
        oldPlugin = oldInstalledPlugins.replace(dir, ' ').rsplit('.', 5)[0].rsplit('-', 1)[0]
        oldFtype = oldInstalledPlugins.replace(dir, ' ').rsplit('.', 1)[-1]
        oldVersion = oldInstalledPlugins.replace(dir, ' ').rsplit('-', 1)[-1].replace('.' + oldFtype, "")


        if (oldPlugin != '') and (oldPlugin != 'readme') and (oldPlugin != 'lm') and (oldPlugin != 'pluginlog') and (oldPlugin != '.DS_Store'): # ignore any files that are not actually plugins
            response.append({'plugin': oldPlugin, 'currentVersion' : oldVersion, 'newVersion': 'Enter Manually','lastVersion': 'NA', 'updateType': 'Enter Manually', 'fileName': oldInstalledPlugins, 'gitRepo': 'Enter Manually', 'pluginLocation': 'Enter Manually'})
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

task = taskApi.newTask("mgmt.RelinkPlugins")
task.title = "Relink Plugins Folder"
taskApi.addTask(targetPhase, task)
