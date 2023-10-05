from .exceptions import *
from .misc import lower_first_level_keys

#-----------------------------------------------------------------------------------------
# Module CONSTANTS
#-----------------------------------------------------------------------------------------

class GeometryTypeNamespace:
	__slots__ = ()
	# Geometry types
	# For SDO Geometry, values retrieved from https://docs.oracle.com/en/database/oracle/oracle-database/21/spatl/spatial-datatypes-metadata.html#GUID-79D7620B-5526-40FD-9604-9642B79908F2
	# on 07/11/2022
	POINT = 1
	LINESTRING = 2
	POLYGON = 3
	COLLECTION = 4
	MULTIPOINT = 5
	MULTILINESTRING = 6
	MULTIPOLYGON = 7
	SOLID = 8
	MULTISOLID = 9
	# multi type mapping
	MULTI = {
		POINT: MULTIPOINT,
		LINESTRING: MULTILINESTRING,
		POLYGON: MULTIPOLYGON,
		COLLECTION: COLLECTION,
		MULTIPOINT: MULTIPOINT,
		MULTILINESTRING: MULTILINESTRING,
		MULTIPOLYGON: MULTIPOLYGON,
		SOLID: MULTISOLID,
		MULTISOLID: MULTISOLID
	}
	REPR = 	{	POINT: 'Point',
				LINESTRING: 'LineString',
				POLYGON: 'Polygon',
				COLLECTION: 'GeometryCollection',
				MULTIPOINT: 'MultiPoint',
				MULTILINESTRING: 'MultiLineString',
				MULTIPOLYGON: 'MultiPolygon',
				SOLID: 'Solid', # not part of GeoJson standard
				MULTISOLID: 'MultiSolid' # not part of GeoJson standard
			}
	# GeoJson type mapping
	JSON_REPR = { 	POINT: REPR[POINT],
					LINESTRING: REPR[LINESTRING],
					POLYGON: REPR[POLYGON],
					COLLECTION: REPR[COLLECTION],
					MULTIPOINT: REPR[MULTIPOINT],
					MULTILINESTRING: REPR[MULTILINESTRING],
					MULTIPOLYGON: REPR[MULTIPOLYGON],
				}
	# WKT type mapping
	WKT_REPR = { 	POINT: 'POINT',
					LINESTRING: 'LINESTRING',
					POLYGON: 'POLYGON',
					COLLECTION: 'GEOMETRYCOLLECTION',
					MULTIPOINT: 'MULTIPOINT',
					MULTILINESTRING: 'MULTILINESTRING',
					MULTIPOLYGON: 'MULTIPOLYGON',
					SOLID: 'POLYHEDRALSURFACE'
				}

GEOMETRY_TYPE = GeometryTypeNamespace()

#-----------------------------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------------------------

# Caracteristics of an SDO Geometry object
class _SDOElement:
	__slots__ = ('type','variant','compound','unsupported','ignore')

	def __init__(self,type=None, variant=None, compound=False, unsupported=False, ignore=False):
		self.type = type
		self.variant = variant
		self.compound = compound
		self.unsupported = unsupported
		self.ignore = ignore

# Method used by class Shape
def coordinates_to_wkt(coordinates, measures=None):
	no_M = measures is None
	if isinstance(coordinates, tuple):
		if no_M: # favour common cases without LRS
			return ' '.join(str(coord) for coord in coordinates) # join insert the separator ' ' between list items
		else:
			return ' '.join(str(coord) for coord in coordinates) + ' ' + str(measures)
	else:
		if no_M:
			_list = [coordinates_to_wkt(coord) for coord in coordinates]
		else:
			_list = [coordinates_to_wkt(coord, measure) for coord, measure in zip(coordinates, measures)]
		if len(_list) == 1:
			return f"({_list[0]})"
		else:
			return f"({','.join(_list)})" # join insert the separator ',' between list items

