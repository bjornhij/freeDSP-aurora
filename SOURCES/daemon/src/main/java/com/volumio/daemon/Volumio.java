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

    public void setInput(String input)
    {
        String call = volumio_url + "browse?url=freedsp_aurora_control/" + input;
        logger.info("Setting volume in Volumio");
        logger.info(call);
        RestTemplate rest = new RestTemplate();
        String result = rest.getForObject(call, String.class);
        logger.info("Result=" + result);
    }

    public void setVolume(int volume)
    {
        String call = volumio_url + "commands/?cmd=volume&volume=" + volume;
        logger.info("Setting input in Volumio");
        logger.info(call);
        RestTemplate rest = new RestTemplate();
        String result = rest.getForObject(call, String.class);
        logger.info("Result=" + result);
    }
}
