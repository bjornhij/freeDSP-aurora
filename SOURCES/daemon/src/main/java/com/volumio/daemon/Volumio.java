package com.volumio.daemon;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
public class Volumio {

    Logger logger = LoggerFactory.getLogger(Volumio.class);

    @Value("${volumiodaemon.volumio_url}")
    private String volumio_url;

    public void setVolume(int volume)
    {
        logger.info(volumio_url);
        String call = volumio_url + "cmd=volume&volume=" + volume;
        logger.info("Setting volume in Volumio");
        RestTemplate rest = new RestTemplate();
        String result = rest.getForObject(call, String.class);
        logger.info("Result=" + result);
    }
}
