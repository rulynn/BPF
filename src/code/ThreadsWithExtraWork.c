#include <iostream>
#include <thread>
#include <mutex>
#include <pthread.h>
#include <unistd.h>
using namespace std;


volatile long long val;
volatile int id = 1;

mutex mut;


void icrement () {

    mut.lock ();
//    for (int i = 0; i < 1000000000; i++) {
//        val++;
//    }
    cout << id << endl;
    long long len = id * 1000000000
    for (int i = 0; i < len; i++) {
        val++;
    }
    id++;
    mut.unlock ();
}

int main (int argc, char* argv []) {

    int times = 1;
    sleep(2);
    while(times > 0) {
        times--;
        // Two threads
        thread t1 (icrement);
        thread t2 (icrement);
        thread t3 (icrement);

        // wait
        t1.join();
        t2.join();
        t3.join();
        cout << val << endl;
    }
    return 0;
}