import sys;
from datetime import datetime, date, timedelta
import pygal;
import parsePMData;

SECONDS = 10

while True:

	parsePMData.readOtherFile( "powerlog-hourly.txt" )

	endTime = datetime.now();
	startTime = endTime - timedelta( seconds=10 );

	usage = []

	for i in range( 0, SECONDS ):
		nextTime = startTime + timedelta( seconds=i );
#	        print "Time: ", str( nextTime);
		minuteIndicies = parsePMData.getData( nextTime.strftime( "%H:%M:%S"), parsePMData.times );
		if len( minuteIndicies ) > 0 :
		   minuteWatts = parsePMData.subVec( parsePMData.watts, minuteIndicies );
		   usage.append( minuteWatts[0] );


	if parsePMData.SHOW_COSTS :
	   for i in range( 0, len( usage ) ):
		  if( endTime.hour < 7 or endTime.hour > 19 ):
			 usage[i] = parsePMData.getCost( usage[i], parsePMData.OFFPEAK );
		  elif endTime.hour > 11 and endTime.hour < 17 :
			 usage[i] = parsePMData.getCost( usage[i], parsePMData.ONPEAK );
		  else:
			 usage[i] = parsePMData.getCost( usage[i], parsePMData.MIDPEAK );


        totalUsage = len(usage);
        if len( usage ) > 2 :
	   totalUsage = (int)(usage[len(usage)-1] - usage[0]);

        sys.stdout.write("Estimated : " + str( totalUsage * (3600/SECONDS) ) + "kWh @ " + str( totalUsage ) + "/" + str( SECONDS ) + " sec\r");
        sys.stdout.flush();

