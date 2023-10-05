# dvf1312

## Installation

Install dependencies (requests, OSMPythonTools)

## Utilisation

in command line: 

python -m dvf1312.dvf1312 -f "31390 Carbonne" -p 31390

in code:

from dvf1312 import dvf1312

result=dvf1312("31390 Carbonne", 31390)

print(result[0]) #json bati

print(result[1]) #json non bati

If you encounter an error with postcode on a specific commune, 
you can try to rename the commune entered in input or tweak 
the code so it downloads based on lat,lon.

For fine tuning automation on downloading public data or
inquiry on developing algorithms to spatially identify 
zones where prices are below or above a treshold,
you can contact me
