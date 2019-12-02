import datetime

dates = [];
times = [];
watts = [];
f = None;

MIDPEAK = 0.122 + 0.05;
OFFPEAK = 0.08 + 0.05;
ONPEAK = 0.161 + 0.05;
SHOW_COSTS = False;

def getCost( watts, tier ):
   return (watts/1000.0)*tier;

def my_range(start, end, step):
    while start < end:
        yield start
        start += step

def readOtherFile(filename):
    f = open(filename, "r");
    words = f.read().split();

    for x in my_range( 0, len( words ), 3 ):
       dates.append ( words[x] );
       times.append ( words[x+1] );
       watts.append ( int( words[x+2] ) );

    f.close()

def readFile():
    f = open("powerlog.txt", "r");
    words = f.read().split();

    for x in my_range( 0, len( words ), 3 ):
       dates.append ( words[x] );
       times.append ( words[x+1] );
       watts.append ( int( words[x+2] ) );
    
    f.close()

def getData( sw, indexData ):
   data = [];
   for i in range( 0, len( indexData ) ):
      if indexData[i].startswith( sw ):
         data.append( i );
   return data;
        

def subVec( inVec, indicies ):
   outVec = []
   for i in range( 0, len( indicies ) ):
      outVec.append( inVec[indicies[i]] );
   return outVec;

def getTodayIndicies():
   td = str( datetime.date.today() );
   return getData( td, dates );
