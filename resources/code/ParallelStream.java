import java.io.IOException;
import java.util.ArrayList;
import java.util.Random;

public class ParallelStream {


    public static void main(String[] args) throws IOException {
        long start = System.currentTimeMillis();
        ArrayList<Integer> integers = new ArrayList<>();
        Random random = new Random();
        for (int i = 0; i < 50000; i++) {
            integers.add(random.nextInt(100000));
        }

        integers.parallelStream().forEach((e) -> {
            int cnt = 0;
            for (int i = 2; i < e; i++) {
                if (e % i == 0){
                    cnt ++;
                }
            }
        });

        System.out.println(System.currentTimeMillis() - start);
    }

}
