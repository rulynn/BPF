import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

/* Memory Overflow

    DESP: Constantly allocate large objects

    CPU: 99%; MEM: 1.6%
*/
public class Overflow {

    public static final int _1MB = 1024*1024;

    public static void main(String[] args) throws IOException {

        System.out.println("Press ENTER to start.");
        System.in.read();

        for (int i = 0; i < 10000000; i++) {
            byte[] allocation = new byte[4 * _1MB];
        }

        System.out.println("Press ENTER to exit.");
        System.in.read();
    }
}
