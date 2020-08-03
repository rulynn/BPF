import java.io.IOException;

/**
 * @Author : linouya
 * @Date : Created in 2020/4/23
 * @Design: "./trace.py 'SyS_write (arg1==1) "%s", arg2' -U -p `pidof java`"

 * Problem:
 $ ./trace.py 'sys_write (arg1==1) "%s", arg2' -U -p 12142
 cannot attach kprobe, probe entry may not exist
 Failed to attach BPF program probe_sys_write_1 to kprobe sys_write

 $ ./tplist.py -p 12142 '*write*'
 */

public class Log {

    public static void main(String[] args) throws IOException {

        System.out.println("Press ENTER to start.");
        System.in.read();
        int len = 1000000;
        if (args.length > 0) {
            len = Integer.parseInt(args[0]);
        }
        for (int i = 0; i < len; i++) {
            MethodFirst();
            MethodSecond();
        }

        System.out.println("Press ENTER to exit.");
        System.in.read();
    }

    public static void MethodFirst() {
        try {
            int a = 10 / 0;
        } catch (Exception e) {
            System.out.println("Error: Divide By 0");
            //e.printStackTrace();
        }
    }

    public static void MethodSecond() {
        try {
            int[] a = new int[2];
            int b = a[100];
        } catch (Exception e) {
            System.out.println("Error: Out Of Bounds");
            //e.printStackTrace();
        }
    }
}