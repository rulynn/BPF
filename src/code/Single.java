import java.util.Random;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class Single {

    public static class Node {
        long val;
        public Node(int val){
            this.val = val;
        }
//        private static Lock lock = new ReentrantLock();

        public synchronized void run() {
//            lock.lock();
            Random random = new Random();
            for (int i = 0; i < 1000000000; i++) {
                val += random.nextInt(100000);
            }
//            lock.unlock();
            System.out.println("val: " + val);
        }
    }


    public static void main(String[] args) throws InterruptedException {
        Thread.sleep(5000);
        long start = System.currentTimeMillis();
//        ArrayList<Integer> integers = new ArrayList<>();
//        Random random = new Random();
//        for (int i = 0; i < 25000; i++) {
//            integers.add(random.nextInt(100000));
//        }
//        for (int i = 0; i < 10000; i++) {
//            for (Integer integer : integers) {
//                integer = integer + random.nextInt(100);
//            }
//
//        }
//        synchronized(map) {
//            long val = 0;
//            Random random = new Random();
//            for (int i = 0; i < 1000000000; i++) {
//                val += random.nextInt(100000);
//            }
//            System.out.println("val: " + val);
//        }
        Node node = new Node(0);
        node.run();

        long end = System.currentTimeMillis();
        System.out.println(end - start);
    }
}
