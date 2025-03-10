<div class="container my-5">
  <div class="row">
    <div class="col-lg-8 mx-auto">
      <!-- Registration Status Alert -->
      <div id="registrationStatus" class="alert d-none mb-4" role="alert"></div>
      
      <div class="card bg-dark">
        <div class="card-header">
          <h2 class="text-center mb-0">Create an Account</h2>
        </div>
        <div class="card-body">
          <p class="lead text-center mb-4">Register to submit and review articles</p>
          
          <form id="registrationForm">
            <div class="mb-3">
              <label for="fullName" class="form-label">Full Name</label>
              <input type="text" class="form-control" id="fullName" name="name" placeholder="Enter your full name" required>
            </div>
            
            <div class="mb-3">
              <label for="email" class="form-label">Email address</label>
              <input type="email" class="form-control" id="email" name="email" placeholder="Enter your email" required>
              <div class="form-text">We'll never share your email with anyone else.</div>
            </div>
            
            <div class="row mb-3">
              <div class="col-md-6">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" name="password" placeholder="Create a password" required>
              </div>
              <div class="col-md-6">
                <label for="confirmPassword" class="form-label">Confirm Password</label>
                <input type="password" class="form-control" id="confirmPassword" name="confirmPassword" placeholder="Confirm your password" required>
              </div>
            </div>
            
            <div class="mb-3">
              <label for="institution" class="form-label">Institution/Organization</label>
              <input type="text" class="form-control" id="institution" name="institution" placeholder="Enter your institution or organization">
            </div>
            
            <div class="mb-3">
              <label for="role" class="form-label">Primary Role</label>
              <select class="form-select" id="role" name="role" required>
                <option value="" selected disabled>Select your primary role</option>
                <option value="author">Author - I want to submit articles</option>
                <option value="reviewer">Reviewer - I want to review submissions</option>
                <option value="editor">Editor - I want to manage the review process</option>
              </select>
            </div>
            
            <div class="mb-3">
              <label for="bio" class="form-label">Short Biography</label>
              <textarea class="form-control" id="bio" name="bio" rows="3" placeholder="Enter a short professional biography"></textarea>
            </div>
            
            <div class="mb-3 form-check">
              <input type="checkbox" class="form-check-input" id="termsCheck" name="termsCheck" required>
              <label class="form-check-label" for="termsCheck">I agree to the <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a></label>
            </div>
            
            <div class="d-grid gap-2">
              <button type="submit" class="btn btn-primary" id="registerButton">
                <span id="registerSpinner" class="spinner-border spinner-border-sm d-none me-2" role="status" aria-hidden="true"></span>
                Create Account
              </button>
            </div>
          </form>
        </div>
      </div>
      
      <div class="card bg-dark mt-4">
        <div class="card-body text-center">
          <p class="mb-0">Already have an account? <a href="login.php" class="text-decoration-none">Login here</a></p>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const registrationForm = document.getElementById('registrationForm');
    const registerButton = document.getElementById('registerButton');
    const registerSpinner = document.getElementById('registerSpinner');
    const registrationStatus = document.getElementById('registrationStatus');
    
    registrationForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate form
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        if (password !== confirmPassword) {
            registrationStatus.textContent = 'Passwords do not match';
            registrationStatus.classList.remove('alert-success');
            registrationStatus.classList.add('alert-danger');
            registrationStatus.classList.remove('d-none');
            return;
        }
        
        // Show loading spinner
        registerButton.disabled = true;
        registerSpinner.classList.remove('d-none');
        
        // Get form data
        const fullName = document.getElementById('fullName').value;
        const email = document.getElementById('email').value;
        const role = document.getElementById('role').value;
        const institution = document.getElementById('institution').value;
        const bio = document.getElementById('bio').value;
        
        // Hide any previous messages
        registrationStatus.classList.add('d-none');
        
        // Send registration request
        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: fullName,
                email: email,
                password: password,
                confirmPassword: confirmPassword,
                role: role,
                institution: institution,
                bio: bio
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Show success message
                registrationStatus.textContent = data.message;
                registrationStatus.classList.remove('alert-danger');
                registrationStatus.classList.add('alert-success');
                registrationStatus.classList.remove('d-none');
                
                // Redirect to homepage after successful registration
                setTimeout(() => {
                    window.location.href = 'index.php';
                }, 1500);
            } else {
                // Show error message
                registrationStatus.textContent = data.message;
                registrationStatus.classList.remove('alert-success');
                registrationStatus.classList.add('alert-danger');
                registrationStatus.classList.remove('d-none');
                
                // Reset button
                registerButton.disabled = false;
                registerSpinner.classList.add('d-none');
            }
        })
        .catch(error => {
            console.error('Error during registration:', error);
            registrationStatus.textContent = 'An error occurred during registration. Please try again.';
            registrationStatus.classList.remove('alert-success');
            registrationStatus.classList.add('alert-danger');
            registrationStatus.classList.remove('d-none');
            
            // Reset button
            registerButton.disabled = false;
            registerSpinner.classList.add('d-none');
        });
    });
});
</script>