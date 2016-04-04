import os, json, datetime, shutil

pluginDir = xlPlugins

now = str(datetime.datetime.now())

jsonDir = 'pluginlog/'

jsonFile = pluginDir+jsonDir+"plugins.json"
jsonFile2 = pluginDir+jsonDir+"2plugins.json"
jsonFile3 = pluginDir+jsonDir+"plugins"+now+".json"

shutil.copyfile(jsonFile, jsonFile2)
shutil.copyfile(jsonFile2, jsonFile3)
os.remove(jsonFile)