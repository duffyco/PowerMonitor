from datetime import date, timedelta
import pygal;
import parsePMData;
parsePMData.readFile()

d = date.today();
todayIndicies = parsePMData.getData( str(d), parsePMData.dates );
todayHours = parsePMData.subVec( parsePMData.times, todayIndicies );
todayWatts = parsePMData.subVec( parsePMData.watts, todayIndicies );


usage = []
for i in range( 0,24 ):
   print "Time: ", i
   if len( parsePMData.getData( format( i, '02'), todayHours ) ) > 0 :
      hourWatts = parsePMData.subVec( todayWatts, parsePMData.getData( format( i, '02'), todayHours ) );
      print "Usage: ",  hourWatts[len(hourWatts)-1] 
      print "Usage2: ", hourWatts[0];
      usage.append( int( hourWatts[len(hourWatts)-1] - hourWatts[0] ) );
   else:
      usage.append( 0 );

if parsePMData.SHOW_COSTS :
   for i in range( 0, len( usage ) ):
      if( i < 7 or i > 19 ) :
         usage[i] = parsePMData.getCost( usage[i], parsePMData.OFFPEAK );
      elif i > 11 and i < 17 :
         usage[i] = parsePMData.getCost( usage[i], parsePMData.ONPEAK );
      else:
         usage[i] = parsePMData.getCost( usage[i], parsePMData.MIDPEAK );

runningTotal = 0;
for i in range( 0, len(usage ) ):
   runningTotal += usage[i];

if( parsePMData.SHOW_COSTS ):
   title = "Usage for:" + str( d ) + " - Total Usage: $" + str( runningTotal);
else:
   title = "Usage for:" + str( d ) + " - Total Usage: " + str( runningTotal);

chart = pygal.Bar();
chart.title = title;
chart.x_labels = map( str, range(0,23) );
chart.add( 'Usage', usage );
chart.render_to_file( "/cifs1/www/html/hourly.svg" );
