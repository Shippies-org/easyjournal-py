<?php
/**
 * Welcome Plugin
 * 
 * This plugin adds a welcome banner to the top of the home page.
 */

// Plugin metadata
$PLUGIN_INFO = array(
    'name' => 'Welcome Banner Plugin',
    'version' => '1.0.0',
    'description' => 'Adds a welcome banner to the home page',
    'author' => 'Replit AI'
);

/**
 * Modify the home page content by adding a welcome banner
 * 
 * @param array $args Arguments passed to the hook
 * @return array Modified arguments
 */
function modify_home_content($args) {
    // Get the template path and page from the arguments
    $template_path = isset($args['template_path']) ? $args['template_path'] : '';
    $page = isset($args['page']) ? $args['page'] : '';
    
    // Only modify the home page content
    if (!(strpos($template_path, 'home.php') !== false || $page === 'index.php')) {
        return $args;
    }
    
    // Get the content
    $content = isset($args['content']) ? $args['content'] : '';
    
    // Create a welcome banner
    $welcome_banner = '
    <div class="alert alert-info text-center mb-4">
        <h4 class="alert-heading">🎉 Welcome to the Academic Journal Submission System!</h4>
        <p>This plugin-enhanced message demonstrates the plugin system\'s capability to modify content.</p>
        <hr>
        <p class="mb-0">Explore our modular submission workflow designed for researchers and reviewers.</p>
    </div>
    ';
    
    // Find the first div in the content (typically the main container)
    // and add the welcome banner after it
    $pattern = '/<div class="container.*?>/';
    if (preg_match($pattern, $content)) {
        $args['content'] = preg_replace($pattern, '$0' . $welcome_banner, $content, 1);
        error_log("Welcome banner added to home page");
    }
    
    return $args;
}

/**
 * Register the plugin hooks when this file is loaded
 */
Plugin::register_hook('beforeContentRender', 'modify_home_content', 10, 'php_welcome_plugin');