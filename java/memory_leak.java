import java.util.Scanner;
import java.util.HashMap;
import java.util.Map;


/*
    Memory Leak: Constantly allocate objects, while using global variables, so that objects cannot be garbage collected
*/

public class Leak {

    public static Map map = new HashMap();

    public static void main(String[] args) {

        System.out.println("Press ENTER to start.");
        System.in.read();

        Scanner in = new Scanner(System.in);
        for (int i = 0; i < 100000000; i++) {
            byte[] b = new byte[10*10];
            map.put(i,b);
        }
        System.out.println(map);

        System.out.println("Press ENTER to exit.");
        System.in.read();
    }
}