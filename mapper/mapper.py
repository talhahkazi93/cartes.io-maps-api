# Cartes.io maps for creation of map and map markers.
# author : Talha kazi

import sys, requests, json,os, argparse

# script path
script_path = os.path.dirname(os.path.realpath(__file__))
# Cartes.io Constant
CARTES_BASE_URL = 'https://cartes.io/'

# Writing json to file
def json_dump(dict:dict,file_name:str,mode:str = 'a' ) -> None:
    file_path  = script_path+ "\\" + file_name
    with open(file_path,mode) as fp:
        json.dump(dict,fp,sort_keys=True,indent=4)

# creating post , put , get requests and featching its response
def post_cartes(url:str,data:dict,req:str) -> requests.models.Response:
    retry_count = 0
    response:requests.models.Response
    while retry_count < 5:
        try:
            if(req == 'POST'):
                response = requests.post(url=url,data=data)
            elif(req == 'GET'):
                response = requests.get(url=url, data=data)
            elif(req ==  'PUT'):
                response = requests.put(url=url, data=data)
            break
        except Exception as e:
            retry_count += 1
    if retry_count == 5:
        sys.exit("Operation failed for" + url)
    elif not response or response.status_code >= 400:
        sys.exit("Could not create object for:" + url +" status code:"+str(response.status_code))
    return response

# Create a map : POST /api/maps
def create_map(map_title:str=None,map_des:str=None,slug:str=None,privacy:str="public",c_marker:str="yes")-> tuple[dict,requests.models.Response]:
    url = CARTES_BASE_URL + 'api/maps'
    data = {
        "title" : map_title,
        "slug" : slug,
        "description" : map_des,
        "privacy" : privacy,
        "users_can_create_markers": c_marker
    }
    r = post_cartes(url,data,'POST')
    sys.stderr.write("creation of map:" + str(r.status_code))
    if r.status_code <=202:
        if r.headers.get('content-type') == 'application/json':
            res = json.loads(r.text)
        else:
            sys.exit('Error in map input parameters')
    return res,r

# Create a marker on a map : POST /api/maps/{map-id}/markers
def create_markers(map_id:str,lat:int,long:int,category:int=None,cat_name:str=None,mar_des:str=None)-> tuple[dict,requests.models.Response]:
    url = CARTES_BASE_URL + 'api/maps/' + map_id + '/markers'
    data ={
        "lat" : lat,
        "lng" : long,
        "description" : mar_des
    }
    if category:
        data["category"] = category
    elif cat_name:
        data["category_name"] = cat_name
    else:
        sys.exit("Category name or Category is required")

    r = post_cartes(url,data,'POST')
    sys.stderr.write("creation of markers:" + str(r.status_code))
    if r.status_code <= 202:
        if r.headers.get('content-type') == 'application/json':
            res = json.loads(r.text)
        else:
            sys.exit(' Error occur in creation of markers, check input parameters(may be duplicate)')
    return res,r

# Get all markers on a map : GET /api/maps/{map-id}/markers
def list_markers(map_id:str)-> tuple[dict,requests.models.Response]:
    url = CARTES_BASE_URL + 'api/maps/' + map_id + '/markers'
    data:dict = {}
    r = post_cartes(url,data,'GET')
    sys.stderr.write("list markers:" + str(r.status_code))
    if r.status_code <= 202:
        if r.headers.get('content-type') == 'application/json':
            res = json.loads(r.text)
        else:
            sys.exit('Error in list markers')
    return res,r

# Edit a marker on a map : PUT /api/maps/{map-id}/markers/{marker-id}
def edit_markers(map_id:str,marker_id:str,token:str,des:str=None) -> tuple[dict,requests.models.Response]:
    url = CARTES_BASE_URL + 'api/maps/' + map_id + '/markers/' + marker_id
    data = {
        "description": des,
        "token": token
    }
    r = post_cartes(url,data,'PUT')
    sys.stderr.write("edit markers:" + str(r.status_code))
    if r.status_code <= 202:
        if r.headers.get('content-type') == 'application/json':
            res = json.loads(r.text)
        else:
            sys.exit('Error in list markers')
    return res,r

