package com.volumio.daemon;

import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
public class Volumio {

    Logger logger = LoggerFactory.getLogger(Volumio.class);

    @Value("${volumiodaemon.volumio_url}")
    private String volumio_url;

    public void setInput(String input)
    {
        String call = volumio_url + "replaceAndPlay";
        logger.info("Setting input in Volumio");
        logger.info(call);

        JSONObject itemObj = new JSONObject();
        itemObj.put("service", "freedsp_aurora_control");
        itemObj.put("type", "song");
        itemObj.put("title", "Optical 1");
        itemObj.put("icon", "fa fa-plug");
        itemObj.put("uri", "aurora/" + input);

        JSONObject queueObj = new JSONObject();
        queueObj.put("item", itemObj);

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<String> request =
                new HttpEntity<String>(queueObj.toString(), headers);

        RestTemplate rest = new RestTemplate();
        String result = rest.postForObject(call, request, String.class);
        logger.info("Result=" + result);
    }

    public void setVolume(int volume)
    {
        String call = volumio_url + "commands/?cmd=volume&volume=" + volume;
        logger.info("Setting volume in Volumio");
        logger.info(call);
        RestTemplate rest = new RestTemplate();
        String result = rest.getForObject(call, String.class);
        logger.info("Result=" + result);
    }
}
