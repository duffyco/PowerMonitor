from datetime import datetime, date, timedelta
import serial;
import time
import parsePMData;


current_milli_time = lambda: int(round(time.time() * 1000))

lastwrite = current_milli_time();
DELTA = 1000;

try:
  parsePMData.readFile();
  basewatts = parsePMData.watts[len(parsePMData.watts)-1];
except: 
  basewatts = 0;

ser = serial.Serial( "/dev/ttyACM0" );

rolloverTime = datetime.now() + timedelta( hours = 1);

while True:
   
   val = "";

   while True:
       val += ser.read();

       try:
          i = val.index( "," );
          val = val[0:i];
       except:
          continue;
    
       break;

   if int( val ) == 0:
     basewatts += 65535;

   if datetime.now() > rolloverTime :
      parsePMData.readFile();
      hourlyIndicies = parsePMData.getData( datetime.now().strftime( "%H:%M" ), parsePMData.times );
      if len(hourlyIndicies) > 0 :
         newDay = parsePMData.subVec( parsePMData.days, hourlyIndicies );
         newTime = parsePMData.subVec( parsePMData.times, hourlyIndicies );
         newWatts  = parsePMData.subVec( parsePMData.watts, hourlyIndicies );
         f2 = open( '/tmp/mnt/sdb1/power/powerlog-hourly.txt', 'w' );

         for j in range( 0, len( newDay ) ):
             f2.write( newDay[j] + " " + newTime[j] + " " + newWatts[j] + "\n" );

         f2.close();
      rolloverTime = datetime.now() + timedelta ( hours = 1 );
	
   if current_milli_time() - lastwrite > DELTA: 
      f = open( '/tmp/mnt/sdb1/power/powerlog.txt', 'a' );
      f2 = open( '/tmp/mnt/sdb1/power/powerlog-hourly.txt', 'a' );
      output = str( datetime.now() ) + " " + str( basewatts + int( val ) ) + "\n";
      f2.write( output );
      f.write( output );
      f.close();
      f2.close();
      lastwrite = current_milli_time();

