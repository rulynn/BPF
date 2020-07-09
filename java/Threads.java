import java.io.IOException;
import java.util.ArrayList;
import java.util.Random;

public class Threads {

    public static void main(String[] args) throws IOException, InterruptedException {
        int times = 5;
        while(times > 0) {
            times--;
            TestThread testThread = new TestThread();
            Thread thread1 = new Thread(testThread);
            Thread thread2 = new Thread(testThread);
            thread1.start();
            thread2.start();

            thread1.join();
            thread2.join();
        }
    }

    public static class TestThread implements Runnable{
        private Long val = 0L;

        @Override
        public void run() {
            synchronized (this) {
                for (int i = 0; i < 400000000; i++) {
                    val++;
                }
                System.out.println(val);
            }
        }
    }
}

