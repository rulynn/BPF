import java.io.IOException;
import java.util.ArrayList;
import java.util.Random;

/**
 * @Author : linouya
 * @Date : Created in 5:25 下午 2020/7/8
 */
public class Threads {

    public static void main(String[] args) throws IOException {
        TestThread testThread = new TestThread();
        Thread thread1 = new Thread(testThread);
        Thread thread2 = new Thread(testThread);
        thread1.start();
        thread2.start();
    }

    public static class TestThread implements Runnable{
        private Long val = 0L;

        @Override
        public synchronized void run() {
            for (int i = 0; i < 400000000; i++) {
                val++;
            }
            System.out.println(val);
        }
    }
}

