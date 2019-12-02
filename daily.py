from datetime import date, timedelta 
import pygal;
import parsePMData;
parsePMData.readFile()

d = date.today();
todayIndicies = parsePMData.getData( str(d), parsePMData.dates );
todayHours = parsePMData.subVec( parsePMData.times, todayIndicies );
todayWatts = parsePMData.subVec( parsePMData.watts, todayIndicies );


usage = []
weekDates = []
for i in range( 6,-1,-1 ):
   d = date.today() - timedelta( days = i );
   print "date: ", str( d )
   weekDates.append( str(d) );
   if len( parsePMData.getData( str(d), parsePMData.dates ) ) > 0 :
      dateIndexes = parsePMData.getData( str( d  ), parsePMData.dates );
      if parsePMData.SHOW_COSTS :
         usage.append( parsePMData.getCost( int( dateIndexes[len(dateIndexes)-1] - dateIndexes[0] ), parsePMData.MIDPEAK ) ); 
      else :
         usage.append( int( dateIndexes[len(dateIndexes)-1] - dateIndexes[0] ) );
   else:
      usage.append( 0 );

runningTotal = 0;
for i in range( 0, len(usage ) ):
   runningTotal += usage[i];

if( parsePMData.SHOW_COSTS ):
   title = "Usage for: Last Week - Total Usage: $" + str( runningTotal);
else:
   title = "Usage for: Last Week - Total Usage: " + str( runningTotal);

chart = pygal.Bar();
chart.title = title;
chart.x_labels = weekDates;
chart.add( 'Usage', usage );
chart.render_to_file( "/cifs1/www/html/week.svg" );
