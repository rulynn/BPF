import java.io.IOException;
import java.math.BigDecimal;

public class BigDec {

    public static void main(String[] args) {
        long start = System.currentTimeMillis();
        for (int i = 0; i < 100000000; i++) {
            BigDecimal multiply = BigDecimal.valueOf(i).multiply(BigDecimal.valueOf(100000000 - i)).multiply(BigDecimal.valueOf((i + 100000000) / 2));
        }
        System.out.println(System.currentTimeMillis() - start);
    }
}