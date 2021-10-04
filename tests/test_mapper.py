import string
from mapper.mapper import create_map,create_markers,list_markers,edit_markers
import random

Baseurl = 'https://cartes.io/'
test_map_id = "bc105f33-f83b-4eab-89e3-30288c3f2ce9"
test_marker_id = '1431'
test_marker_token = "7muIXhEHClVrhEtWj1BpBhpYHV213TRv"
test_longitute = random.randrange(-179,179)
test_latitude =  random.randrange(-89,89)
test_category_name= ''.join(random.choices(string.ascii_letters, k=7))
print(test_latitude,test_longitute,test_category_name)

def test_create_map():
    r = create_map()
    assert r.status_code == 200

def test_create_markers():
    r = create_markers(map_id=test_map_id,lat=test_latitude,long=test_longitute,cat_name=test_category_name)
    assert r.status_code == 201

def test_list_markers():
    r = list_markers(map_id=test_map_id)
    assert r.status_code == 200

def test_edit_markers():
    r = edit_markers(map_id=test_map_id,marker_id=test_marker_id,token=test_marker_token)
    assert r.status_code == 200