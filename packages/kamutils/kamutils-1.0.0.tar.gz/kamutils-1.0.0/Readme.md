Library for converting Oracle SDO GEOMETRY into spatial objects which implements the [\_\_geo_interface\_\_](https://gist.github.com/sgillies/2217756) protocol (GeoJSON-like dict).  
Supported geometry types are : Point, Linestring, Polygon, MultiPoint, MultiLinestring, MultiPolygon and Collection.  

Converted geometry can be used directly by other packages that support **\_\_geo_interface\_\_** like [Shapely](https://shapely.readthedocs.io/en/stable/manual.html) or [GeoPandas](https://geopandas.org/en/stable).  
*Kamutils* provides a WKT representation (Well Known Text) of the converted geometry.

*Kamutils* allows geometry conversion for database versions that does not implement `SDO_UTIL` methods like `TO_WKTGEOMETRY` or `TO_JSON` / `TO_GEOJSON`, or implement them partially.  
For example, you may encounter an error `3D geometries are not supported by geometry WKB/WKT generation` with method `SDO_UTIL.TO_WKTGEOMETRY` if you have 3D geometry with X,Y,Z coordinates.

*Kamutils* includes other miscellaneous utilities.

## License
*Kamutils* is licensed under CeCILL-B license, a BSD-like french/european license.

License in English : https://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html  
License in French : https://www.cecill.info/licences/Licence_CeCILL-B_V1-fr.html

## Requirements
*Kamutils* has been tested with :

- Python 3.7
- oracledb 1.1.1

Dependencies : none

## Oracle SDO GEOMETRY conversion
### Example 1 - Read and convert geometry with **convert_from_sdo_geometry()**
	import oracledb
	from kamutils.spatial import convert_from_sdo_geometry

	oracledb.init_oracle_client()
	connection = oracledb.connect(user="Test", password="********", dsn="MY_DSN")

	with connection.cursor() as cursor:
		cursor.execute("select geometry, ID from MY_BASE.MY_TABLE where ID='l1'")
		row = cursor.fetchone()
		if row:
			spatial_object = convert_from_sdo_geometry(row[0])
			if spatial_object.error is None:
				print('converted object :')
				print(spatial_object)
				print('srid :',spatial_object.srid)
				print('error :',spatial_object.error)
				print('to WKT:')
				print(spatial_object.wkt())
			else:
				print(spatial_object.error)
				print('id :',spatial_object.error.id)
				print('msg :',spatial_object.error.msg)

output :

	converted object :
	<SpatialObject - type:LineString srid:None {'type': 'LineString', 'coordinates': [(10.0, 25.0, 0.0), (20.0, 30.0, 0.0), (25.0, 25.0, 0.0), (30.0, 30.0, 0.0)], 'measures': None}>
	srid : None
	error : None
	to WKT:
	LINESTRING Z(10.0 25.0 0.0,20.0 30.0 0.0,25.0 25.0 0.0,30.0 30.0 0.0)

output in case of error :

	Error 2 : Unknown geometry : SDO_GTYPE = 0
	id : 2
	msg : Unknown geometry : SDO_GTYPE = 0

### Example 2 - Interoperability
	. . .
	spo = convert_from_sdo_geometry(row[0])
	import json
	print('json dump :')
	print(json.dumps(spo.__geo_interface__))
	print()

	from shapely import geometry
	obj=geometry.shape(spo)
	print('shapely :')
	print(type(obj))
	print(obj)
	print()

	import geojson
	obj=geojson.mapping.to_mapping(spo)
	print('geojson :')
	print(type(obj))
	print(obj)
	print()

	import plpygis
	obj=plpygis.Geometry.shape(spo)
	print('plpygis :')
	print(type(obj))
	print(obj)

output :

	json dump :
	{"type": "LineString", "coordinates": [[10.0, 25.0, 0.0], [20.0, 30.0, 0.0], [25.0, 25.0, 0.0], [30.0, 30.0, 0.0]]}

	shapely :
	<class 'shapely.geometry.linestring.LineString'>
	LINESTRING Z (10 25 0, 20 30 0, 25 25 0, 30 30 0)

	geojson :
	<class 'dict'>
	{'type': 'LineString', 'coordinates': [(10.0, 25.0, 0.0), (20.0, 30.0, 0.0), (25.0, 25.0, 0.0), (30.0, 30.0, 0.0)]}

	plpygis :
	<class 'plpygis.geometry.LineString'>
	01020000800400000000000000000024400000000000003940000000000000000000000000000034400000000000003e4
	000000000000000000000000000003940000000000000394000000000000000000000000000003e400000000000003e40
	0000000000000000

### Example 3 - Conversion to ArcGis geometry
	import arcpy
	. . .
	spo = convert_from_sdo_geometry(row[0])
	if spo.srid is None:
		# supposing you know the actual coordinates system of the source geometry
		srid = KNOWN_SRID
	else:
		srid = spo.srid
	arcpy_geom = arcpy.FromWKT(spo.wkt(), arcpy.SpatialReference(srid))

### Classes and fonctions
Function `convert_from_sdo_geometry` : converts a `SDO_GEOMETRY` object and returns a `SpatialObject` instance.  
Module : `kamutils.spatial`

Class `SpatialObject`  
Module : `kamutils.spatial`  
Properties :
- `type` : returns the geometry type (see [Geometry types constants](#geometry-types))
- `srid` : returns the srid (Spatial Reference IDentifier) wich identifies the coordinate system of the geometry. If not defined, return `None`
- `error` : returns the conversion error if any or `None`.  
`error` is an instance of class `Error`
- `__geo_interface__` : returns a GeoJSON dict representation of the geometry. The geometry is not converted to EPSG:4326 regardless of its srid.
- `is_valid` : returns `True` if the geometry is valid, i.e. there is no conversion error, `False` in other cases

Methods :
- `wkt()` : returns the WKT representation of the geometry
- `geometries()` : returns an iterator over all sub-objects in case of a collection (flattening all sub-collections). If the `SpatialObject` is not a collection, the iterator returns the object itself.


Class `Error`  
Module : `kamutils.exceptions`  
Attributes :
- `id` : returns the error id (see [Error codes](#error-codes))
- `msg` : returns the error message

### <a id="geometry-types"></a>Geometry types
To import Geometry types constants :

	from kamutils.spatial import GEOMETRY_TYPE

Constant list :
| Constant name | Value |
| --------- | :---------: |
| GEOMETRY_TYPE.POINT | 1 |
| GEOMETRY_TYPE.LINESTRING | 2 |
| GEOMETRY_TYPE.POLYGON | 3 |
| GEOMETRY_TYPE.COLLECTION | 4 |
| GEOMETRY_TYPE.MULTIPOINT | 5 |
| GEOMETRY_TYPE.MULTILINESTRING | 6 |
| GEOMETRY_TYPE.MULTIPOLYGON | 7 |


### <a id="error-codes"></a>Error codes
To import Error codes constants :

	from kamutils.exceptions import ERROR

Constant list :
| Constant name | Value |
| --------- | :---------: |
| ERROR.EXCEPTION | -1 |
| ERROR.INVALID_SDO_GEOMETRY | 1 |
| ERROR.UNKNOW_TYPE | 2 |
| ERROR.UNSUPPORTED_GEOMETRY | 3 |
| ERROR.INVALID_GEOMETRY | 4

### Limitations
The following geometry types are partially supported :
| SDO_ETYPE | SDO_INTERPRETATION | Type (\*) | Limitation | 
| :-------: | :---------: | ----------- | ----------- |
| 1 | 0 | Oriented point | The point is converted but the orientation is ignored |
| 1 | > 1 | Point cluster | Converted to `Multipoint` |
| 2 | 2 | Line string made up of circular arcs | Circular arcs are transformed into straight line segments connecting the arc's coordinates |
| 4 | > 1 | Compound line string with vertices connected by straight line segments or by circular arcs | Circular arcs are transformed into straight line segments connecting the arc's coordinates |
| 1003<br>2003 | 2 | Polygon made up of a connected sequence of circular arcs | Circular arcs are transformed into straight line segments connecting the arc's coordinates |
| 1005<br>2005 |  | Compound polygon with some vertices connected by straight line segments and some by circular arcs | Circular arcs are transformed into straight line segments connecting the arc's coordinates |

\* From [Oracle SDO_GEOMETRY Object Type - Values and Semantics in SDO_ELEM_INFO](https://docs.oracle.com/en/database/oracle/oracle-database/21/spatl/spatial-datatypes-metadata.html#GUID-270AE39D-7B83-46D0-9DD6-E5D99C045021)

The following geometry types are not supported by the current version. They produce an error `UNSUPPORTED_GEOMETRY`.
| SDO_ETYPE | SDO_INTERPRETATION | Type (\*) |
| :-------: | :---------: | ----------- |
| 0 |  | Geometry types not supported by Oracle Spatial |
| 2 | 3 | NURBS curve |
| 1003 | 3 | Optimized rectangle |
| 1003 | 4 | Circle |
| 1007 | 1 | Solid |
| 1007 | 3 | Solid of type 'optimized box' |
| 1008 |  | Multi Solid |
| 2003 | 3 | Optimized rectangle |
| 2003 | 4 | Circle |

## Other utilities
### RangeSet
*RangeSet* creates a set of intervals to categorize values in different levels.  
*RangeSet* support numeric values for ranges.

#### Example :
	from kamutils.analyse import RangeSet

	s = RangeSet(1,2,5)
	print("Levels :")
	print(s)
	print()
	for v in [1, 1.5, 2, 2.1, 12]:
		r = s.level(v)
		print("Level of {:>4}".format(v),":",r,"      ",s.label(r))
	print()
	print("Last level :",s.last_level(),'\n')

	# ranges can be defined with just the upper bound of each interval like above
	# or with lower and upper bounds defined, or a combination or both
	s = RangeSet(1,(2,4),5,6,7,(7,9),11)
	print("Levels :")
	print(s)
	print()
	for v in [0, 1.5, 2]:
		r = s.level(v)
		print("Level of {:>4}".format(v),":",r,"      ",s.label(r))
	print()
	print("Last level :",s.last_level(),'\n')

output :

	Levels :
	0:<= 1
	1:1]..2]
	2:2]..5]
	3:> 5

	Level of    1 : 0        <= 1
	Level of  1.5 : 1        1]..2]
	Level of    2 : 1        1]..2]
	Level of  2.1 : 2        2]..5]
	Level of   12 : 3        > 5

	Last level : 3 

	Levels :
	0:<= 1
	1:1]..[2
	2:[2..4]
	3:4]..5]
	4:5]..6]
	5:6]..7]
	6:7]..9]
	7:9]..11]
	8:> 11

	Level of    0 : 0        <= 1
	Level of  1.5 : 1        1]..[2
	Level of    2 : 2        [2..4]

	Last level : 8 
