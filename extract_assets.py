import json
import requests
import os
from os import path
import mimetypes

SAVES_PATH = 'saves'
MECHS_PATH = 'Mechs'

def makePath(aPath):
    try:
        if not path.exists(aPath):
            os.makedirs(aPath)
    except OSError as e:
        if not path.isdir(aPath):
            raise
        if e.errno != errno.EEXIST:
            raise

def loadJSONFile(pathToJSON):
    if path.exists(pathToJSON):
        f = open(pathToJSON)
        json_data = json.load(f)
        f.close()
        return json_data

def getSaveName(savefile):
    json_str = loadJSONFile(savefile)
    for (k,v) in json_str.items():
        if k == "SaveName" and v != "":
            return v

files = os.listdir(SAVES_PATH)
global savefilename
for file in files:
    if file[0] != ".":
        savefilename = getSaveName(path.join(SAVES_PATH,file))
        print(savefilename)

def getImageFromURL(url,filename):
    img = requests.get(url, allow_redirects=True)
    makePath(path.join(MECHS_PATH, savefilename))
    
    content_type = img.headers['content-type']
    extension = mimetypes.guess_extension(content_type)
    
    output = filename + extension
    open(output, 'wb').write(img.content)

def downloadFileFromURL(url, dst):
    f = requests.get(url, allow_redirects=True, verify=False)
    content_type = f.headers['content-type']
    extension = mimetypes.guess_extension(content_type)
    print(extension)
    print(f.status_code)
    if (f.status_code == 200 and extension == None):
        extension = '.txt'
    output = path.join(dst, 'Mesh_' + extension)
    #print(output)
    open(output, 'wb').write(f.content)

def downloadCustomBoard(dst):
    image_url = mech_obj['CustomImage']['ImageURL']
    print(f'downloading {name} from {image_url}')
    getImageFromURL(image_url, path.join(dst, nickname))
    print('done.')

def downloadCustomModel(dst):
    mesh = mech_obj['CustomMesh']
    mesh_url = mesh['MeshURL']
    diffuse_url = mesh['DiffuseURL']
    normal_url = mesh['NormalURL']
    collider_url = mesh['ColliderURL']
    
    print(f'downloading mesh for {nickname} from {mesh_url} to {dst}')
    print(dst)
    downloadFileFromURL(mesh_url, path.join(dst))
#     getImageFromURL(image_url, path.join(dst, name))
    print('done.')

#json.dumps(json_data)
#print(json.dumps(json_data, indent = 2, sort_keys=True))

filename = '362005894'
filepath = path.join(SAVES_PATH, filename + '.json')
print(filepath)
savefilename = getSaveName(filepath)
json_data = json.load(open(filepath))
f = open(filepath)
json_str = json.load(f)
f.close()
assetfolder = ''

for (k, v) in json_str.items():
    if k == 'ObjectStates':
        randomInts = []
        randomInt = 0
        obj_states = v
        for (mech_obj) in obj_states:
            name = mech_obj['Name']
            nickname = mech_obj['Nickname']
            if nickname == '':
                randomInt = random.randint(0,65536)
                randomStr = str(randomInt)
                nickname = name + '_no.' + randomStr

            downloadName = name + '_' + nickname
            
            assetfolder = os.path.join(MECHS_PATH, savefilename, nickname, name)
            makePath(assetfolder)
            #print(assetfolder)
            
            #if name == 'Custom_Board':
                #downloadCustomBoard(assetfolder)
            if name == 'Custom_Model':
                downloadCustomModel(assetfolder)
            
print('image downloading done.')