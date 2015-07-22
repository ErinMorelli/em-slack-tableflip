<?php
#
# EM SLACK TABLEFLIP
# Copyright (c) 2015 Erin Morelli
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

// Redirect to landing page
if ( $_SERVER['REQUEST_METHOD'] == 'GET' ) {
    header("Location: http://www.erinmorelli.com"); // TO DO: Make a landing page to redirect to
    die();
}
// Else, if not POST, die
else if ( $_SERVER['REQUEST_METHOD'] != 'POST' ) {
    http_response_code(405);
    die("Method Not Allowed");
}

// Check that we have a token
if ( !isset($_POST['token']) ) {
    http_response_code(401);
    die("Missing Token");
}

// Check that we have a command
if ( !isset($_POST['command']) ) {
    http_response_code(400);
    die("Bad Request");
}

// Store POST data
$token = $_POST['token'];
$command = $_POST['command'];

// Validate token
if ( $token != 'MY_SLACK_APP_TOKEN' ) { // User-set value
    http_response_code(401);
    die("Invalid Token");
}

// Validate command
if ( !preg_match('/^\/flip$/', $command) ) {
    http_response_code(400);
    die("Bad Request");
}

// Set base GET URL
$base_url = 'http://table-flip.herokuapp.com/';

// Set word flip flag
$is_word_flip = false;

// Set flip type based on input
if ( isset($_POST['text']) ) {
    $flip_type = $_POST['text'];

    // Check to see if this is a word flip
    preg_match('/^word\s(\S*)$/', $flip_type, $matches);

    if ( $matches ) {
        $is_word_flip = true;

        $flip_word = $matches[1];
        $flip_type = "flipping/$flip_word";
    }
} else {
    $flip_type = 'flipping';
}

// Set full url
$get_url = $base_url . $flip_type;

// Set User Agent
$user_agent = "EMSlackTableflip/1.0 (https://github.com/erinmorelli/em-slack-tableflip; erin@erinmorelli.com)";

// Begin cURL request
$curl_req = curl_init($get_url);

// Set cURL options
curl_setopt($curl_req, CURLOPT_USERAGENT, $user_agent);
curl_setopt($curl_req, CURLOPT_RETURNTRANSFER, true);

// Get response
$curl_res = curl_exec($curl_req);

// Check response
if ( curl_getinfo($curl_req, CURLINFO_HTTP_CODE) != 200 ) {
    if ( $is_word_flip ) {
        $reply = "Flip word '$flip_word' is not valid";
    } else {
        $reply = "Flip type '$flip_type' was not found.";
    }
}
else {
    $reply = $curl_res;
}

// Close connection
curl_close($curl_req);

// Reply
echo $reply;

?>