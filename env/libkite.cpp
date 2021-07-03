#include "kite.hpp"


extern "C" {

//    vect init_vect(double theta, double phi, double r){
//        return vect{theta, phi, r};
//    }
//    kite init_kite(vect p, vect v){
//        return kite{p, v};
//    }
    bool simulation_step(kite* k, const double step, const double action){
      bool continuation=true;
      continuation=k->update_state(step,action);
      return continuation;
    }

    double getreward(kite* k,const double step,const double action){
      return (k->compute_power(step,action));
    }

}