# Shape : represents the geometry with its type and coordinates
class Shape:
	__slots__ = ('_type', '_has_Z','_coordinates','_measures','_collection')

	def __init__(self,type,has_Z,coordinates=None,measures=[],collection=None):
		self._type = type
		self._has_Z = has_Z
		self._coordinates = coordinates
		if isinstance(measures,list) and len(measures) == 0:
			self._measures = None
		else:
			self._measures = measures
		self._collection = collection

	def wkt(self): 
		"""Returns the WKT representation of the geometry"""
		if self._measures is None:
			if self._has_Z:
				dims = ' Z'
			else:
				dims = ' '
		else:
			if self._has_Z:
				dims = ' ZM'
			else:
				dims = ' M'
		if self._collection is None:
			if self._coordinates is None: # to check : _type is supposed not to be None, but is this right ?
				return f"{GEOMETRY_TYPE.WKT_REPR[self._type]}{dims}EMPTY"
			else:
				if self._type == GEOMETRY_TYPE.POINT:
					return f"{GEOMETRY_TYPE.WKT_REPR[self._type]}{dims}({coordinates_to_wkt(self._coordinates, self._measures)})"
				else:
					return f"{GEOMETRY_TYPE.WKT_REPR[self._type]}{dims}{coordinates_to_wkt(self._coordinates, self._measures)}"
		else: # collection
			_list = [shape.wkt() for shape in self._collection]
			if len(_list) == 1:
				return f"{GEOMETRY_TYPE.WKT_REPR[self._type]}{dims}({_list[0]})"
			else:
				return f"{GEOMETRY_TYPE.WKT_REPR[self._type]}{dims}({','.join(_list)})"

	@property
	def geometry(self):
		"""Returns a dict representation of the geometry"""
		return {"type":GEOMETRY_TYPE.REPR[self._type], "coordinates": self._coordinates, "measures": self._measures}

# SpatialObject : represents a 2D or 3D object with geometry, SRID and potential error
class SpatialObject:
	__slots__ = ('_shape', '_srid', '_error')

	def __init__(self,*args,**kwargs):
		self._shape = None
		for arg in args:
			if isinstance(arg,Shape): # init _shape with the first one
				self._shape = arg
				break
		kwargs = lower_first_level_keys(kwargs)
		self._srid = kwargs.get('srid', None) # private / Spatial Reference IDentifier
		self._error = kwargs.get('error', None) # private / Potential error with id & msg or None
		if self._shape is None:
			self._shape = kwargs.get('shape', None) # private / Geometry

	def geometry_repr(self):
		if self._shape is None:
			return None
		else:
			if self._shape._type == GEOMETRY_TYPE.COLLECTION:
				collection = [SpatialObject(shape=shape,srid=self.srid,error=self.error).geometry_repr() for shape in self._shape._collection]
				return {"collection":collection}
			else:
				return self._shape.geometry

	def __repr__(self):
		if self._error is None:
			if self._shape is None:
				return f"<{self.__class__.__name__} - empty>"
			else:
				if self._shape._type == GEOMETRY_TYPE.COLLECTION:
					return f"<{self.__class__.__name__} - type:{GEOMETRY_TYPE.REPR[self._shape._type]} srid:{self._srid} {self.geometry_repr()}>"
				else:
					return f"<{self.__class__.__name__} - type:{GEOMETRY_TYPE.REPR[self._shape._type]} srid:{self._srid} {self._shape.geometry}>"
		else:
			return f"<{self.__class__.__name__} - {self._error.__repr__()}>"

	@property
	def type(self): # type getter
		return self._shape._type

	@property
	def shape(self): # shape getter
		return self._shape

	@property
	def srid(self): # srid getter
		return self._srid

	@property
	def error(self): # error getter
		return self._error

	@property
	def __geo_interface__(self): # GeoJSON-like representation - cf https://gist.github.com/sgillies/2217756
		if self._shape is None:
			return None
		else:
			if self._shape._type == GEOMETRY_TYPE.COLLECTION:
				return({"type": GEOMETRY_TYPE.JSON_REPR[GEOMETRY_TYPE.COLLECTION], "geometries": [{"type": GEOMETRY_TYPE.JSON_REPR[shape._type], "coordinates": shape._coordinates} for shape in self._shape._collection]})
			else:
				return({"type": GEOMETRY_TYPE.JSON_REPR[self._shape._type], "coordinates": self._shape._coordinates})

	@property
	def is_valid(self): # return True if the geometry is valid, i.e. there is no conversion error / False in other cases
		return self._error is None

	def geometries(self): 
		"""Returns this object or an iterator over all sub-spatial objects in case of a collection (flatten the sub-collections)."""
		if self._shape is None:
			yield None
		else:
			if self._shape._collection is None:
				yield self
			else:
				for shape in self._shape._collection:
					yield from SpatialObject(shape=shape,srid=self.srid,error=self.error).geometries()

	def wkt(self):
		return self._shape.wkt()

