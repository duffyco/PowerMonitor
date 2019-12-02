from datetime import datetime, date, timedelta
import pygal;
import parsePMData;
parsePMData.readOtherFile( "powerlog-hourly.txt" )

endTime = datetime.now();
startTime = endTime - timedelta( hours=1 );

usage = []
title = []
for i in range( 0,60 ):
    nextTime = startTime + timedelta( minutes=i );
#    print "Time: ", str( nextTime);
    title.append( nextTime.strftime( "%M" ) ); 
    minuteIndicies = parsePMData.getData( nextTime.strftime( "%H:%M"), parsePMData.times );
    if len( minuteIndicies ) > 0 :
       minuteWatts = parsePMData.subVec( parsePMData.watts, minuteIndicies );
       if  int( minuteWatts[len(minuteWatts)-1] - minuteWatts[0] ) < 0 :
          usage.append( 0 );
       else:  
          usage.append( int( minuteWatts[len(minuteWatts)-1] - minuteWatts[0] ) ); 
    else:
       usage.append( 0 );


if parsePMData.SHOW_COSTS :
   for i in range( 0, len( usage ) ):
      if( endTime.hour < 7 or endTime.hour > 19 ):
         usage[i] = parsePMData.getCost( usage[i], parsePMData.OFFPEAK );
      elif endTime.hour > 11 and endTime.hour < 17 :
         usage[i] = parsePMData.getCost( usage[i], parsePMData.ONPEAK );
      else:
         usage[i] = parsePMData.getCost( usage[i], parsePMData.MIDPEAK );



runningTotal = 0
for i in range( 0,len(usage)):
   runningTotal += usage[i];
 
print usage;
chart = pygal.Bar( label_font_size=8 );

if( parsePMData.SHOW_COSTS ):
   chart.title = "Usage Since: " + startTime.strftime( "%H:%M" ) + " - Total Used: $" + str( runningTotal ) ;
else:
   chart.title = "Usage Since: " + startTime.strftime( "%H:%M" ) + " - Total Used: " + str( runningTotal ) ;
chart.x_labels = title;
chart.add( 'Usage', usage );
chart.render_to_file( "/cifs1/www/html/minute.svg" );
