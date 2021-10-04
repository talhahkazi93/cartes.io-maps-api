# Mapper for Cartes.io
Using API we generate map with markers in cartes.io

### Dependencies

* [request](https://docs.python-requests.org/en/latest/) (Requests is an elegant and simple HTTP library for Python, built for human beings.)
* [mypy](http://mypy-lang.org/) (Mypy is an optional static type checker for Python)


### Main function
The main function is the `main()` function in `mapper.py`.

### Arguments

**[Modes of operation]** Select request.

* Use `-m` to create a map .
  * parameter required : None
* Use `-c` create a marker.
  * parameter required : map_id, latitude, longitude, category name or category id
* Use `-l` to prioritize by the objective.
  * parameter required : map_id
* Use `-e` for first-in-first-out search.
  * parameter required : map_id, marker_id & token

**[map-title]** can be set by using `-mt` identifier 

**[map-id]** can be set by using `-mi` identifier 

**[map-description]** can be set by using `-md` identifier 

**[map-privacy]** can be set by using `-mp` identifier 

**[map-usersetting]** can be set by using `-mu` identifier 

**[marker-title]** can be set by using `-rt` identifier 

**[marker-id]** can be set by using `-ri` identifier 

**[marker-categoryname]** can be set by using `-rn` identifier 

**[marker-category]** can be set by using `-rc` identifier 

**[marker-lattitude]** can be set by using `-rl` identifier 

**[arker-longitude]** can be set by using `-rg` identifier 

**[marker-description]** can be set by using `-rd` identifier 

**[marker-token]** can be set by using `-rk` identifier 

"# razakazi-t" 
