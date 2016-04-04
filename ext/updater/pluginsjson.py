import os
import com.xhaus.jyson.JysonCodec as json
from com.xebialabs.deployit.plugin.api.reflect import Type

dir = xlPlugins  #from task in XLR
oldFiles = os.listdir(dir)
jsonFile = dir+"plugins.json"
__release = getCurrentRelease()

#print jsonFile

#check if json file exists already,if it does, remove it

if os.path.isfile(jsonFile) is True:
    print "File exists ... updating with current plugin data!"
    os.remove(jsonFile)

response = []

#create an entry for each plugin found

for oldInstalledPlugins in oldFiles:
    #print oldInstalledPlugins
    oldPlugin = oldInstalledPlugins.replace(dir, ' ').rsplit('.', 5)[0].rsplit('-', 1)[0]
    oldFtype = oldInstalledPlugins.replace(dir, ' ').rsplit('.', 1)[-1]
    oldVersion = oldInstalledPlugins.replace(dir, ' ').rsplit('-', 1)[-1].replace('.' + oldFtype, "")
    print "Old: ", oldPlugin
    print "Old Plugin: " + oldPlugin + " version is: ", oldVersion + "\n"
    if (oldPlugin != ''):
        response.append({'plugin': oldPlugin, 'currentVersion' : oldVersion, 'newVersion': 'null', 'fileName': oldInstalledPlugins, 'pluginType': 'Enter Manually', 'gitRepo': 'Enter Manually', 'url': 'Enter Manually'})
        __steps = {"mgmt.updateplugins" : [{'plugin': oldPlugin, 'currentVersion' : oldVersion, 'newVersion': 'null', 'fileName': oldInstalledPlugins, 'pluginType': 'Enter Manually', 'gitRepo': 'Enter Manually', 'url': 'Enter Manually'}]}

    #print json.dumps(response)
        print __steps

#create the file
outputFile = open(jsonFile, "w+")
json_data = json.dumps(response, outputFile, indent=4)
#fileData = json.dump(response, outputFile, indent=4)
outputFile.write(json_data)
outputFile.close()

print json_data
print "OUTFILE: ", outputFile
#file.write(fileData)

print __release


def createSimpleTask(phaseId, taskTypeValue, title, propertyMap):
    """
    adds a custom task to a phase in the release
    :param phaseId: id of the phase
    :param taskTypeValue: type of task to add
    :param title: title of the task
    :param propertyMap: properties to add to the task
    :return:
    """
    parenttaskType = Type.valueOf("xlrelease.CustomScriptTask")

    parentTask = parenttaskType.descriptor.newInstance("nonamerequired")
    parentTask.setTitle(title)

    childTaskType = Type.valueOf(taskTypeValue)
    childTask = childTaskType.descriptor.newInstance("nonamerequired")
    for item in propertyMap:
        if childTask.hasProperty(item):
            childTask.setProperty(item,propertyMap[item])
        else:
            print "dropped property: %s on %s because: not applicable" % (item, taskTypeValue)
    parentTask.setPythonScript(childTask)

    taskApi.addTask(str(phaseId),parentTask)



def get_target_phase(targetPhase):
    """
    search the release for the targetPhase by string name
    for some stupid reason we can't address it by its name ..
    :param targetPhase:string
    :return:phaseId
    """
    phaseList = phaseApi.searchPhasesByTitle(targetPhase,release.id)
    if len(phaseList) == 1:
        return phaseList[0]
    else:
        return False
        #should be replaced by some logic to create the phase



def load_profile(profile):
    """
    returns a dict .. if input is json it will return ad dict .. if dict it will return the dict
    :param profile:
    :return:
    """

    if type(profile) is dict:
        return profile
    else:
       return json.loads(profile)

def download_json_profile(url):
    print "downloading json from %s" % url
    error = 300
    output = requests.get(url)

    if ( output.status_code < error ) :
        print "Download from %s : succesfull" % url
        print str(output.text)
        return str(output.text)
    else:
        print 'unable to download json'
        return False


def handle_profile(profile, targetPhase):
    """
    parse the loaded profile and add a task for each item in it
    :param profile: json or dict
    :param targetPhase: phase to add the steps to
    :return:
    """

    loaded_profile = load_profile(profile)
    phaseId = get_target_phase(targetPhase)
    title_nr = 0

    for type, data in loaded_profile.items():

        if __type_step_dict.has_key(type):
            taskTypeValue = __type_step_dict[type]
        else:
            taskTypeValue = type

        for data_item in data:
            final_data_items = dict(data_item.items() + __default_data_items.items())
            title_nr += 1

            createSimpleTask(phaseId, taskTypeValue, "dar_build_task_%s_%i" % (type, title_nr), final_data_items )

# both inputJson and inputJsonUrl cannot be None .
# we need input
if inputJson == None and inputJsonUrl == None:
    print "both inputJson and inputJsonUrl are empty: this can not be . existing step"
    sys.exit(2)

# inputJsonUrl takes precedence over inputJson ..
# BECAUSE I SAY SO ....Biatch
# Just checking if anyone ever really reads this ;-)
if inputJsonUrl.startswith('http'):
    inputJson = download_json_profile(inputJsonUrl)

handle_profile(__pre_build_steps, phaseName)
handle_profile(inputJson, phaseName)
handle_profile(__post_build_steps, phaseName)
handle_profile(__cleanup_build_steps, phaseName)
