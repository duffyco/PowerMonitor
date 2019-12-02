int analogPin = 0;     // potentiometer wiper (middle terminal) connected to analog pin 3
                       // outside leads to ground and +5V
int val = 0;           // variable to store the value read
int previousValue = 0;
boolean on = false;
boolean previousState = false;
unsigned int count = 0;

void setup()
{
  Serial.begin(9600);          //  setup serial
}

void loop()
{
  val = analogRead(analogPin); 

  on = val > 100;
 
  if( previousState != on ) {
    
     if( on )
     {
        count++;
        Serial.print( count );
        Serial.print( "," );
     }  
        
  }

  previousState = on;   
}

