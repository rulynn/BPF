package code;

import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

/**
 * @Author : linouya
 * @Date : Created in 5:19 下午 2020/8/23
 */
public class ThreadsWithLock3 {

    public static volatile Long val = 0L;

    private static Lock lock = new ReentrantLock();

    public static void main(String[] args) throws InterruptedException {
        Thread.sleep(5000);
        int times = 1;
        while(times > 0) {
            times--;
            TestThread testThread1 = new TestThread(1);
            TestThread testThread2 = new TestThread(2);

            Thread thread1 = new Thread(testThread1);
            Thread thread2 = new Thread(testThread2);
            thread1.start();
            thread2.start();
        }
    }

    public static class TestThread implements Runnable{

        public volatile Integer id;

        public TestThread(int id){
            this.id = id;
        }

        @Override
        public void run() {

            long start = System.currentTimeMillis();
            System.out.println("now tid: " + Thread.currentThread().getId() + " ::: start time: " + start);
            for (int i = 0; i < id * 100000000; i++) {
                val++;
                if (i % 100000000 == 0) {
                    long end = System.currentTimeMillis();
                    System.out.println("now tid: " + Thread.currentThread().getId() + " ::: time: " + end);
                }
            }
            long end = System.currentTimeMillis();
            System.out.println("now tid: " + Thread.currentThread().getId() + " ::: finish time: " + end);
            cal();
        }
    }

    public static void cal(){
        lock.lock();
        for (int i = 0; i < 300000000; i++) {
            val++;
            if (i % 100000000 == 0) {
                long end = System.currentTimeMillis();
                System.out.println("now tid: " + Thread.currentThread().getId() + " ::: time: " + end);
            }
        }
        lock.unlock();
    }



}
