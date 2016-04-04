import os.path, time, shutil, os, fileinput, string, pprint, filecmp, glob


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

#location of the XLD Server
xld_install = xlHome

# location to save move repository, ext, plugins and conf directores
save_path = xlRepository

Product = xlProduct

#print "You are updating ", Product

if (Product == 'XL Deploy'):
    # list the persistent directories from XLD that need to be copied
    directories = ['ext', 'conf', 'repository', 'work', 'bin']
    properties_file = save_path + "/conf/deployit.conf"

else:
    # list the persistent directories from XLR that need to be copied
    directories = ['ext', 'conf', 'repository', 'archive', 'work', 'bin']
    #check the reference to the repository file and make sure it's correct
    properties_file = save_path + "/conf/xl-release-server.conf"


#create folders to organize reposititory if they don't exist
if os.path.exists(save_path):
    print 'Your shared repository at ' + save_path + ' already exists I am updating your ' + Product + ' server!\n'
    for dir in directories:
        new_folder = str(save_path + "/" + dir)
        old_loc = str(xlHome + "/" + dir) #XLD/XLR server directory from the plugin

        print "Updating the " + old_loc + " directory!\n"
        #print "os.path.islink("+old_loc+") is: ", os.path.islink(old_loc)
        #ignore the repository and work folders they only need to be checked and moved on the first install
        if os.path.islink(old_loc):
            print "There is no upgrade available for " + dir + "!\n"
        else:
            #remove the folders from the new install
            shutil.rmtree(old_loc)
            print "Removing ", old_loc

            #symlink the shared folders to the new locations
            os.system("ln -s " + new_folder + " " + old_loc)
            #print "ln -s " + new_folder + " ", old_loc
            print "\nSymlinking ", new_folder + " to " + old_loc

else:
    #print save_path, "Creating shared repository path for: ", new_folder
    os.makedirs(save_path)
    print "\nCreating directory: ", save_path

    #compile location for new repository
    for dir in directories:

        new_folder = str(save_path) + "/" + str(dir)
        #print "NEW FOLDER: ", new_folder
        old_loc = xlhome + "/" + dir #XLD/XLR Core Directory can be hardcoded here

        #print old_loc
        #print "Directory: ", dir
        #print "New Folder: ", new_folder


        #copy repository from install of XLD/XLR to specified save_path
        try:
            print "\nCopying " + old_loc + " to " +  new_folder
            shutil.copytree(old_loc, new_folder)
        # Directories are the same
        except shutil.Error as e:
            print('Directory not copied. Error: %s' % e)
        # Any error saying that the directory doesn't exist
        except OSError as e:
            print('Directory not copied. Error: %s' % e)

        #remove the folders from the new install
        shutil.rmtree(old_loc)
        print "\nRemoving ", old_loc

        #symlink the shared folders
        os.system("ln -s " + new_folder + " " + old_loc)
        #print "ln -s " + new_folder + " ", old_loc
        print "\nSymlinking ", new_folder + " to " + old_loc

#check the reference to the repository file and make sure it's correct
#print "\n\n" + properties_file + "\n\n"
repository_loc = "jcr.repository.path=file:/" + save_path + "/repository"
oldProp ='jcr.repository.path=repository'

s = open(properties_file).read()
if repository_loc in s:
    print "Checking the repository!\n"
    print "The repository link " + repository_loc + " is already set in " + properties_file + "!"
else:
    print 'Updating the repository location in your ' + properties_file + " file from " + oldProp + " to " + repository_loc + "!"
    s = s.replace(oldProp, repository_loc)
    f = open(properties_file, 'w')
    f.write(s)
    f.close()

