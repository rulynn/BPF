import java.io.IOException;

public class NormalTest {
    private static Boolean flagA=true;
    private static Boolean flagB=false;
    private static Boolean flagC=false;

    public static void main(String[] args) {

        final Object lock = new Object();

        Thread aThread=new Thread(new Runnable() {

            @Override
            public void run() {
                for(int i=0;i<10;) {

                    synchronized (lock) {

                        if (flagA) {
                            //线程A执行
                            System.out.println("A");
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
                for(int i=0;i<10;) {

                    synchronized (lock) {
                        if (flagB) {
                            //线程执行
                            System.out.println("B");
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
                for(int i=0;i<10;) {

                    synchronized (lock) {

                        if (flagC) {
                            //线程执行
                            System.out.println("C");
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

            }
        });

        cThread.start();
        bThread.start();
        aThread.start();
    }
}
