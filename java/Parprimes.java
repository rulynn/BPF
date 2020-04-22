import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

/**
 * @Author : linouya
 * @Date : Created in 11:02 下午 2020/4/22
 */
public class Parprimes {


    static int NTHREADS = 2;
    static int MAXNUM = 10000;

    static Node[] nodes;

    static class Node {
        int start = 0;
        int end = 0;
        int count = 0;
        Lock lock;
    }

    private static boolean isDivisible(int n, int d) {
        return n % d == 0;
    }

    private static boolean isSimplePrime(int n) {
        return n <= 2;
    }

    private static boolean isPrime(int n) {
        if (isSimplePrime(n)) return true;
        for (int d = 3; d < n; d += 2) {
            if (isDivisible(n, d)) return false;
        }
        return true;
    }

    private static void primesLoop(Node node) {

        for (int n = node.start; n < node.end; ++n) {
            if (isPrime(n)) {
                node.lock.lock();
                ++node.count;
                node.lock.unlock();
            }
        }

    }

    public static void main(String[] args) throws IOException, InterruptedException {
        System.out.println("Press ENTER to start.");
        System.in.read();

        if (args.length > 0) {
            NTHREADS = Integer.parseInt(args[0]);
            MAXNUM = Integer.parseInt(args[1]);
        }
        nodes = new Node[NTHREADS];

        List<Thread> list = new ArrayList();


        for (int i = 0; i < NTHREADS; i++) {

            nodes[i] = new Node();
            nodes[i].start = i * (MAXNUM / NTHREADS);
            nodes[i].end = (i + 1) * (MAXNUM / NTHREADS);
            nodes[i].count = 0;
            nodes[i].lock = new ReentrantLock();

            Thread thread = new MyThread(nodes[i]);
            list.add(thread);
            thread.start();
        }
        int count = 0;
        for (int i = 0; i < NTHREADS; i++) {
            list.get(i).join();
            System.out.println(String.format("thread %d found %d primes", i, nodes[i].count));
            count += nodes[i].count;
        }
        System.out.println(String.format("Primes found: %d", count));



        System.out.println("Press ENTER to exit.");
        System.in.read();
    }

    public static class MyThread extends Thread {

        private Node node;

        public MyThread(Node node) {
            this.node = node;
        }
        public void run() {
            primesLoop(node);
        }
    }
}
