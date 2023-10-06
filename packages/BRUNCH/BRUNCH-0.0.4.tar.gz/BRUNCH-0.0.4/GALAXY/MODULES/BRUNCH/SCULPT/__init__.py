
'''
SCULPT.START ({
	"DRIVE PATH": DRIVE_PATH,
	
	"BYTES INDEXES": [ 0, 28 ],		
	"PLATE": b'',
	
	"PROGRESS": PROGRESS
})
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
		"BYTES FOR PLATE" 
	],
    "properties" : {
		"DRIVE PATH": {
			"type": "string"
		},
		
        "BYTES INDEXES" : { 
			"type" : "array",
		}
    }
}

def START (CARGO):
	validate (
		instance = CARGO, 
		schema = SCHEMA
	)

	DRIVE_PATH = CARGO ["DRIVE PATH"]
	
	BYTES_FOR_PLATE = CARGO ["BYTES FOR PLATE"]
	assert (type (BYTES_FOR_PLATE) == bytes)
	
	BYTES_PER_PLATE = len (BYTES_FOR_PLATE)
	BYTES_INDEXES = CARGO ["BYTES INDEXES"]
	
	MEAL_INDEX_START = BYTES_INDEXES [0];
	MEAL_INDEX_END = BYTES_INDEXES [1];

	with open (DRIVE_PATH, "wb") as SELECTOR:
		SELECTOR.seek (MEAL_INDEX_START)
		
		PLATE = True;
		while PLATE:
			PLATE_INDEX_START = SELECTOR.tell ()
			
			#print ("PLATE INDEX START:", PLATE_INDEX_START)
			
			#
			#	CHECK IF A FULL PLATE WOULD 
			#	PUT THE SCANNER PAST THE LAST INDEX
			#
			if (
				(PLATE_INDEX_START + BYTES_PER_PLATE) > MEAL_INDEX_END
			):
				SCULPT_SIZE = MEAL_INDEX_END - PLATE_INDEX_START + 1
				if (SCULPT_SIZE <= 0):
					return;
					
				SCULPTURE = BYTES_FOR_PLATE [0:SCULPT_SIZE]
					
			else:
				SCULPT_SIZE = BYTES_PER_PLATE
				SCULPTURE = BYTES_FOR_PLATE
					
					
			#print ("SCULPT_SIZE:", SCULPT_SIZE)
			#print ("SCULPTURE:", SCULPTURE)
			
			SELECTOR.write (SCULPTURE)