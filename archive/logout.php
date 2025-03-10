<?php
/**
 * Logout page for the Academic Journal Submission System
 * 
 * This file serves as a logout endpoint. The cookie will be cleared by the Flask backend.
 */

// Just redirect back to the home page - the cookie clearing happens in the Flask backend
header("Location: index.php");
exit;
?>