package SpeedCodeBKD;

import SpeedCodeBKD.Utils.Processor.EmailSender;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.core.io.ClassPathResource;

import java.io.FileNotFoundException;

@Slf4j
@SpringBootApplication
public class SpeedCodeBackedApplication {

    public static String resourceFolder = new ClassPathResource("static").getPath();

    @Autowired
    public static EmailSender emailProcessor;

    public static void main(String[] args) throws FileNotFoundException {
        SpringApplication.run(SpeedCodeBackedApplication.class, args);
        log.info("================ COMPLETED LOADING SPRING-BOOT ================");
        log.info(" * Debug values:");
        log.info("   - Static resource folder: " + SpeedCodeBackedApplication.resourceFolder);
        log.info("================================================================");
    }
}
