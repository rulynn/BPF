import java.io.IOException;
import java.util.ArrayList;
import java.util.Random;

public class Threads {

    public static volatile Long val = 0L;

    public static void main(String[] args) throws InterruptedException {
        int times = 2;
        while(times > 0) {
            times--;
            TestThread testThread = new TestThread();
            Thread thread1 = new Thread(testThread);
            Thread thread2 = new Thread(testThread);
            thread1.start();
            thread2.start();

            thread1.join();
            thread2.join();
            System.out.println(val);
        }
    }

    public static class TestThread implements Runnable{
        @Override
        public void run() {
            synchronized (this) {
                for (int i = 0; i < 400000000; i++) {
                    val++;
                }
            }
        }
    }
}

