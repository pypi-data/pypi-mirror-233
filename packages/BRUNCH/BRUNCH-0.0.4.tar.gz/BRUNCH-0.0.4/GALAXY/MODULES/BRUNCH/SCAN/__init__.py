




'''
	import BRUNCH.SCAN as SCAN
'''
	
def PROGRESS (PARAMS):
	return;


#
#	https://python-jsonschema.readthedocs.io/en/latest/
#
from jsonschema import validate
SCHEMA = {
    "type" : "object",
	"required": [ 
		"DRIVE PATH",
		"BYTES INDEXES", 
		"BYTES PER PLATE" 
	],
    "properties" : {
		"DRIVE PATH": {
			"type": "string"
		},
        "BYTES INDEXES" : { 
			"type" : "array",
		},
        "BYTES PER PLATE" : {
			"type" : "number"
		}
    }
}

def START (CARGO):
	#print ("CARGO", CARGO)

	validate (
		instance = CARGO, 
		schema = SCHEMA
	)

	DRIVE_PATH = CARGO ["DRIVE PATH"]
	BYTES_PER_PLATE = CARGO ["BYTES PER PLATE"]
	BYTES_INDEXES = CARGO ["BYTES INDEXES"]
	
	#print ("VALID?")
	
	
	if ("PROGRESS" in CARGO):
		PROGRESS = CARGO ["PROGRESS"]
	
	
	#
	#	--
	#

	'''
		BYTES PER PLATE: 10
		BYTE INDEXES: [ 0, 28 ]
	
		 0 TO  9
		10 TO 19
		
		20 TO 29
	'''

	MEAL_INDEX_START = BYTES_INDEXES [0];
	MEAL_INDEX_END = BYTES_INDEXES [1];

	with open (DRIVE_PATH, "rb") as f:
		f.seek (MEAL_INDEX_START)
		#PLATE_INDEX_0 = f.tell ()
			
		PLATE = True;
		while PLATE:
			PLATE_INDEX_START = f.tell ()
						
			#
			#	CHECK IF A FULL PLATE WOULD 
			#	PUT THE SCANNER PAST THE LAST INDEX
			#
			if (
				(PLATE_INDEX_START + BYTES_PER_PLATE) > MEAL_INDEX_END
			):
				SCAN_SIZE = MEAL_INDEX_END - PLATE_INDEX_START + 1
				if (SCAN_SIZE <= 0):
					return;
				
			else:
				SCAN_SIZE = BYTES_PER_PLATE;
				
			#print ("SCAN SIZE:", SCAN_SIZE)
			
			PLATE = f.read (SCAN_SIZE)
			if (len (PLATE) == 0):
				print ("THERE WERE NO BYTES LEFT TO SCAN")
				return;	
			
			PROGRESS ({
				"PLATE": PLATE,
				"BYTES INDEXES": [
					PLATE_INDEX_START,
					PLATE_INDEX_START + SCAN_SIZE
				]
			})	
			
			
	
			 
		 
