import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class ThreadsWithLock2 {

    public static volatile Long val = 0L;
    public static volatile Integer id = 3;

    private static Lock lock = new ReentrantLock();

    public static void main(String[] args) throws InterruptedException {
        Thread.sleep(5000);
        int times = 1;
        while(times > 0) {
            times--;
            ThreadsWithLock.TestThread testThread = new ThreadsWithLock.TestThread();
            Thread thread1 = new Thread(testThread);
            Thread thread2 = new Thread(testThread);
            thread1.start();
            thread2.start();
        }
    }

    public static class TestThread implements Runnable{
        @Override
        public void run() {
            lock.lock();
            long start = System.currentTimeMillis();
            System.out.println("now tid: " + Thread.currentThread().getId() + " ::: start time: " + start);
            for (int i = 0; i < id * 100000000; i++) {
                val++;
                if (i % 100000000 == 0) {
                    long end = System.currentTimeMillis();
                    System.out.println("now tid: " + Thread.currentThread().getId() + " ::: time: " + end);
                }
            }
            id *= 2;
            long end = System.currentTimeMillis();
            System.out.println("now tid: " + Thread.currentThread().getId() + " ::: finish time: " + end);
            lock.unlock();
        }
    }


}
