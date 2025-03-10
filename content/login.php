<div class="container my-5">
  <div class="row">
    <div class="col-md-6 mx-auto">
      <!-- Login Status Alert -->
      <div id="loginStatus" class="alert d-none mb-4" role="alert"></div>
      
      <div class="card bg-dark">
        <div class="card-header">
          <h2 class="text-center mb-0">Login</h2>
        </div>
        <div class="card-body">
          <p class="lead text-center mb-4">Sign in to access your account</p>
          
          <form id="loginForm">
            <div class="mb-3">
              <label for="email" class="form-label">Email address</label>
              <input type="email" class="form-control" id="email" name="email" placeholder="Enter your email" required>
            </div>
            
            <div class="mb-3">
              <label for="password" class="form-label">Password</label>
              <input type="password" class="form-control" id="password" name="password" placeholder="Enter your password" required>
            </div>
            
            <div class="mb-3 form-check">
              <input type="checkbox" class="form-check-input" id="rememberMe" name="rememberMe">
              <label class="form-check-label" for="rememberMe">Remember me</label>
            </div>
            
            <div class="d-grid gap-2">
              <button type="submit" class="btn btn-primary" id="loginButton">
                <span id="loginSpinner" class="spinner-border spinner-border-sm d-none me-2" role="status" aria-hidden="true"></span>
                Login
              </button>
            </div>
            
            <div class="mt-3 text-center">
              <a href="#" class="text-decoration-none">Forgot your password?</a>
            </div>
          </form>
        </div>
      </div>
      
      <div class="card bg-dark mt-4">
        <div class="card-body">
          <h5 class="card-title">Don't have an account?</h5>
          <p class="card-text">Register to submit articles, participate in reviews, and stay updated with the journal.</p>
          <div class="d-grid">
            <a href="register.php" class="btn btn-outline-primary">Register Now</a>
          </div>
        </div>
      </div>
      
      <!-- Demo Account Information -->
      <div class="card bg-dark border-warning mt-4">
        <div class="card-header border-warning bg-warning text-dark">
          <h5 class="mb-0"><i class="bi bi-info-circle me-2"></i>Demo Mode Enabled</h5>
        </div>
        <div class="card-body">
          <p class="mb-3">For testing purposes, you can use the following accounts:</p>
          
          <div class="table-responsive">
            <table class="table table-dark table-sm">
              <thead>
                <tr>
                  <th>Role</th>
                  <th>Email</th>
                  <th>Password</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><span class="badge bg-primary">Author</span></td>
                  <td>author@example.com</td>
                  <td>author</td>
                  <td><button class="btn btn-sm btn-outline-light autofill-btn" data-email="author@example.com" data-password="author">Use</button></td>
                </tr>
                <tr>
                  <td><span class="badge bg-info">Reviewer</span></td>
                  <td>reviewer@example.com</td>
                  <td>reviewer</td>
                  <td><button class="btn btn-sm btn-outline-light autofill-btn" data-email="reviewer@example.com" data-password="reviewer">Use</button></td>
                </tr>
                <tr>
                  <td><span class="badge bg-success">Editor</span></td>
                  <td>editor@example.com</td>
                  <td>editor</td>
                  <td><button class="btn btn-sm btn-outline-light autofill-btn" data-email="editor@example.com" data-password="editor">Use</button></td>
                </tr>
                <tr>
                  <td><span class="badge bg-danger">Admin</span></td>
                  <td>admin@example.com</td>
                  <td>admin</td>
                  <td><button class="btn btn-sm btn-outline-light autofill-btn" data-email="admin@example.com" data-password="admin">Use</button></td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div class="alert alert-warning text-dark mt-3 mb-0">
            <small><i class="bi bi-exclamation-triangle-fill me-2"></i>These accounts are for demonstration purposes only. In a production environment, you should use secure passwords.</small>
          </div>
        </div>
      </div>
      
      <!-- Account Types -->
      <div class="card bg-dark mt-4">
        <div class="card-header">
          <h5 class="mb-0">Account Types</h5>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-4">
              <div class="text-center mb-3">
                <i class="bi bi-person-circle display-6"></i>
                <h6 class="mt-2">Author</h6>
                <p class="small">Submit and track articles</p>
              </div>
            </div>
            <div class="col-md-4">
              <div class="text-center mb-3">
                <i class="bi bi-eyeglasses display-6"></i>
                <h6 class="mt-2">Reviewer</h6>
                <p class="small">Review submitted content</p>
              </div>
            </div>
            <div class="col-md-4">
              <div class="text-center">
                <i class="bi bi-briefcase display-6"></i>
                <h6 class="mt-2">Editor</h6>
                <p class="small">Manage the review process</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const loginButton = document.getElementById('loginButton');
    const loginSpinner = document.getElementById('loginSpinner');
    const loginStatus = document.getElementById('loginStatus');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    
    // Handle demo account auto-fill buttons
    const autofillButtons = document.querySelectorAll('.autofill-btn');
    autofillButtons.forEach(button => {
        button.addEventListener('click', function() {
            const email = this.getAttribute('data-email');
            const password = this.getAttribute('data-password');
            
            // Set form values
            emailInput.value = email;
            passwordInput.value = password;
            
            // Add highlight effect to show fields were updated
            emailInput.classList.add('bg-warning', 'text-dark');
            passwordInput.classList.add('bg-warning', 'text-dark');
            
            // Focus on submit button
            loginButton.focus();
            
            // Remove highlight after a short delay
            setTimeout(() => {
                emailInput.classList.remove('bg-warning', 'text-dark');
                passwordInput.classList.remove('bg-warning', 'text-dark');
            }, 1500);
            
            // Show a helpful message
            loginStatus.textContent = 'Demo account credentials filled. Click Login to continue.';
            loginStatus.classList.remove('alert-danger');
            loginStatus.classList.add('alert-info');
            loginStatus.classList.remove('d-none');
        });
    });
    
    // Handle form submission
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show loading spinner
        loginButton.disabled = true;
        loginSpinner.classList.remove('d-none');
        
        // Get form data
        const email = emailInput.value;
        const password = passwordInput.value;
        
        // Hide any previous messages
        loginStatus.classList.add('d-none');
        
        // Send login request
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Show success message
                loginStatus.textContent = data.message;
                loginStatus.classList.remove('alert-danger', 'alert-info');
                loginStatus.classList.add('alert-success');
                loginStatus.classList.remove('d-none');
                
                // Handle redirect to appropriate page based on role
                let redirectUrl = data.redirect || 'index.php';
                
                // Show redirect message
                loginStatus.textContent = `${data.message} Redirecting to your dashboard...`;
                
                // Redirect after a short delay
                setTimeout(() => {
                    window.location.href = redirectUrl;
                }, 1000);
            } else {
                // Show error message
                loginStatus.textContent = data.message;
                loginStatus.classList.remove('alert-success', 'alert-info');
                loginStatus.classList.add('alert-danger');
                loginStatus.classList.remove('d-none');
                
                // Reset button
                loginButton.disabled = false;
                loginSpinner.classList.add('d-none');
            }
        })
        .catch(error => {
            console.error('Error during login:', error);
            loginStatus.textContent = 'An error occurred during login. Please try again.';
            loginStatus.classList.remove('alert-success', 'alert-info');
            loginStatus.classList.add('alert-danger');
            loginStatus.classList.remove('d-none');
            
            // Reset button
            loginButton.disabled = false;
            loginSpinner.classList.add('d-none');
        });
    });
});
</script>