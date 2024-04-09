<?php
/**
 * Plugin Name: Slowy
 * Plugin URI:  https://wordpress.org/plugins/
 * Description: Just a plugin, go away.
 * Version:     1.0
 * Author:      Your Name
 * Author URI:  https://www.what-are-you-looking-at?.com
 * License:     GPLv2 or later
 */

add_action('wp_footer', 'look_at_me_I_am_a_query');

function look_at_me_I_am_a_query() {
    global $wpdb;

    // A highly resource-intensive query
    $query = "
        SELECT p1.ID, p2.post_title, 
        ABS(CHAR_LENGTH(p1.post_content) - CHAR_LENGTH(p2.post_content)) AS content_length_difference
        FROM {$wpdb->posts} p1
        CROSS JOIN {$wpdb->posts} p2
        WHERE p1.post_type = 'post' AND p2.post_type = 'post'
        AND p1.post_status = 'publish' AND p2.post_status = 'publish'
        ORDER BY content_length_difference DESC
        LIMIT 200;
    ";

    $start_time = microtime(true);
    $results = $wpdb->get_results($query);
    $end_time = microtime(true);

    $execution_time = round($end_time - $start_time, 4);
    echo "<!-- Super Intensive Query executed. Execution Time: {$execution_time} seconds -->";
}

add_action('wp_head', 'this_is_another_query');

function this_is_another_query() {
    global $wpdb;

    // A highly resource-intensive query
    $query = "
        SELECT p1.ID, p2.post_title, 
        ABS(CHAR_LENGTH(p1.post_content) - CHAR_LENGTH(p2.post_content)) AS content_length_difference
        FROM {$wpdb->posts} p1
        CROSS JOIN {$wpdb->posts} p2
        WHERE p1.post_type = 'post' AND p2.post_type = 'page'
        AND p1.post_status = 'publish' AND p2.post_status = 'publish'
        ORDER BY content_length_difference DESC;
    ";

    $start_time = microtime(true);
    $results = $wpdb->get_results($query);
    $end_time = microtime(true);

    $execution_time = round($end_time - $start_time, 4);
    echo "<!-- Super Intensive Query executed. Execution Time: {$execution_time} seconds -->";
}