def main():
    parser = argparse.ArgumentParser(description='Validate')
    # Map Parameter
    parser.add_argument('-mt', dest='maptitle', help='map-title', nargs='?', const="",type=str)
    parser.add_argument('-mi', dest='mapid', help='map-id',type=str)
    parser.add_argument('-md', dest='mapdes', help='map-description', nargs='?',default="",type=str)
    parser.add_argument('-mp', dest='mappriv', help='map-privacy',default='public',type=str)
    parser.add_argument('-mu', dest='mapusr', help='map-usersetting', default='yes',type=str)

    # Marker Parameter
    parser.add_argument('-rt', action='append', dest='ip', help='marker-title', nargs='?', default="",type=str)
    parser.add_argument('-ri', dest='marid', help='marker-id', nargs='?', type=str)
    parser.add_argument('-rn', dest='marctnm', help='marker-categoryname',nargs='?',type=str)
    parser.add_argument('-rc', dest='marcat', help='marker-category', nargs='?',type=int)
    parser.add_argument('-rl', dest='marlat', help='marker-lattitude', nargs='?',type=int)
    parser.add_argument('-rg', dest='marlong', help='marker-longitude', nargs='?',type=int)
    parser.add_argument('-rd', dest='mardes', help='marker-description', nargs='?', default="", type=str)
    parser.add_argument('-rk', dest='martoken', help='marker-token', nargs='?', type=str)

    # Modes Of Operation
    g = parser.add_argument_group()
    g.add_argument('-m',"--createmap", action='append', dest='createmap', help='Create-map', nargs='?', const="")
    g.add_argument('-c',"--createmarker", action='append', dest='createmarker', help='Create-marker', nargs='?', const="")
    g.add_argument('-l',"--listmarker", action='append', dest='listmarker', help='list-marker', nargs='?', const="")
    g.add_argument('-e',"--editmarker", action='append', dest='editmarker', help='edit-marker', nargs='?', const="")

    args = parser.parse_args()
    if not (args.createmap or args.createmarker or args.listmarker or args.editmarker):
        sys.exit('no mode of operation selected. Plese select from -m, c, l, e\n')

    # creation of map
    if args.createmap:
        map,r = create_map(map_title=args.maptitle,map_des=args.mapdes,slug=None,privacy=args.mappriv,c_marker=args.mapusr)
        map_id = map["uuid"]
        map_token = map["token"]
        json_dump(map, 'map_'+str(map_id))
        print(map)

    # creation of markers
    if args.createmarker:
        if 'map_id' in locals():
            args.mapid = map_id
        if (args.createmap == None and args.mapid == None or (args.marlat == None or args.marlong == None) or (
                args.marctnm == None and args.marcat == None)):
            parser.error('Creation of markers required map id , latitude , longitaude and category id or name')
        marker,r = create_markers(map_id=args.mapid,lat=args.marlat,long=args.marlong,cat_name=args.marctnm,category=args.marcat)
        marker_id = marker["id"]
        marker_token = marker["token"]
        json_dump(marker, 'map_' + str(args.mapid))
        print(marker)

    # edit markers
    if args.editmarker:
        if (args.createmap == None and args.mapid == None or (args.martoken == None or args.marid == None)):
            parser.error('edit of markers required map id,marker id and marker token')
        em,r = edit_markers(map_id=args.mapid,marker_id=args.marid,token=args.martoken,des=args.mardes)
        print(em)


    # list all markers
    if args.listmarker:
        if (args.createmap == None and args.mapid == None):
            parser.error('list of markers required map id')
        lst_marker,r = list_markers(map_id=args.mapid)
        markerid = [ str(i["id"]) for i in lst_marker]
        print(markerid)
        json_dump(lst_marker, 'map_' + str(args.mapid)+'_markers','w')


if __name__ == '__main__':

    main()


