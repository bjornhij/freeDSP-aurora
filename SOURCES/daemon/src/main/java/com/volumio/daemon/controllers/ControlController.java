package com.volumio.daemon.controllers;

import com.volumio.daemon.State;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
@Validated
public class ControlController {
    @Autowired
    State state;

    @GetMapping("/")
    @ResponseBody
    public String root() {

        String html = "<body>" +
                "<head>" +
                "<script src=\"https://code.jquery.com/jquery-3.4.1.min.js\" integrity=\"sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=\" crossorigin=\"anonymous\"></script>" +
                "<h1>Hypex/volumio control</h1>" +
                "</head>" +
                "<body>" +
                "<a href=\"#\" class=\"state\" data-id=\"on\">on</a> / \n" +
                "<a href=\"#\" class=\"state\" data-id=\"off\">off</a>" +
                "<br/><br/>" +
                "<a href=\"#\" class=\"volume\" data-id=\"down\">voldown</a> /\n" +
                "<a href=\"#\" class=\"volume\" data-id=\"up\">volup</a> <br/><br>" +
                "<a href=\"#\" class=\"input\" data-id=\"usb\">usb</a><br/>\n" +
                "<a href=\"#\" class=\"input\" data-id=\"optical_1\">optical_1</a><br/>\n" +
                "<a href=\"#\" class=\"input\" data-id=\"optical_2\">optical_2</a><br/>\n" +
                "<a href=\"#\" class=\"input\" data-id=\"optical_3\">optical_3</a><br/>\n" +
                "<a href=\"#\" class=\"input\" data-id=\"optical_4\">optical_4</a><br/>\n" +
                "<a href=\"#\" class=\"input\" data-id=\"analog_1\">analog_1</a><br/>\n" +
                "<a href=\"#\" class=\"input\" data-id=\"analog_2\">analog_2</a><br/>\n" +
                "<a href=\"#\" class=\"input\" data-id=\"analog_3\">analog_3</a><br/>\n" +
                "<a href=\"#\" class=\"input\" data-id=\"analog_4\">analog_4</a><br/>" +
                "<body>" +
                "<script>\n" +
                "\n" +
                "$(\".state\").on(\"click\", function() {\n" +
                "\t\n" +
                "\tstate = $(this).data(\"id\");\n" +
                "\t$.ajax({\n" +
                "\t    url: '/state/' + state,\n" +
                "\t    type: 'PUT',\n" +
                "\t    success: function(result) {\n" +
                "\t        alert(\"AMP ON\");\n" +
                "\t    }\n" +
                "\t});\n" +
                "\t\n" +
                "});\n" +
                "\t\n" +
                "$(\".volume\").on(\"click\", function() {\n" +
                "\n" +
                "\tstate = $(this).data(\"id\");\n" +
                "\t$.ajax({\n" +
                "\t    url: '/volume/' + state,\n" +
                "\t    type: 'PUT',\n" +
                "\t    success: function(result) {\n" +
                "\t    }\n" +
                "\t});\n" +
                "\n" +
                "});" +
                "$(\".input\").on(\"click\", function() {\n" +
                "\n" +
                "\tstate = $(this).data(\"id\");\n" +
                "\t$.ajax({\n" +
                "\t    url: '/input/' + state,\n" +
                "\t    type: 'PUT',\n" +
                "\t    success: function(result) {\n" +
                "\t        alert(\"INPUT CHANGE\");\n" +
                "\t    }\n" +
                "\t});\n" +
                "\n" +
                "});" +
                "</script>" +
                "</html>";

        return html;
    }
}

/*

<a href="#" class="state" data-id="on">on</a> /
<a href="#" class="state" data-id="off">off</a>
<br/><br>
<a href="#" class="volume" data-id="up">volup</a> /
<a href="#" class="volume" data-id="down">voldown</a>
<br/><br>
<a href="#" class="input" data-id="optical_1">optical_1</a><br/>
<a href="#" class="input" data-id="optical_2">optical_2</a><br/>
<a href="#" class="input" data-id="optical_3">optical_3</a><br/>
<a href="#" class="input" data-id="optical_4">optical_4</a><br/>
<a href="#" class="input" data-id="analog_1">analog_1</a><br/>
<a href="#" class="input" data-id="analog_2">analog_2</a><br/>
<a href="#" class="input" data-id="analog_3">analog_3</a><br/>
<a href="#" class="input" data-id="analog_4">analog_4</a><br/>



<script>

$(".state").on("click", function() {

	state = $(this).data("id");
	$.ajax({
	    url: '/state/' + state,
	    type: 'PUT',
	    success: function(result) {
	        alert("AMP ON");
	    }
	});

});

$(".volume").on("click", function() {

	state = $(this).data("id");
	$.ajax({
	    url: '/volume/' + state,
	    type: 'PUT',
	    success: function(result) {
	        alert("VOL CHANGE");
	    }
	});

});

$(".input").on("click", function() {

	state = $(this).data("id");
	$.ajax({
	    url: '/input/' + state,
	    type: 'PUT',
	    success: function(result) {
	        alert("INPUT CHANGE");
	    }
	});

});

</script>

 */
