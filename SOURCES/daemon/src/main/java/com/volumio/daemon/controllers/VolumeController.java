package com.volumio.daemon.controllers;


import com.volumio.daemon.Volume;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.validation.constraints.Max;
import javax.validation.constraints.Min;
import javax.validation.constraints.Pattern;

@Controller
@Validated
public class VolumeController {

    @Autowired
    Volume volume;

    @GetMapping("/volume")
    @ResponseBody
    public int getVolume() {
        return this.volume.getVolume();
    }

    @PutMapping("/volume/{vol}")
    @ResponseBody
    void putVolume(@PathVariable(value="vol") @Pattern(regexp="up|down|\\d{1,2}") String volume)
    {
        int curvol = this.volume.getVolume();

        switch(volume)
        {
            case "up":

                if(curvol < 80)
                    this.volume.setVolume(curvol + 1);

                break;

            case "down":

                if(curvol > 0)
                    this.volume.setVolume(curvol - 1);

                break;

            default:

                this.volume.setVolume(Integer.parseInt(volume));

                break;
        }
    }
}
