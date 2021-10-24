import os, json
from types import SimpleNamespace
import asyncio
from vulcan import Keystore
from vulcan import Account
from vulcan import Vulcan
import json
import glob
import shutil

grades=[]
new_grades=[]
now_grades=[]

old_grades = 'grades/'
new_temp_grades = 'tempgrades/'

if(not os.path.isfile("keystore.json") or not os.path.isfile("account.json")): 
    input("No keystore or account file! Run setup.py")
    quit() 

def DeleteTemp(path_to_del):
    files = glob.glob(f'{path_to_del}*.json')
    for f in files:
        os.remove(f)

def GetGradesFromFolder(path_to_json):
    gradesToReturn=[]
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    for json_file in json_files:
        with open(f"{path_to_json}{json_file}", "r") as f:
            gradesToReturn.append(json.loads(f.read(), object_hook=lambda d: SimpleNamespace(**d)))
    return gradesToReturn

DeleteTemp(new_temp_grades)
grades = GetGradesFromFolder(old_grades)

# Piece code from vulcan api, I don't know how it works, but works
async def main():  
    with open("keystore.json") as f:
        keystore = Keystore.load(f)

    with open("account.json") as f:
        account = Account.load(f)

    client = Vulcan(keystore, account)
    await client.select_student()

    now_grades = await client.data.get_grades()

    now_grades = [grade async for grade in now_grades]
    
    for grade in now_grades:
        with open(f"tempgrades/{grade.key}.json", "w") as f:
            f.write(grade.as_json)
    
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

now_grades = GetGradesFromFolder(new_temp_grades)

for item in now_grades:
    if item not in grades:
        new_grades.append(item)

for g in new_grades:
    print(f"CLMN_NAME: {g.Column.Name} CODE_NAME: {g.Column.Code} SUBJ_NAME: {g.Column.Subject.Name} MARK_INFO: {g.DateCreated.Date} {g.DateCreated.Time} TECH_NAME: {g.Creator.DisplayName}", end="\n\n")
    #print(g, end="\n\n")

DeleteTemp(old_grades)

for file_name in os.listdir(new_temp_grades):
    # construct full file path
    source = new_temp_grades + file_name
    destination = old_grades + file_name
    # move only files
    if os.path.isfile(source):
        shutil.move(source, destination)

# TODO:
# - Make markdown
# - Add discord webhooks