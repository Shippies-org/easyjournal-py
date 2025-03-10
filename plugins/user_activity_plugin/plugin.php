<?php
/**
 * User Activity Tracking Plugin
 * 
 * This plugin tracks user logins and displays a "last login" message.
 */

// Plugin metadata
$PLUGIN_INFO = array(
    'name' => 'User Activity Tracker',
    'version' => '1.0.0',
    'description' => 'Tracks user logins and displays last login information',
    'author' => 'Replit AI'
);

/**
 * Track user login activity
 * 
 * @param array $args Arguments passed to the hook (user_id, user_role)
 * @return null
 */
function track_user_login($args) {
    $user_id = isset($args['user_id']) ? $args['user_id'] : 0;
    $user_role = isset($args['user_role']) ? $args['user_role'] : '';
    
    if (!$user_id) {
        return null;
    }
    
    // In a real implementation, this would save to a database
    // Here we'll just log it
    error_log("User login tracked: User ID $user_id ($user_role) logged in at " . date('Y-m-d H:i:s'));
    
    // We could store this in a database table or user meta
    // For example:
    // $db = get_db_connection();
    // $stmt = $db->prepare("UPDATE users SET last_login = NOW() WHERE id = ?");
    // $stmt->bind_param("i", $user_id);
    // $stmt->execute();
    
    return null;
}

/**
 * Add last login information to user pages
 * 
 * @param array $args Arguments passed to the hook
 * @return array Modified arguments
 */
function add_login_info($args) {
    // Only add to my_submissions.php page
    $page = isset($args['page']) ? $args['page'] : '';
    if ($page !== 'my_submissions.php') {
        return $args;
    }
    
    // Get the content
    $content = isset($args['content']) ? $args['content'] : '';
    
    // Create a last login banner (in a real implementation, this would fetch the actual last login time)
    $login_info = '
    <div class="alert alert-secondary mb-4">
        <i class="fas fa-clock"></i> <strong>Your last login:</strong> ' . date('Y-m-d H:i:s', time() - 86400) . '
    </div>
    ';
    
    // Find the first container div in the content and add the login info after it
    $pattern = '/<div class="container.*?>/';
    if (preg_match($pattern, $content)) {
        $args['content'] = preg_replace($pattern, '$0' . $login_info, $content, 1);
        error_log("Added last login info to my_submissions page");
    }
    
    return $args;
}

/**
 * Register the plugin hooks when this file is loaded
 */
Plugin::register_hook('onUserLogin', 'track_user_login', 10, 'user_activity_plugin');
Plugin::register_hook('beforeContentRender', 'add_login_info', 10, 'user_activity_plugin');