#include "kite.hpp"

extern "C" {



  __declspec(dllexport) vect __stdcall init_vect(double theta, double phi, double r){
    return vect{theta, phi, r};
  }
  __declspec(dllexport) kite __stdcall init_kite(vect p, vect v){
    return kite{p, v};
  }
  __declspec(dllexport) bool __stdcall simulation_step(kite* k, const double step){
    bool continuation=true;
    continuation=k->update_state(step);
    return continuation;
  }

//  __declspec(dllexport) bool __stdcall simulate(kite* k, const double C_l, const double C_d, const double psi, const int integration_steps, const double step, const vect wind){
//    bool continuation=true;
//    int i=0;
//    while(continuation && i<integration_steps) {
//        continuation=k->update_state(step, wind, C_l, C_d, psi);
//        i++;
//      }
//    return continuation;
//  }
//
//  __declspec(dllexport) double __stdcall getbeta(kite* k, const vect wind){
//    return k->getbeta(wind);
//  }


  __declspec(dllexport) double __stdcall getreward(kite* k,const double psi){
    return (k->compute_power(psi));
  }

}
