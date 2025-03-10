<!-- Main Navigation -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
    <div class="container">
        <a class="navbar-brand journal-title" href="index.php">
            <i class="bi bi-journal-text me-2"></i>
            Academic Journal
        </a>
        <!-- Demo Mode Badge - will be shown/hidden via JavaScript -->
        <span id="demoModeBadge" class="badge bg-warning text-dark ms-2 d-none">
            <i class="bi bi-info-circle me-1"></i> Demo Mode
        </span>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarMain" aria-controls="navbarMain" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarMain">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                    <a class="nav-link <?php echo $activePage == 'home' ? 'active' : ''; ?>" href="index.php">
                        <i class="bi bi-house-door me-1"></i> Home
                    </a>
                </li>
                
                <!-- Author: Submit Article -->
                <li class="nav-item auth-required author-required">
                    <a class="nav-link <?php echo $activePage == 'submit' ? 'active' : ''; ?>" href="submit.php">
                        <i class="bi bi-file-earmark-plus me-1"></i> Submit Article
                    </a>
                </li>
                
                <!-- Author: My Submissions -->
                <li class="nav-item auth-required author-required">
                    <a class="nav-link <?php echo $activePage == 'my_submissions' ? 'active' : ''; ?>" href="my_submissions.php">
                        <i class="bi bi-file-earmark-text me-1"></i> My Submissions
                    </a>
                </li>
                
                <!-- Reviewer: Review Queue -->
                <li class="nav-item auth-required reviewer-required">
                    <a class="nav-link <?php echo $activePage == 'review' ? 'active' : ''; ?>" href="review.php">
                        <i class="bi bi-list-check me-1"></i> Review Queue
                    </a>
                </li>
                
                <!-- Editor/Admin: Admin Panel -->
                <li class="nav-item auth-required editor-required">
                    <a class="nav-link <?php echo $activePage == 'admin' ? 'active' : ''; ?>" href="admin.php">
                        <i class="bi bi-gear me-1"></i> Admin
                    </a>
                </li>
                
                <!-- Resources dropdown (visible to all) -->
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        <i class="bi bi-info-circle me-1"></i> Resources
                    </a>
                    <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                        <li><a class="dropdown-item" href="#">Author Guidelines</a></li>
                        <li><a class="dropdown-item" href="#">Reviewer Guidelines</a></li>
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item" href="#">Journal Policies</a></li>
                        <li><a class="dropdown-item" href="#">Ethics Statement</a></li>
                    </ul>
                </li>
            </ul>
            
            <div class="d-flex">
                <!-- Login/Register buttons (replaced by user dropdown when logged in) -->
                <div class="btn-group me-2">
                    <a href="login.php" class="btn btn-outline-light <?php echo $activePage == 'login' ? 'active' : ''; ?>">
                        <i class="bi bi-box-arrow-in-right me-1"></i> Login
                    </a>
                    <a href="register.php" class="btn btn-primary <?php echo $activePage == 'register' ? 'active' : ''; ?>">
                        <i class="bi bi-person-plus me-1"></i> Register
                    </a>
                </div>
                <form class="d-flex">
                    <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                    <button class="btn btn-outline-success" type="submit">
                        <i class="bi bi-search"></i>
                    </button>
                </form>
            </div>
        </div>
    </div>
</nav>

<script>
// This script handles the visibility of menu items based on user role
// It will be executed when the page is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get the auth status from cookies
    const hasSession = document.cookie.split(';').some((item) => item.trim().startsWith('session_token='));
    
    // Handle elements that require authentication
    const authElements = document.querySelectorAll('.auth-required');
    authElements.forEach(element => {
        element.style.display = hasSession ? '' : 'none';
    });
});
</script>
