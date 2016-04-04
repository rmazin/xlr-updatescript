import os, os.path, time, shutil, fileinput, string, pprint, filecmp, glob, fnmatch, sys
import com.xhaus.jyson.JysonCodec as json
from com.xebialabs.xlrelease.domain import Task
from com.xebialabs.deployit.plugin.api.reflect import Type
from java.text import SimpleDateFormat

dir = xlPlugins + "/plugins" #from task in XLR
dir2 = newPlugins + "/plugins" #from task in XLR

#print "New Plugins: ", dir
#print "Old Plugins: ", dir2

nextPhase = "Update Plugins"

release = getCurrentRelease()
releaseId = release.id
#print "Current Release: ", releaseId
#print "Phase ID: ", phase.id

newPhase = phaseApi.searchPhasesByTitle(nextPhase, str(release.id))
targetPhase = str(newPhase[0])


if os.path.islink(dir):
    print "There are no updates available for your plugins!"
else:

    new = []
    old = []

    newFiles = os.listdir(dir)
    oldFiles = os.listdir(dir2)

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

    #print "NEW: ", new

    compare = set(old) & set(new)

    for comp in compare:
        #print "Matched: ", comp
        pattern = comp + "*"
        print "Looking for: ", pattern

        for oldName in oldFiles:
            #print comp
            #print 'Filename: %-25s %s' % (name, fnmatch.fnmatch(name, pattern))
            if fnmatch.fnmatch(oldName, pattern) is True:
                print "Found a match with the " + comp + " plugin. Removing " + oldName + " from " + dir2 + "\n"
                #time.sleep(1) #add a pause if needed
                os.remove(dir2 + "/" + oldName) #remove old plugin if a match was found
                #print "os.remove(" + dir2 + "/" + oldName +")"
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


task = taskApi.newTask("mgmt.RelinkPlugins")
task.title = "Relink Plugins Folder"
taskApi.addTask(targetPhase, task)
