import java.io.IOException;
import java.util.ArrayList;
import java.util.Random;

public class Single {


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
        long val = 0;
        Random random = new Random();
        for (int i = 0; i < 1000000; i++) {
            for (int j = 0; j < 1000000; j++) {
                val += random.nextInt(100000);
            }
        }
        System.out.println("val: " + val);
        long end = System.currentTimeMillis();
        System.out.println(end - start);
    }
}
