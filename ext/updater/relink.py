import os, shutil

pluginDir = xlPlugins.replace('plugins/', 'plugins')
newPlugins = newPlugins
oldPlugins = xlHome + "plugins"
xlHome = xlHome

print "Dir: ", dir
print "New Plugins: ", newPlugins
print "Old Plugins: ",  oldPlugins
print "Live plugins: ", pluginDir
print "XLHome: ", xlHome

if os.path.islink(oldPlugins):
    print "The plugins folder is already a link.  Your update is complete!"
    shutil.rmtree(newPlugins) #remove new plugins directory

elif (newPlugins == xlHome):

    shutil.rmtree(newPlugins) #remove new plugins directory
    os.symlink(pluginDir, oldPlugins)
    print "Symlinking " + xlHome + " to " + oldPlugins +" !\n"
    print "Your update is complete!"

elif(newPlugins != xlHome) and os.path.islink(oldPlugins) is False:
    #os.system("ln -s " + oldPlugins + pluginDir)  #symlink
    print "os.symlink("+pluginDir+", "+oldPlugins+")"
    shutil.rmtree(newPlugins) #remove new plugins directory
    shutil.rmtree(oldPlugins) #remove server plugins directory
    os.symlink(pluginDir, oldPlugins) #symlink plugins directory
    print "Symlinking " + xlHome + "plugins to " + oldPlugins +" !\n"
    print "Your update is complete!"
else:
    shutil.rmtree(newPlugins) #remove new plugins directory
    print "The new plugins folder has been deleted. Your update is complete!"