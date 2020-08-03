import java.io.IOException;

public class NormalTest {
    private static Boolean flagA=true;
    private static Boolean flagB=false;
    private static Boolean flagC=false;
    private static Integer count = 2000000;
    private static long start;

    public static void main(String[] args) throws IOException {

        final Object lock = new Object();

        start = System.currentTimeMillis();


        Thread aThread=new Thread(new Runnable() {

            @Override
            public void run() {
                for(int i=0;i<count;) {

                    synchronized (lock) {

                        if (flagA) {
                            //线程A执行
                            //System.out.println("A");
                            flagA=false;
                            flagB=true;
                            flagC=false;
                            lock.notifyAll();
                            i++;

                        }else {
                            try {
                                lock.wait();
                            } catch (InterruptedException e) {
                                // TODO Auto-generated catch block
                                e.printStackTrace();
                            }

                        }
                    }

                }


            }
        });



        Thread bThread=new Thread(new Runnable() {

            @Override
            public void run() {
                for(int i=0;i<count;) {

                    synchronized (lock) {
                        if (flagB) {
                            //线程执行
                            //System.out.println("B");
                            flagA=false;
                            flagB=false;
                            flagC=true;
                            lock.notifyAll();
                            i++;

                        }else {

                            try {
                                lock.wait();
                            } catch (InterruptedException e) {
                                // TODO Auto-generated catch block
                                e.printStackTrace();
                            }

                        }

                    }



                }


            }
        });


        Thread cThread=new Thread(new Runnable() {

            @Override
            public void run() {
                for(int i=0;i<count;) {

                    synchronized (lock) {

                        if (flagC) {
                            //线程执行
                            //System.out.println("C");
                            flagA=true;
                            flagB=false;
                            flagC=false;
                            lock.notifyAll();
                            i++;

                        }else {

                            try {
                                lock.wait();
                            } catch (InterruptedException e) {
                                // TODO Auto-generated catch block
                                e.printStackTrace();
                            }

                        }


                    }

                }
                System.out.println(System.currentTimeMillis() - start);
            }
        });

        System.out.println("Press ENTER to start.");
        System.in.read();

        cThread.start();
        bThread.start();
        aThread.start();
    }
}
