package com.volumio.daemon;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.event.ContextRefreshedEvent;
import org.springframework.context.event.EventListener;


@SpringBootApplication()
public class DaemonApplication {

    @Autowired
    Volume volume;

    @Autowired
    Input input;

    @Autowired
    LircClient lircClient;

    public static void main(String[] args) {

        SpringApplication.run(DaemonApplication.class, args);
    }

    Logger logger = LoggerFactory.getLogger(Volumio.class);


    @EventListener
    public void onApplicationEvent(ContextRefreshedEvent event) {
        logger.info("Initialized");
        volume.setVolume(5);
        input.setInput("usb");
        lircClient.openConnection();
    }

}
