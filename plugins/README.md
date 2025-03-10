# Academic Journal Plugin System

This directory contains plugins for the Academic Journal Submission System. Plugins provide a way to extend and modify the functionality of the system without changing the core code.

## Plugin Directory Structure

Each plugin should be placed in its own directory within the `plugins` directory with a structure like:

```
plugins/
  ├── my_plugin/
  │   ├── plugin.php             # Main plugin file (required)
  │   ├── templates/             # Optional template overrides
  │   │   ├── content/           
  │   │   │   └── custom_page.php
  │   │   └── ...
  │   └── assets/                # Optional plugin assets
  │       ├── css/
  │       ├── js/
  │       └── ...
  └── another_plugin/
      └── ...
```

## Creating a Plugin

1. Create a new directory for your plugin within the `plugins` directory
2. Create a `plugin.php` file in your plugin directory
3. Implement hook callbacks in your plugin.php file
4. Register your plugin's hooks using `Plugin::register_hook()`

### Example Plugin Structure

```php
<?php
/**
 * My Custom Plugin
 * 
 * This plugin adds custom functionality to the journal system.
 */

// Plugin metadata (optional but recommended)
$PLUGIN_INFO = array(
    'name' => 'My Custom Plugin',
    'version' => '1.0.0',
    'description' => 'Adds custom functionality to the journal system',
    'author' => 'Your Name'
);

/**
 * Example hook callback function
 * 
 * @param array $args Arguments passed to the hook
 * @return array Modified arguments
 */
function my_custom_hook_callback($args) {
    // Modify the arguments or perform actions
    $args['modified'] = true;
    return $args;
}

/**
 * Register the plugin hooks when this file is loaded
 */
Plugin::register_hook('hookName', 'my_custom_hook_callback', 10, 'my_plugin');
?>
```

## Available Hooks

The system provides several hooks that plugins can use to modify behavior:

| Hook Name | Description | Arguments |
|-----------|-------------|-----------|
| `beforePageProcess` | Called before processing a page | `filepath`, `user` |
| `onTemplateOverride` | Called to allow template overrides | `original_template`, `page`, `user` |
| `beforeContentRender` | Called before rendering the page content | `template_path`, `content`, `page` |
| `afterContentRender` | Called after content is rendered | `template_path`, `page` |
| `onUserLogin` | Called when a user logs in | `user_id`, `user_role` |
| `onArticleSubmit` | Called when an article is submitted | `submission_id`, `author_id` |
| `onReviewAssign` | Called when a reviewer is assigned | `submission_id`, `reviewer_id`, `editor_id` |
| `onReviewSubmit` | Called when a review is submitted | `review_id`, `reviewer_id`, `submission_id` |
| `onDecisionMade` | Called when a decision is made on a submission | `submission_id`, `decision`, `editor_id` |

## Template Overrides

Plugins can provide custom templates to replace the system's default templates. To do this:

1. Create a `templates` directory in your plugin directory
2. Create directories matching the system's structure (e.g., `templates/content/`)
3. Add your template files with the same names as the system templates
4. Register a hook for `onTemplateOverride` to specify when to use your templates

## Hook Priority

When registering a hook, you can specify a priority (default is 10). Hooks with lower priority numbers run first. This allows you to control the order in which plugin hooks are executed if multiple plugins use the same hook.

## Plugin Interaction

Plugins should try to be compatible with each other. Be careful about making assumptions about the DOM structure or global variables, as other plugins might modify them.

## Testing Plugins

You can test your plugins by activating them and checking if they perform as expected. The system logs plugin activity in the error log, which can help with debugging.