#-----------------------------------------------------------------------------------------
# SDO Geometry conversion : create a SpatialObject object from an Oracle SDO_GEOMETRY Object 
#-----------------------------------------------------------------------------------------

# Variants
_EXTERIOR = 1
_INTERIOR = 2
_CLUSTER = 3

# SDO_ETYPE / SDO_INTERPRETATION mapping
_sdo_elem_types = {
	0: _SDOElement(unsupported=True),
	(1,1): _SDOElement(type=GEOMETRY_TYPE.POINT),
	(1,0): _SDOElement(ignore=True), # Orientation for an oriented point.
	1: _SDOElement(type=GEOMETRY_TYPE.POINT, variant=_CLUSTER), # Point cluster with n points.
	(2,1): _SDOElement(type=GEOMETRY_TYPE.LINESTRING), # Line string whose vertices are connected by straight line segments.
	(2,2): _SDOElement(type=GEOMETRY_TYPE.LINESTRING), # Line string made up of a connected sequence of circular arcs.
	(2,3): _SDOElement(unsupported=True), # NURBS (non-uniform rational B-spline) curve. For more information, see NURBS Curve Support in Oracle Spatial.
	3: _SDOElement(type=GEOMETRY_TYPE.POLYGON, variant=_EXTERIOR), # cf Note: the use of 3 as an SDO_ETYPE value for polygon ring elements in a single geometry is discouraged. You should specify 3 only if you do not know if the simple polygon is exterior or interior
	4: _SDOElement(type=GEOMETRY_TYPE.LINESTRING, compound=True), # Compound line string with some vertices connected by straight line segments and some by circular arcs
	(1003,1): _SDOElement(type=GEOMETRY_TYPE.POLYGON, variant=_EXTERIOR), # Simple polygon whose vertices are connected by straight line segments.
	(1003,2): _SDOElement(type=GEOMETRY_TYPE.POLYGON, variant=_EXTERIOR), # Polygon made up of a connected sequence of circular arcs that closes on itself.
	(1003,3): _SDOElement(unsupported=True), # Rectangle type (sometimes called optimized rectangle).
	(1003,4): _SDOElement(unsupported=True), # Circle type.
	1005: _SDOElement(type=GEOMETRY_TYPE.POLYGON, variant=_EXTERIOR, compound=True), # Compound polygon with some vertices connected by straight line segments and some by circular arcs.
	1006: _SDOElement(type=GEOMETRY_TYPE.MULTIPOLYGON, variant=_EXTERIOR, compound=True), # Surface consisting of one or more polygons, with each edge shared by no more than two polygons.
	(1007,1) : _SDOElement(unsupported=True), # Solid
	#ToDo : restore (1007,1) : _SDOElement(type=GEOMETRY_TYPE.SOLID, compound=True), # Solid consisting of multiple surfaces that are completely enclosed in a three-dimensional space, so that the solid has an interior volume. A solid element can have one exterior surface defined by the 1006 elements and zero or more interior boundaries defined by the 2006 elements. The value n in the Interpretation column must be 1 or 3.
	(1007,3) : _SDOElement(unsupported=True), # Solid of type 'optimized box'
	1008 : _SDOElement(unsupported=True), # Composite solid formed by multiple adjacent simple solids
	#ToDo : restore 1008 : _SDOElement(type=GEOMETRY_TYPE.MULTISOLID, compound=True), # Composite solid formed by multiple adjacent simple solids: one element type 1008 (holding the count of simple solids), followed by any number of element type 1007 (each describing one simple solid)
	(2003,1): _SDOElement(type=GEOMETRY_TYPE.POLYGON, variant=_INTERIOR), # Simple polygon whose vertices are connected by straight line segments.
	(2003,2): _SDOElement(type=GEOMETRY_TYPE.POLYGON, variant=_INTERIOR), # Polygon made up of a connected sequence of circular arcs that closes on itself.
	(2003,3): _SDOElement(unsupported=True), # Rectangle type (sometimes called optimized rectangle).
	(2003,4): _SDOElement(unsupported=True), # Circle type.
	2005: _SDOElement(type=GEOMETRY_TYPE.POLYGON, variant=_INTERIOR, compound=True), # Compound polygon with some vertices connected by straight line segments and some by circular arcs.
	2006: _SDOElement(type=GEOMETRY_TYPE.MULTIPOLYGON, variant=_INTERIOR, compound=True), # Surface consisting of one or more polygons, with each edge shared by no more than two polygons.
}

