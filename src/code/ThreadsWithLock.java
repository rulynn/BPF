import java.io.IOException;
import java.util.ArrayList;
import java.util.Random;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;


public class ThreadsWithLock {
    public static volatile Long val = 0L;

    private static Lock lock = new ReentrantLock();

    public static void main(String[] args) throws InterruptedException {
        Thread.sleep(5000);
        int times = 1;
        while(times > 0) {
            times--;
            TestThread testThread = new TestThread();
            Thread thread1 = new Thread(testThread);
            Thread thread2 = new Thread(testThread);
            //Thread thread3 = new Thread(testThread);
            thread1.start();
            thread2.start();
            //thread3.start();

//            thread1.join();
//            thread2.join();
//            System.out.println(val);
        }
    }

    public static class TestThread implements Runnable{
        @Override
        public void run() {
            //if (lock.tryLock()) {
                lock.lock();
                long start = System.currentTimeMillis();
                for (int i = 0; i < 500000000; i++) {
                    val++;
                    if (i % 100000000 == 0) {
                        long end = System.currentTimeMillis();
                        System.out.println("now tid: " + Thread.currentThread().getId() + " ::: time: " + (end - start));
                    }
                }
                System.out.println("now tid: " + Thread.currentThread().getId() + " finish");
                lock.unlock();
            //}
        }
    }

}
