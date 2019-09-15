package com.volumio.daemon;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
public class Volumio {

    Logger logger = LoggerFactory.getLogger(Volumio.class);

    public final String volumio_url = "http://hypex-amp.local/api/v1/commands/?";

    public void setVolume(int volume)
    {
        String call = volumio_url + "cmd=volume&volume=" + volume;
        logger.info("Setting volume in Volumio");
        RestTemplate rest = new RestTemplate();
        String result = rest.getForObject(call, String.class);
        logger.info("Result=" + result);
    }
}
