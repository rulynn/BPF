import java.io.IOException;

/**
 * @Author : linouya
 * @Date : Created in 7:36 下午 2020/5/24
 */
public class Sync {


    static int NTHREADS = 5;
    //static int MAXNUM = 10000;

    public static void main(String[] args) throws IOException {
        System.out.println("Press ENTER to start.");
        System.in.read();

        if (args.length > 0) {
            NTHREADS = Integer.parseInt(args[0]);
            //MAXNUM = Integer.parseInt(args[1]);
        }

        //List<Thread> list = new ArrayList();
        for (int i = 0; i < NTHREADS; i++) {

            Thread thread = new MyThread();
            //list.add(thread);
            thread.start();
        }

        System.out.println("Press ENTER to exit.");
        System.in.read();
    }

    public static class MyThread extends Thread {

        @Override
        public void run() {
            String tmp = "";
            for (int i = 0; i < 10000000; i++) {
                tmp += "hello";
            }
        }
    }

}
