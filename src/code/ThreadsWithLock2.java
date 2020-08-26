import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class ThreadsWithLock2 {

    public static volatile Long val = 0L;
//    public static volatile Integer id = 3;

    private static Lock lock = new ReentrantLock();

    public static void main(String[] args) throws InterruptedException {
        Thread.sleep(5000);
        int times = 1;
        while(times > 0) {
            times--;
            TestThread testThread1 = new TestThread(6);
            TestThread testThread2 = new TestThread(3);
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
            long end = System.currentTimeMillis();
            System.out.println("now tid: " + Thread.currentThread().getId() + " ::: finish time: " + end);
            lock.unlock();
        }
    }


}
