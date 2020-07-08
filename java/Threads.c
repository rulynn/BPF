#include <iostream>
#include <thread>
#include <mutex>
#include <pthread.h>
using namespace std;


volatile int val;

mutex mut;


void icrement () {

    for (int i = 0; i < 100000000; i++) {
        mut.lock ();
        val++;
        mut.unlock ();
    }
}


int main (int argc, char* argv []) {

    int times = 5;
    while(times > 0) {
        times--;
        // Two threads
        thread t1 (icrement);
        thread t2 (icrement);

        // wait
        t1.join ();
        t2.join ();
        cout << val << endl;
        return 0;
    }
}