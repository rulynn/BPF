import java.io.IOException;
import java.util.ArrayList;
import java.util.Random;

import static java.lang.Thread.sleep;

public class SingleFun {


    public static void main(String[] args) throws IOException, InterruptedException {
        int times = 5;
        while (times > 0) {
            times--;
            long start = System.currentTimeMillis();
            runTest();
            long end = System.currentTimeMillis();
            System.out.println(end - start);
        }
    }
    
    public static void runTest(){
        ArrayList<Integer> integers = new ArrayList<>();
        Random random = new Random();
        for (int i = 0; i < 250000; i++) {
            integers.add(random.nextInt(100000) + 1);
        }
        for (int i = 0; i < 100000; i++) {
            for (int j = 0; j <integers.size() - 1; j++) {
                integers.set(j, integers.get(j) % integers.get(j + 1) + 1);
            }

        }
    }
}
