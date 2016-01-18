import os, os.path, time, shutil, os, fileinput, string, pprint, filecmp, glob, fnmatch

'''

To use this script:
- drop it in the root of the XL Deploy server files
- run it as a python script

This script moves the repository, plugins, conf, work and bin directories to a centralized location
and adds symlinks to the server on the initial run and links the new repository location in /conf/depoyit.conf.
For subsequent updates it moves the updated files and re links the necessary centralized directories.


'''

#stop XLD or XLR Service
#os.system("service stop xldeploy")
#pause for service to stop
#time.sleep(25)

#print "The XL Deploy service is shutting down for an upgrade!"
# list the persistent directories from XLD that need to be copied
directories = ['ext', 'conf', 'plugins', 'repository', 'archive', 'work', 'bin']

#location of the XLD Server
#print os.path.dirname(os.path.realpath(__file__))
xld_install = os.path.dirname(os.path.realpath(__file__))

# location to save move repository, ext, plugins and conf directores

save_path = "/" + raw_input("Please input the new shared path for your XL Deploy repository: ") #this can be changed to a hardcoded location
#create folders to organize reposititory if they don't exist
if os.path.exists(save_path):
    print 'Your shared repository at ' + save_path + ' already exists I am updating your XL Deploy server!'
    for dir in directories:
        if (dir == 'plugins'):

            if os.path.islink(dir):
                print "There is no upgrade available for " + dir + "!"
            else:

                dir2 = save_path + "/" + dir

                old = []
                new = []

                oldFiles = os.listdir(dir2)
                newFiles = os.listdir(dir)

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

                    #oldFiles = os.listdir(dir2)
                    #newFiles = os.listdir(dir1)

                    for oldName in oldFiles:
                        #print comp
                        #print 'Filename: %-25s %s' % (name, fnmatch.fnmatch(name, pattern))
                        if fnmatch.fnmatch(oldName, pattern) is True:
                            print "Found a match with the " + comp + " plugin. Removing " + oldName + " from " + dir2
                            #time.sleep(1) #add a pause if needed
                            os.remove(dir2 + "/" + oldName) #remove old plugin if a match was found
                            #print "os.remove(" + dir2 + "/" + oldName +")"
                    for newName in newFiles:
                        if fnmatch.fnmatch(newName, pattern) is True:
                            #print "MATCH: ",  fnmatch.fnmatch(oldName, pattern)
                            print "Copying a new version of the " + newName + " plugin to " + dir2 + "/" + newName
                            #print "New Name: " + newName + " and Old Name: " + oldName
                            shutil.copyfile(dir + "/" + newName, dir2 + "/" + newName.replace('plugins', ' ')) #copy new version of plugins
                            #print "shutil.copyfile("+ dir1 + "/" + newName + "," + dir2 + "/" + newName.replace('plugins', '') + ")"

                    #print "Comparison: ", compare

                    #find the difference between the new plugins and old plugins
                    different = set(new) - set(old)

                    if len(different) == 0:
                        different = set(old) - set(new)
                        print "Old plugins have more!!"

                    for diff in different:
                        print "New: ", diff
                      #  shutil.copyfile(dir + "/" + diff, dir2 + "/" + diff #copy new plugins
                      #  shutil.rmtree(dir) #remove new plugins directory
                    #  os.system("ln -s " + new_folder + " " + dir) #symlink plugins directory to centralized location

        else:
            print "Updating the " + dir + " directory!"
            #ignore the repository and work folders they only need to be checked and moved on the first install
            if os.path.islink(dir):
                print "There is no upgrade available for " + dir + "!"
            else:
                new_folder = str(save_path) + "/" + str(dir)
                old_loc = os.path.dirname(os.path.realpath(__file__)) + "/" + dir #XLD/XLR Core Directory can be hardcoded here
                #remove the folders from the new install
                shutil.rmtree(dir)
                print "Removing ", old_loc

                #symlink the shared folders to the new locations
                os.system("ln -s " + new_folder + " " + old_loc)
                #print "ln -s " + new_folder + " ", old_loc
                print "Symlinking ", new_folder + " to " + old_loc

else:
    #print save_path, "Creating shared repository path for: ", new_folder
    os.makedirs(save_path)
    print "Creating directory: ", save_path

    #compile location for new repository
    for dir in directories:

        new_folder = str(save_path) + "/" + str(dir)
        old_loc = os.path.dirname(os.path.realpath(__file__)) + "/" + dir #XLD/XLR Core Directory can be hardcoded here

        print old_loc
        print "New Folder: ", new_folder
        print "Directory: ", dir

        #copy repository from install of XLD/XLR to specified save_path
        try:
            shutil.copytree(dir, new_folder)
        # Directories are the same
        except shutil.Error as e:
            print('Directory not copied. Error: %s' % e)
        # Any error saying that the directory doesn't exist
        except OSError as e:
            print('Directory not copied. Error: %s' % e)

        #remove the folders from the new install
        shutil.rmtree(old_loc)
        print "Removing ", old_loc

        #symlink the shared folders
        os.system("ln -s " + new_folder + " " + old_loc)
        #print "ln -s " + new_folder + " ", old_loc
        print "Symlinking ", new_folder + " to " + old_loc

#check the reference to the repository file and make sure it's correct
properties_file = save_path + "/conf/xl-release-server.conf"
repository_loc = "jcr.repository.path=file:/" + save_path + "/repository"
oldProp ='jcr.repository.path=repository'

s = open(properties_file).read()
if repository_loc in s:
    print "Checking the repository!"
    print "The repository link " + repository_loc + " is already set in " + properties_file + "!"
else:
    print 'Updating the repository location in your ' + properties_file + " file from " + oldProp + " to " + repository_loc + "!"
    s = s.replace(oldProp, repository_loc)
    f = open(properties_file, 'w')
    f.write(s)
    f.close()