# Conversion function
def convert_from_sdo_geometry(sdo_geometry):

	# recursive sub-function
	# ToDo : see usage considerations 2.2.6 to ignore some combinations ?
	def get_element(elem_idx,collect_polygon_rings=None,collect_surfaces=None): # returns a tuple : element, index of the next triplet to process in sdo_elem_info
		# When collect_polygon_rings or collect_surfaces is set, returns None if the element is not of the expected type/variant
		sdo_etype = int(sdo_elem_info.getelement(elem_idx+1))
		sdo_interpretation = int(sdo_elem_info.getelement(elem_idx+2))
		sdo_elem = _sdo_elem_types.get((sdo_etype, sdo_interpretation))
		if sdo_elem is None:
			sdo_elem = _sdo_elem_types.get(sdo_etype)
			if sdo_elem is None:
				raise KamException(ERROR.UNKNOW_TYPE,f"Unknown element type : SDO_ETYPE = {sdo_etype} / SDO_INTERPRETATION = {sdo_interpretation}")
		if sdo_elem.unsupported:
			raise ConversionException(ERROR.UNSUPPORTED_GEOMETRY,f"Unsupported geometry : SDO_ETYPE = {sdo_etype} / SDO_INTERPRETATION = {sdo_interpretation}")
		if sdo_elem.ignore:
			return None, elem_idx + 3

		if ((collect_surfaces is not None) and (sdo_elem.type != GEOMETRY_TYPE.MULTIPOLYGON)) or ((collect_polygon_rings is not None) and (sdo_elem.type != GEOMETRY_TYPE.POLYGON)):
			return None, elem_idx
		if sdo_elem.type == GEOMETRY_TYPE.MULTIPOLYGON:
			if collect_surfaces is None:
				if sdo_elem.variant == _INTERIOR:
					pass
					# ToDo ? Independant interior surface is converted as MultiPolygon but could also raise following error :
					# raise ConversionException(ERROR.INVALID_GEOMETRY,'Interior surface must be part of a SOLID')
			elif sdo_elem.variant != collect_surfaces:
				if sdo_elem.variant == _INTERIOR:
					raise ConversionException(ERROR.INVALID_GEOMETRY,'Invalid SOLID : missing exterior surface')
				else: # exterior surface but collecting interior surface -> stop building the current SOLID
					return None, elem_idx
		elif sdo_elem.type == GEOMETRY_TYPE.POLYGON:
			if collect_polygon_rings is None:
				if sdo_elem.variant == _INTERIOR: # polygons should start with an exterior ring
					raise ConversionException(ERROR.INVALID_GEOMETRY,'Invalid POLYGON : missing exterior ring')
				else:
					polygon,elem_idx = get_element(elem_idx,collect_polygon_rings=_EXTERIOR)
					while elem_idx < sdo_elem_len:
						element,elem_idx = get_element(elem_idx,collect_polygon_rings=_INTERIOR)
						if element is None: # No more interior rings
							break
						else:
							# Combine interior rings of polygons with exterior ring
							polygon._coordinates.extend(element._coordinates)
							if has_M: polygon._measures.extend(element._measures)
					return polygon, elem_idx
			elif (collect_polygon_rings == _INTERIOR) and (sdo_elem.variant == _EXTERIOR): # another polygon -> stop building the current one
				return None, elem_idx
		
		coordinates = []
		measures = []
		if sdo_elem.compound:
			if (sdo_elem.type == GEOMETRY_TYPE.SOLID):
				# The value of SDO_INTERPRETATION can be :
				# 1 : subsequent triplets in the SDO_ELEM_INFO array describe the exterior 1006 and optional interior 2006 surfaces that make up the solid element.
				# 3 : the solid is an optimized box
				element,elem_idx = get_element(elem_idx+3,collect_surfaces=_EXTERIOR) # exterior_surface first
				if element is None: # solid shoud start with an exterior surface
					raise ConversionException(ERROR.INVALID_GEOMETRY,'Invalid SOLID : missing exterior surface')
				else:
					coordinates = [element._coordinates]
					if has_M: measures = [element._measures]
				while (elem_idx < sdo_elem_len):
					element,elem_idx = get_element(elem_idx,collect_surfaces=_INTERIOR)
					if element is None: # No more interior surfaces
						break
					else:
						coordinates.append(element._coordinates) # Add interior surfaces to SOLID
						if has_M: measures.append(element._measures)
			elif (sdo_elem.type == GEOMETRY_TYPE.MULTIPOLYGON) or (sdo_elem.type == GEOMETRY_TYPE.MULTISOLID):
				# The value of SDO_INTERPRETATION specifies the number of polygons or solids
				elem_count = 0
				elem_idx += 3
				while (elem_idx < sdo_elem_len) and (elem_count < sdo_interpretation):
					# surface with SDO_ETYPE = 2006 is composed of polygon interior boundaries (SDO_ETYPE = 2003 or 2005)
					element,elem_idx = get_element(elem_idx,_INTERIOR if (sdo_elem.variant == _INTERIOR) else None)
					if element is None:
						break
					else:
						coordinates.append(element._coordinates) # add polygon or solid geometry
						if has_M: measures.append(element._measures)
						elem_count += 1
				if elem_count < sdo_interpretation:
					if (sdo_elem.type == GEOMETRY_TYPE.MULTIPOLYGON):
						raise ConversionException(ERROR.INVALID_GEOMETRY,f"Invalid MULTIPOLYGON : {sdo_interpretation} polygons expected but {elem_count} found")
					else:
						raise ConversionException(ERROR.INVALID_GEOMETRY,f"Invalid MULTISOLID : {sdo_interpretation} solids expected but {elem_count} found")
			else:
				# The value of SDO_INTERPRETATION specifies the number of subelements (triplets)
				last_idx = elem_idx + (sdo_interpretation * 3) # index of last subelement
				elem_idx += 3
				while elem_idx <= last_idx:
					element,elem_idx = get_element(elem_idx)
					coordinates.extend(element._coordinates) # Aggregate geometry of subelement
					if has_M: measures.extend(element._measures)
				if sdo_elem.type == GEOMETRY_TYPE.POLYGON:
					coordinates = [coordinates]
					if has_M: measures = [measures]
			return Shape(sdo_elem.type,has_Z,coordinates,measures), elem_idx	
		else:
			# From SDO_GEOMETRY doc : the start and end points for the sequence describing a specific element in the SDO_ORDINATES array are determined 
			# by the STARTING_OFFSET values for that element and the next element in the SDO_ELEM_INFO array.
			sdo_starting_offset = int(sdo_elem_info.getelement(elem_idx)) - 1 # Offset values start at 1 and not at 0.
			elem_idx += 3
			if elem_idx < sdo_elem_len:
				sdo_ending_offset = int(sdo_elem_info.getelement(elem_idx)) - 1 # index of last ordinate + 1
			else: # last element
				sdo_ending_offset = sdo_ordinates.size() # index of last ordinate + 1
			for point_idx in range(sdo_starting_offset,sdo_ending_offset,sdo_dims):
				# coordinates of each point are stored in a tuple
				if has_Z:
					point_coordinates = (sdo_ordinates.getelement(point_idx),sdo_ordinates.getelement(point_idx+1),sdo_ordinates.getelement(point_idx+sdo_Z_offset))
				else:
					point_coordinates = (sdo_ordinates.getelement(point_idx),sdo_ordinates.getelement(point_idx+1))
				coordinates.append(point_coordinates)
				if has_M: measures.append(sdo_ordinates.getelement(point_idx+sdo_M_offset))
			geom_type = sdo_elem.type
			if sdo_elem.type == GEOMETRY_TYPE.POLYGON:
				coordinates = [coordinates]
				if has_M: measures = [measures]
			elif (sdo_elem.type == GEOMETRY_TYPE.POINT):
				if (sdo_elem.variant == _CLUSTER):
					geom_type = GEOMETRY_TYPE.MULTIPOINT
				else:
					coordinates = coordinates.pop()
					if has_M: measures = measures.pop()
			return Shape(geom_type,has_Z,coordinates,measures), elem_idx

	# function 'convert_from_sdo_geometry' main code
	try:
		# Oracle SDO_GEOMETRY Object : https://docs.oracle.com/database/121/SPATL/sdo_geometry-object-type.htm#SPATL490
		try:
			sdo_gtype = int(sdo_geometry.__getattr__('SDO_GTYPE'))
			sdo_srid = sdo_geometry.__getattr__('SDO_SRID')
			if sdo_srid is not None: sdo_srid = int(sdo_srid)
			sdo_elem_info = sdo_geometry.__getattr__('SDO_ELEM_INFO')
			sdo_ordinates = sdo_geometry.__getattr__('SDO_ORDINATES')
		except Exception as exception:
			raise ConversionException(ERROR.INVALID_SDO_GEOMETRY,"Error accessing SDO_GEOMETRY object property : ".join(str(exception)))

		sdo_geom_type = sdo_gtype % 100 # From SDO_GEOMETRY doc : geometry type coded on the last two digits : 00 through 09, with 10 through 99 reserved for future use
		if sdo_geom_type == 0:
			raise ConversionException(ERROR.UNKNOW_TYPE,f"Unknown geometry : SDO_GTYPE = 0")
		sdo_lrs_dim = (sdo_gtype//100) % 10 # From SDO_GEOMETRY doc : linear referencing measure dimension coded on the second digit : 3, 4 or 0
		sdo_dims = sdo_gtype//1000 # From SDO_GEOMETRY doc : number of dimensions coded on the first digit : 2, 3, or 4
		if (sdo_dims == 4) or (sdo_lrs_dim != 0):
			has_M = True
			has_Z = (sdo_dims == 4)
			if sdo_lrs_dim == 0: sdo_lrs_dim = 4 # should not happen ?
			if sdo_lrs_dim == 3:
				sdo_M_offset = 2
				if has_Z: sdo_Z_offset = 3
			else: # sdo_lrs_dim == 4
				sdo_M_offset = 3
				sdo_Z_offset = 2
		else:
			has_M = False
			if sdo_dims == 3:
				has_Z = True
				sdo_Z_offset = 2
			else:
				has_Z = False
		error = None

		if sdo_elem_info is None:
			sdo_point = sdo_geometry.__getattr__('SDO_POINT')
			if sdo_point is None: # No geometry, neither in SDO_ELEM_INFO nor in SDO_POINT --> return an empty point
				return SpatialObject(Shape(GEOMETRY_TYPE.POINT,has_Z), srdid=sdo_srid, error=error)
			else:
				point_coordinates = (sdo_point.__getattr__('X'), sdo_point.__getattr__('Y'), sdo_point.__getattr__('Z'))
				return SpatialObject(Shape(GEOMETRY_TYPE.POINT,has_Z,point_coordinates), srdid=sdo_srid, error=error)
		else:
			elements = []
			geom_distinct_types = set()
			sdo_elem_len = sdo_elem_info.size()
			elem_idx = 0
			while elem_idx < sdo_elem_len:
				# get_element returns the associated element with type and coordinates + the index of the next triplet to process in sdo_elem_info
				element,elem_idx = get_element(elem_idx)
				if element is None: # some elements can be ignored
					continue
				geom_distinct_types.add(element._type)
				elements.append(element)

			if len(elements) == 0:
				return SpatialObject(error=error)
			elif len(elements) == 1:
				return SpatialObject(elements[0], srdid=sdo_srid, error=error)
			else:
				first_type = geom_distinct_types.pop()
				# result is a collection if :
				# - source type is a collection
				# - elements doesn't have the same geometry type
				# - elements are of the same geometry type but it's a multi-type geometry
				if (sdo_geom_type == GEOMETRY_TYPE.COLLECTION) or (len(geom_distinct_types) > 0) or (first_type == GEOMETRY_TYPE.MULTI[first_type]):
					return SpatialObject(Shape(GEOMETRY_TYPE.COLLECTION,has_Z,collection=elements), srdid=sdo_srid, error=error)
				else: # several elements of same type --> build a multi-type geometry element
					return SpatialObject(Shape(GEOMETRY_TYPE.MULTI[first_type],has_Z,[element._coordinates for element in elements],[element._measures for element in elements] if has_M else [] ),
										 srdid=sdo_srid, error=error)

	except ConversionException as exception:
		return SpatialObject(error=Error(exception.error_id,exception.message))
	except Exception as exception:
		return SpatialObject(error=Error(ERROR.EXCEPTION,str(exception)))
