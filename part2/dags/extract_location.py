import os , sys

def extract_loc(file:str,admincodes:list) -> dict:
    with open(file) as f:
        lines = f.readlines()
    locations = {}
    for line in lines:
        a = line.split('\t')
        admincode = a[4]
        if admincode in admincodes:
            locations[a[1]+a[2]] = {}
            locations[a[1] + a[2]]["latitude"] = a[9]
            locations[a[1] + a[2]]["longitude"] = a[10]

    return locations

def run_loc(file , admincode,ti):
    # path = os.path.join(sys.path[0],"DE.txt")
    locs = extract_loc(file=file, admincodes=admincode)
    # print(locs)
    ti.xcom_push(key='locations_dict',value=locs)
    # return locs

# from subprocess import Popen, PIPE
# # path = os.path.join(sys.path[0],"DE.txt")
# path = '..\..\Kazi\PycharmProjects\cartes.io'
# p = Popen(['python','-m','mapper'],stdin=PIPE, stdout=PIPE, stderr=PIPE)
# output, err = p.communicate()
# val = output.decode("utf-8")
# print(val)

# from subprocess import Popen, PIPE
# import time
# path = os.path.join(sys.path[0],"DE.txt")
# mapid = '060e1fea-bc79-4a29-bd87-e7a577361d3b'
# markers = run_loc(file=path,admincode='["BE"]')
#
# for key,value in markers.items():
#     print("================================+++++++++++++++++++++++++++++++++++++++++++++++++")
#     path = os.path.join(sys.path[0], "mapper.py")
#     p = Popen(['python', path, '-c','-mi',mapid,'-rn',key,'-rl',value['latitude'],'-rg',value['longitude']],
#               stdin=PIPE, stdout=PIPE, stderr=PIPE)
#     output, err = p.communicate()
#     val = output.decode("utf-8")
#     print(val)
#     print(err)
#     time.sleep(5)