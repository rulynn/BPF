import java.io.IOException;

/**
 * @Author : linouya
 * @Date : Created in 1:51 上午 2020/4/23
 */
public class SystemGC {

    public static final int _1MB = 1024*1024;

    public static void main(String[] args) throws IOException {

        System.out.println("Press ENTER to start.");
        System.in.read();

        for (int i = 0; i < 10000000; i++) {
            byte[] allocation = new byte[4 * _1MB];
            System.gc();
            if (i % 100 == 0) {
                System.gc();
            }
        }

        System.out.println("Press ENTER to exit.");
        System.in.read();
    }
}
