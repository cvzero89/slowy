<?php
/**
 * Plugin Name: its-a-me-mario
 * Description: Fetches JSON data via a POST request and displays it.
 * Version: 1.0
 * Author: Your Name
 */

 function fetch_and_display_json() {
    $response = wp_remote_post('https://node.newnotthatgooddomain.com/api', array(
        'method'      => 'POST',
        'timeout'     => 45,
        'redirection' => 5,
        'httpversion' => '1.0',
        'blocking'    => true,
        'headers'     => array(
            'Content-Type' => 'application/json',
        ),
        'body'        => json_encode(array('hello' => 'world')),
        'cookies'     => array()
        )
    );

    if ( is_wp_error( $response ) ) {
        $error_message = $response->get_error_message();
        return "Something went wrong: $error_message";
    } else {
        $body = wp_remote_retrieve_body( $response );
        $data = json_decode( $body );
        // Check if the response includes 'image_url' and display the image
        if ( !empty($data->imageUrl) ) {
            $image_url = $data->imageUrl;
            $output = "<img src='{$image_url}' alt='Image' />";
        } else {
            $output = 'Image URL not found in the response.';
        }
        return $output;
    }
}


add_shortcode('mario', 'fetch_and_display_json');
