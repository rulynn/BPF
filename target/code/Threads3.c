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
    for (int i = 0; i < 2000000000; i++) {
        val++;
    }
    mut.unlock ();
}

void thread1() {
    for (int i = 0; i < 1000000000; i++) {
        val++;
    }
    icrement ();
}

void thread2() {
    for (int i = 0; i < 1500000000; i++) {
        val++;
    }
    icrement ();
}


int main (int argc, char* argv []) {

    int times = 1;
    sleep(2);
    while(times > 0) {
        times--;
        // Two threads
        thread t1 (thread1);
        thread t2 (thread2);

        // wait
        t1.join();
        t2.join();
        cout << val << endl;
    }
    return 0;
}