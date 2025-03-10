<?php
/**
 * Plugin System for Academic Journal Submission System
 * 
 * This file defines the core Plugin class that plugins interact with
 * to register and execute hooks.
 */

class Plugin {
    /**
     * Storage for registered hooks
     * [hook_name => [[callback, priority, plugin_name], ...]]
     */
    private static $hooks = array();
    
    /**
     * Storage for loaded plugins
     * [plugin_name => plugin_info]
     */
    private static $plugins = array();
    
    /**
     * Register a hook callback
     * 
     * @param string $hook_name The name of the hook to register for
     * @param callable|string $callback The function to call when the hook is triggered
     * @param int $priority Optional priority (lower numbers run first, default 10)
     * @param string $plugin_name Optional name of the plugin registering the hook
     * @return bool True if registered successfully
     */
    public static function register_hook($hook_name, $callback, $priority = 10, $plugin_name = '') {
        if (!isset(self::$hooks[$hook_name])) {
            self::$hooks[$hook_name] = array();
        }
        
        self::$hooks[$hook_name][] = array(
            'callback' => $callback,
            'priority' => $priority,
            'plugin_name' => $plugin_name
        );
        
        // Sort by priority (lower numbers first)
        usort(self::$hooks[$hook_name], function($a, $b) {
            return $a['priority'] - $b['priority'];
        });
        
        return true;
    }
    
    /**
     * Execute all callbacks registered for a hook
     * 
     * @param string $hook_name The name of the hook to execute
     * @param mixed $args Arguments to pass to the callbacks
     * @return array Results from all callbacks
     */
    public static function execute_hook($hook_name, $args = null) {
        $results = array();
        
        if (!isset(self::$hooks[$hook_name])) {
            return $results;
        }
        
        foreach (self::$hooks[$hook_name] as $hook) {
            $callback = $hook['callback'];
            $plugin_name = $hook['plugin_name'];
            
            try {
                // Execute the callback
                if (is_callable($callback)) {
                    $result = call_user_func($callback, $args);
                    if ($result !== null) {
                        $results[] = $result;
                    }
                } else if (is_string($callback) && function_exists($callback)) {
                    $result = $callback($args);
                    if ($result !== null) {
                        $results[] = $result;
                    }
                } else {
                    error_log("Invalid callback for hook: $hook_name in plugin: $plugin_name");
                }
            } catch (Exception $e) {
                error_log("Error executing hook: $hook_name, plugin: $plugin_name, error: " . $e->getMessage());
            }
        }
        
        return $results;
    }
    
    /**
     * Load all plugins from the plugins directory
     * 
     * @return array Loaded plugin names
     */
    public static function load_plugins() {
        $loaded_plugins = array();
        $plugins_dir = 'plugins';
        
        // Ensure plugins directory exists
        if (!is_dir($plugins_dir)) {
            error_log("Plugins directory not found: $plugins_dir");
            return $loaded_plugins;
        }
        
        // Scan the plugins directory for plugin directories
        $plugin_dirs = array_filter(glob($plugins_dir . '/*'), 'is_dir');
        
        foreach ($plugin_dirs as $plugin_dir) {
            $plugin_name = basename($plugin_dir);
            $plugin_file = $plugin_dir . '/plugin.php';
            
            // Check if plugin.php exists
            if (file_exists($plugin_file)) {
                try {
                    // Load the plugin file
                    include_once $plugin_file;
                    
                    // Check if the plugin registered itself properly
                    // This is typically done by calling Plugin::register_hook in the plugin file
                    self::$plugins[$plugin_name] = array(
                        'path' => $plugin_dir,
                        'info' => isset($PLUGIN_INFO) ? $PLUGIN_INFO : array(
                            'name' => $plugin_name,
                            'version' => '1.0.0',
                            'description' => 'No description provided',
                            'author' => 'Unknown'
                        )
                    );
                    
                    $loaded_plugins[] = $plugin_name;
                    error_log("Loaded plugin: $plugin_name");
                } catch (Exception $e) {
                    error_log("Error loading plugin $plugin_name: " . $e->getMessage());
                }
            }
        }
        
        return $loaded_plugins;
    }
    
    /**
     * Check if a plugin is loaded
     * 
     * @param string $plugin_name The name of the plugin to check
     * @return bool True if the plugin is loaded
     */
    public static function is_plugin_loaded($plugin_name) {
        return isset(self::$plugins[$plugin_name]);
    }
    
    /**
     * Get a plugin's directory path
     * 
     * @param string $plugin_name The name of the plugin
     * @return string|null The plugin's directory path or null if not found
     */
    public static function get_plugin_path($plugin_name) {
        if (isset(self::$plugins[$plugin_name])) {
            return self::$plugins[$plugin_name]['path'];
        }
        return null;
    }
    
    /**
     * Find a template file, checking plugin overrides first
     * 
     * @param string $template_path Relative path to the template
     * @return string The path to the template file to use
     */
    public static function find_template($template_path) {
        // Check plugin template overrides
        foreach (self::$plugins as $plugin_name => $plugin) {
            $plugin_template = $plugin['path'] . '/templates/' . $template_path;
            if (file_exists($plugin_template)) {
                return $plugin_template;
            }
        }
        
        // No override found, return original path
        return $template_path;
    }
    
    /**
     * Get information about all loaded plugins
     * 
     * @return array Plugin information
     */
    public static function get_plugin_info() {
        return self::$plugins;
    }
}

// Initialize plugins when this file is loaded
Plugin::load_plugins();