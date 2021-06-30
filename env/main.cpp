#include "kite.hpp"
#include <iostream>

int main(int argc, char* argv[]){
  vect initial_position(0.0, 0.0, 0.0);
  vect initial_velocity(0.0, 0.0, 0.0);
  kite k(initial_position, initial_velocity);
  k.update_state(1.0, 0.034);
  return 0;

}

//   double wind_speed_x=atol(argv[1]);
//   vect initial_position{pi/6, 0.0, 50.0};
//k.simulate(0.0001,600000);//simulating for 10 minutes