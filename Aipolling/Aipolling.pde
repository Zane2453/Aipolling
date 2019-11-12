import processing.net.*;
Client myClient;

int[] nums;

void setup(){
  myClient = new Client(this, "127.0.0.1", 8888);
}

void draw(){
  if (myClient.available() > 0){
    String data_buffer = myClient.readString();
    String[] data_split = splitTokens(data_buffer, ",;");
    
    if(match(data_split[0], "p") != null){
      nums = int(split(data_split[1], ' '));
      println(nums);
      //myClient.write("s");
    }
  }
}

void keyPressed() {
  if (key == '1') {
    myClient.write("s"); 
  } else if (key == '2') {
    myClient.write("n");
  } 
}
