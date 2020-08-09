import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * @Author : linouya
 * @Date : Created in 2:23 上午 2020/4/23
 */
public class LeakSecond {

    public static final int _1MB = 1024*1024;

    public static void main(String[] args) throws IOException {

        System.out.println("Press ENTER to start.");
        System.in.read();

        List<byte[]> list = new ArrayList<byte[]>();

        for (int i = 0; i < 10000000; i++) {
            byte[] allocation = new byte[_1MB/100];
            list.add(allocation);
        }

        System.out.println("Press ENTER to exit.");
        System.in.read();
    }

}
