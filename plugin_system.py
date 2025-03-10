"""
Plugin System for Academic Journal Submission System

This module provides a plugin architecture to extend the functionality
of the journal system without modifying core code.
"""
import os
import sys
import importlib.util
import logging
import inspect
import json
from typing import Dict, List, Callable, Any, Optional, Union

# Set up logging
logger = logging.getLogger(__name__)

class PluginSystem:
    # Dictionary to store registered hooks and their callbacks
    hooks: Dict[str, List[Dict[str, Any]]] = {}
    
    # Dictionary to store loaded plugins
    plugins: Dict[str, Any] = {}
    
    # Dictionary to store plugin paths for template overrides
    plugin_paths: Dict[str, str] = {}
    
    @classmethod
    def register_hook(cls, hook_name: str, callback: Callable, priority: int = 10, plugin_name: str = '') -> bool:
        """
        Register a hook callback
        
        Args:
            hook_name: The name of the hook to register for
            callback: The function to call when the hook is triggered
            priority: Optional priority (lower numbers run first, default 10)
            plugin_name: Optional name of the plugin registering the hook
            
        Returns:
            bool: True if registered successfully
        """
        # Validate the hook name and callback
        if not hook_name or not callable(callback):
            logger.error(f"Plugin error: Invalid hook name or callback for '{hook_name}'")
            return False
        
        # Initialize the hook array if it doesn't exist
        if hook_name not in cls.hooks:
            cls.hooks[hook_name] = []
        
        # Add the callback to the hook
        cls.hooks[hook_name].append({
            'callback': callback,
            'priority': priority,
            'plugin': plugin_name
        })
        
        logger.debug(f"Registered hook '{hook_name}' from plugin '{plugin_name}'")
        return True
    
    @classmethod
    def execute_hook(cls, hook_name: str, args: Any = None) -> List[Any]:
        """
        Execute all callbacks registered for a hook
        
        Args:
            hook_name: The name of the hook to execute
            args: Arguments to pass to the callbacks
            
        Returns:
            List[Any]: Results from all callbacks
        """
        results = []
        
        # If no callbacks are registered for this hook, return empty results
        if hook_name not in cls.hooks or not cls.hooks[hook_name]:
            return results
        
        # Sort hooks by priority
        sorted_hooks = sorted(cls.hooks[hook_name], key=lambda h: h['priority'])
        
        # Execute callbacks in priority order
        for hook in sorted_hooks:
            try:
                callback = hook['callback']
                # Check if it's a method or function (different arg handling)
                if inspect.ismethod(callback):
                    # For methods, 'self' is already bound
                    result = callback(args)
                else:
                    # For functions
                    result = callback(args)
                
                if result is not None:
                    results.append(result)
            except Exception as e:
                logger.error(f"Plugin error in hook '{hook_name}': {str(e)}")
        
        return results
    
    @classmethod
    def load_plugins(cls) -> List[str]:
        """
        Load all plugins from the plugins directory
        
        Returns:
            List[str]: Loaded plugin names
        """
        plugins_dir = os.path.join(os.getcwd(), 'plugins')
        if not os.path.exists(plugins_dir):
            logger.info("Plugins directory does not exist. Creating it.")
            os.makedirs(plugins_dir)
            return []
        
        plugin_dirs = [d for d in os.listdir(plugins_dir) 
                    if os.path.isdir(os.path.join(plugins_dir, d)) and not d.startswith('__') 
                    and d != 'jats_plugin']
        
        loaded = []
        
        for plugin_name in plugin_dirs:
            plugin_dir = os.path.join(plugins_dir, plugin_name)
            plugin_file = os.path.join(plugin_dir, 'plugin.py')
            
            if os.path.exists(plugin_file):
                # Store the plugin path for template overrides
                cls.plugin_paths[plugin_name] = plugin_dir
                
                # Import the plugin module
                try:
                    # Add the plugin directory to sys.path temporarily
                    sys.path.insert(0, plugin_dir)
                    
                    # Import the plugin module
                    spec = importlib.util.spec_from_file_location(plugin_name, plugin_file)
                    if spec and spec.loader:
                        plugin_module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(plugin_module)
                        
                        # Call the register function if it exists
                        if hasattr(plugin_module, 'register_plugin'):
                            plugin_module.register_plugin()
                        
                        # Store the plugin module
                        cls.plugins[plugin_name] = plugin_module
                        loaded.append(plugin_name)
                        logger.info(f"Loaded plugin: {plugin_name}")
                    else:
                        logger.error(f"Failed to load plugin '{plugin_name}': Invalid module specification")
                except Exception as e:
                    logger.error(f"Failed to load plugin '{plugin_name}': {str(e)}")
                finally:
                    # Remove the plugin directory from sys.path
                    if plugin_dir in sys.path:
                        sys.path.remove(plugin_dir)
        
        return loaded
    
    @classmethod
    def is_plugin_loaded(cls, plugin_name: str) -> bool:
        """
        Check if a plugin is loaded
        
        Args:
            plugin_name: The name of the plugin to check
            
        Returns:
            bool: True if the plugin is loaded
        """
        return plugin_name in cls.plugins
    
    @classmethod
    def get_plugin_path(cls, plugin_name: str) -> Optional[str]:
        """
        Get a plugin's directory path
        
        Args:
            plugin_name: The name of the plugin
            
        Returns:
            Optional[str]: The plugin's directory path or None if not found
        """
        return cls.plugin_paths.get(plugin_name)
    
    @classmethod
    def find_template(cls, template_path: str) -> str:
        """
        Find a template file, checking plugin overrides first
        
        Args:
            template_path: Relative path to the template
            
        Returns:
            str: The path to the template file to use
        """
        # Check each plugin for an override
        for plugin_name, plugin_dir in cls.plugin_paths.items():
            override_path = os.path.join(plugin_dir, 'templates', template_path)
            if os.path.exists(override_path):
                logger.debug(f"Using template override from plugin '{plugin_name}': {override_path}")
                return override_path
        
        # No override found, use the default template
        return template_path
    
    @classmethod
    def get_plugin_info(cls) -> Dict[str, Dict[str, Any]]:
        """
        Get information about all loaded plugins
        
        Returns:
            Dict[str, Dict[str, Any]]: Plugin information
        """
        plugin_info = {}
        for plugin_name, plugin_module in cls.plugins.items():
            info = {
                'name': plugin_name,
                'path': cls.plugin_paths.get(plugin_name, ''),
                'hooks': []
            }
            
            # Get hook registrations for this plugin
            for hook_name, hooks in cls.hooks.items():
                for hook in hooks:
                    if hook['plugin'] == plugin_name:
                        info['hooks'].append(hook_name)
            
            # Get plugin metadata if available
            if hasattr(plugin_module, 'PLUGIN_INFO'):
                info.update(plugin_module.PLUGIN_INFO)
            
            plugin_info[plugin_name] = info
        
        return plugin_info

# Initialize the plugin system
def init_plugin_system():
    """Initialize the plugin system and load all plugins"""
    return PluginSystem.load_plugins()