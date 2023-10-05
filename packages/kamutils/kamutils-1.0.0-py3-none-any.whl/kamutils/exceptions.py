#-----------------------------------------------------------------------------------------
# CONSTANTS for Errors
#-----------------------------------------------------------------------------------------

# Errors IDs & default messages  ---------------------------------------------------------

class ErrrorNamespace:
	__slots__ = ()
	# SDO Geometry conversion errors
	EXCEPTION = -1
	INVALID_SDO_GEOMETRY = 1
	UNKNOW_TYPE = 2
	UNSUPPORTED_GEOMETRY = 3
	INVALID_GEOMETRY = 4
	MSG = {
		INVALID_SDO_GEOMETRY: "Error accessing SDO_GEOMETRY object property",
		UNKNOW_TYPE: "Unknown type",
		UNSUPPORTED_GEOMETRY: "Unsupported geometry",
		INVALID_GEOMETRY: "Invalid Geometry",
	}

ERROR = ErrrorNamespace()

#-----------------------------------------------------------------------------------------
# Error class
#-----------------------------------------------------------------------------------------

class Error:
	__slots__ = ('id', 'msg')

	def __init__(self, id, msg=None):
		self.id = id
		if msg == None: 
			self.msg = ERROR.MSG.get(id,"")
		else:
			self.msg = msg

	def __repr__(self):
		return f"Error {self.id} : {self.msg}"

#-----------------------------------------------------------------------------------------
# EXCEPTIONS
#-----------------------------------------------------------------------------------------

class KamException(Exception): # custom Exception with error id property
	def __init__(self, error_id, message=None):
		if message == None: message = ERROR.MSG.get(error_id,"")
		super().__init__(message)
		self.error_id = error_id
		self.message = message

class ConversionException(KamException):
    """Raised when an error occurs during conversion."""
