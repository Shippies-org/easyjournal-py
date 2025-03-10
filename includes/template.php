<?php
/**
 * Base template for all pages in the Academic Journal Submission System
 * 
 * This file serves as the main layout template for all pages.
 * It includes the header, navigation, content section, and footer.
 * 
 * Variables that should be set before including this template:
 * - $pageTitle: Title of the page (default: 'Academic Journal Submission System')
 * - $activePage: Current active page for navigation highlighting (e.g., 'home', 'submit', etc.)
 * - $pageContent: Path to the content file to be included
 */

// Set default values if not provided
if (!isset($pageTitle)) {
    $pageTitle = 'Academic Journal Submission System';
}

if (!isset($activePage)) {
    $activePage = '';
}

// Include header
include('includes/header.php');

// Include navigation
include('includes/navigation.php');

// Main content container with padding for fixed navbar
?>
<div class="content-wrapper pt-5 mt-4">
    <?php 
    // Include the page content
    if (isset($pageContent) && file_exists($pageContent)) {
        include($pageContent);
    } else {
        // Display error if content file doesn't exist
        echo '<div class="container my-5"><div class="alert alert-danger">Error: Content file not found.</div></div>';
    }
    ?>
</div>

<?php
// Include footer
include('includes/footer.php');
?>