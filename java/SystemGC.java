import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * @Author : linouya
 * @Date : Created in 1:51 2020/4/23
 * @Design: ./trace.py 'u:/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.242.b08-0.el7_7.x86_64/jre/lib/amd64/server/libjvm.so:method__entry (STRCMP("gc", arg4)) "induced GC"' -U -p 16161
 * Problem: No output

 */
public class SystemGC {

    public static final int _1MB = 1024*1024;

    public static void main(String[] args) throws IOException {

        System.out.println("Press ENTER to start.");
        System.in.read();

        List<byte[]> list = new ArrayList<byte[]>();

        for (int i = 0; i < 10000000; i++) {
            byte[] allocation = new byte[_1MB];
            list.add(allocation);
            if (i % 100 == 0) {
                list.clear();
            }
            if (i % 2000 == 0) {
                System.gc();
            }
        }

        System.out.println("Press ENTER to exit.");
        System.in.read();
    }
}
