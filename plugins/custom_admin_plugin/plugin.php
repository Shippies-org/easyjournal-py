<?php
/**
 * Custom Admin Plugin
 * 
 * This plugin customizes the admin dashboard and provides a template override.
 */

// Plugin metadata
$PLUGIN_INFO = array(
    'name' => 'Custom Admin Interface',
    'version' => '1.0.0',
    'description' => 'Customizes the admin dashboard with an enhanced interface',
    'author' => 'Replit AI'
);

/**
 * Override the admin template
 * 
 * @param array $args Arguments passed to the hook
 * @return array|string The path to the template file or null
 */
function override_admin_template($args) {
    // Check if this is the admin page
    $page = isset($args['page']) ? $args['page'] : '';
    if ($page !== 'admin.php') {
        return null;
    }
    
    // Return the path to our custom admin template
    return __DIR__ . '/templates/content/admin.php';
}

/**
 * Add custom styles to the admin page
 * 
 * @param array $args Arguments passed to the hook
 * @return array Modified arguments
 */
function enhance_admin_page($args) {
    // Check if this is the admin page
    $page = isset($args['page']) ? $args['page'] : '';
    if ($page !== 'admin.php') {
        return $args;
    }
    
    // Get the content
    $content = isset($args['content']) ? $args['content'] : '';
    
    // Add custom JavaScript to enhance the admin experience
    $custom_script = '
    <script>
    document.addEventListener("DOMContentLoaded", function() {
        // Add a notification counter badge to the admin page
        const adminHeader = document.querySelector("h1");
        if (adminHeader) {
            adminHeader.innerHTML += " <span class=\"badge bg-danger\">3</span>";
        }
        
        // Add a last login time indicator
        const adminContainer = document.querySelector(".container");
        if (adminContainer) {
            const loginInfo = document.createElement("div");
            loginInfo.className = "alert alert-info mt-3";
            loginInfo.innerHTML = "<strong>Last login:</strong> Today at 09:45 AM";
            adminContainer.insertBefore(loginInfo, adminContainer.firstChild);
        }
    });
    </script>
    ';
    
    // Append the custom script to the content
    if (strpos($content, '</div>') !== false) {
        $args['content'] = str_replace('</div>', $custom_script . '</div>', $content);
    }
    
    return $args;
}

/**
 * Register the plugin hooks when this file is loaded
 */
Plugin::register_hook('onTemplateOverride', 'override_admin_template', 10, 'custom_admin_plugin');
Plugin::register_hook('beforeContentRender', 'enhance_admin_page', 10, 'custom_admin_plugin');