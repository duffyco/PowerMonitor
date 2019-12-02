#import sys;
from datetime import datetime, date, timedelta
import pygal;
import parsePMData;

SECONDS = 15 

while True:

	parsePMData.readOtherFile( "powerlog-hourly.txt" )

	endTime = datetime.now();
	startTime = endTime - timedelta( seconds=SECONDS );

	usage = []

	for i in range( 0, SECONDS ):
		nextTime = startTime + timedelta( seconds=i );
#	        print "Time: ", str( nextTime);
		minuteIndicies = parsePMData.getData( nextTime.strftime( "%H:%M:%S"), parsePMData.times );
		if len( minuteIndicies ) > 0 :
		   minuteWatts = parsePMData.subVec( parsePMData.times, minuteIndicies );
		   usage.append( minuteWatts[0] );


	if parsePMData.SHOW_COSTS :
	   for i in range( 0, len( usage ) ):
		  if( endTime.hour < 7 or endTime.hour > 19 ):
			 usage[i] = parsePMData.getCost( usage[i], parsePMData.OFFPEAK );
		  elif endTime.hour > 11 and endTime.hour < 17 :
			 usage[i] = parsePMData.getCost( usage[i], parsePMData.ONPEAK );
		  else:
			 usage[i] = parsePMData.getCost( usage[i], parsePMData.MIDPEAK );

        avg = 0.0;
#        for i in range( len( usage ) -1, 1, -1 ):
        delta = datetime.strptime(usage[len(usage)-1], "%H:%M:%S.%f") - datetime.strptime(usage[0], "%H:%M:%S.%f"); 

        avg = int(delta.seconds) + ( int( delta.microseconds) / 1000000.0 ); 

        fStr = "{0:.2f} s/W - ".format( avg/len(usage) )
        fMin = "{0:.2f} W/m - ".format(60/(avg/len(usage))) 
        fKWH = "{0:.2f} W/h".format( 3600/(avg/len(usage)))
 
        print fStr,fMin,fKWH

#        sys.stdout.write(str(avg/len(usage)) + "W/s - " + str(avg/len(usage)*60) + " W/min - " + str(avg/len(usage)*3600) + "kWh \r");
#        sys.stdout.write( fStr + fMin + fKWH + "\r" );
#        sys.stdout.flush();
