<?php
/**
 * Plugin Name: Flash
 * Plugin URI: http://example.com
 * Description: Demonstrates an extremely inefficient database query via a shortcode for educational purposes.
 * Version: 1.0
 * Author: Your Name
 * Author URI: http://example.com
 */

add_shortcode('slow_shortcode', 'extreme_expensive_operation');

function extreme_expensive_operation() {
    global $wpdb;

    // Extremely inefficient query example
    $query = "
    SELECT p1.ID, p1.post_title,
    (
        SELECT COUNT(*)
        FROM {$wpdb->posts} p2
        CROSS JOIN (SELECT post_date FROM {$wpdb->posts} WHERE post_type = 'post' AND post_status = 'publish' ORDER BY post_date DESC) p3
        WHERE p2.post_date < p1.post_date
        AND p2.post_type = 'post'
        AND p2.post_status = 'publish'
    ) AS older_posts_count
    FROM {$wpdb->posts} p1
    WHERE p1.post_type = 'post' AND p1.post_status = 'publish'
    ORDER BY older_posts_count DESC;
    ";

    $results = $wpdb->get_results($query);
    $output = "<ul>";

    foreach ($results as $post) {
        $output .= "<li>{$post->post_title} - Older Posts Count: {$post->older_posts_count}</li>";
    }

    $output .= "</ul>";

    return $output;
}
