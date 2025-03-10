<div class="container my-5">
  <div class="row">
    <div class="col-lg-8 mx-auto">
      <!-- Submission Status Alert -->
      <div id="submissionStatus" class="alert d-none mb-4" role="alert"></div>
      
      <div class="card bg-dark">
        <div class="card-header">
          <h2 class="text-center mb-0">Submit Your Article</h2>
        </div>
        <div class="card-body">
          <p class="lead text-center mb-4">Please complete the form below to submit your article for review</p>
          
          <form id="submissionForm" enctype="multipart/form-data">
            <div class="mb-3">
              <label for="title" class="form-label">Article Title</label>
              <input type="text" class="form-control" id="title" name="title" placeholder="Enter the title of your article" required>
            </div>
            
            <div class="mb-3">
              <label for="authors" class="form-label">Authors</label>
              <input type="text" class="form-control" id="authors" name="authors" placeholder="Enter author names (separated by commas)" required>
            </div>
            
            <div class="mb-3">
              <label for="abstract" class="form-label">Abstract</label>
              <textarea class="form-control" id="abstract" name="abstract" rows="5" placeholder="Enter your abstract (max 300 words)" required></textarea>
              <div class="form-text text-end"><span id="abstractWordCount">0</span>/300 words</div>
            </div>
            
            <div class="mb-3">
              <label for="keywords" class="form-label">Keywords</label>
              <input type="text" class="form-control" id="keywords" name="keywords" placeholder="Enter keywords (separated by commas)">
            </div>
            
            <div class="mb-3">
              <label for="category" class="form-label">Category</label>
              <select class="form-select" id="category" name="category" required>
                <option value="" selected disabled>Select a category</option>
                <option value="Original Research">Original Research</option>
                <option value="Review Article">Review Article</option>
                <option value="Case Study">Case Study</option>
                <option value="Short Communication">Short Communication</option>
                <option value="Technical Note">Technical Note</option>
              </select>
            </div>
            
            <div class="mb-3">
              <label for="manuscriptFile" class="form-label">Manuscript File</label>
              <input class="form-control" type="file" id="manuscriptFile" name="manuscriptFile" accept=".pdf,.doc,.docx" required>
              <div class="form-text">Please upload your manuscript as a PDF, DOC, or DOCX file (max 10MB).</div>
            </div>
            
            <div class="mb-3">
              <label for="coverLetter" class="form-label">Cover Letter</label>
              <textarea class="form-control" id="coverLetter" name="coverLetter" rows="4" placeholder="Enter your cover letter"></textarea>
            </div>
            
            <div class="mb-3 form-check">
              <input type="checkbox" class="form-check-input" id="termsCheck" name="termsCheck" required>
              <label class="form-check-label" for="termsCheck">I confirm that this manuscript has not been submitted elsewhere and follows the journal's guidelines</label>
            </div>
            
            <div class="d-grid gap-2">
              <button type="submit" class="btn btn-primary" id="submitButton">
                <span id="submitSpinner" class="spinner-border spinner-border-sm d-none me-2" role="status" aria-hidden="true"></span>
                Submit Article
              </button>
            </div>
          </form>
        </div>
      </div>
      
      <div class="card bg-dark mt-4">
        <div class="card-header">
          <h3 class="mb-0">Submission Guidelines</h3>
        </div>
        <div class="card-body">
          <ul class="list-group list-group-flush bg-transparent">
            <li class="list-group-item bg-transparent">Articles must be original and not published elsewhere</li>
            <li class="list-group-item bg-transparent">Manuscripts should be formatted according to the journal's template</li>
            <li class="list-group-item bg-transparent">References should follow APA style</li>
            <li class="list-group-item bg-transparent">Maximum length: 8,000 words including references</li>
            <li class="list-group-item bg-transparent">All figures and tables must be properly labeled and referenced in the text</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const submissionForm = document.getElementById('submissionForm');
    const submitButton = document.getElementById('submitButton');
    const submitSpinner = document.getElementById('submitSpinner');
    const submissionStatus = document.getElementById('submissionStatus');
    const abstractTextarea = document.getElementById('abstract');
    const abstractWordCount = document.getElementById('abstractWordCount');
    
    // Word count for abstract
    abstractTextarea.addEventListener('input', function() {
        const text = this.value;
        const wordCount = text.trim() === '' ? 0 : text.trim().split(/\s+/).length;
        abstractWordCount.textContent = wordCount;
        
        // Visual indicator if over limit
        if (wordCount > 300) {
            abstractWordCount.classList.add('text-danger');
            abstractWordCount.classList.add('fw-bold');
        } else {
            abstractWordCount.classList.remove('text-danger');
            abstractWordCount.classList.remove('fw-bold');
        }
    });
    
    // Handle form submission
    submissionForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate abstract word count
        const abstractText = abstractTextarea.value;
        const wordCount = abstractText.trim() === '' ? 0 : abstractText.trim().split(/\s+/).length;
        
        if (wordCount > 300) {
            submissionStatus.textContent = 'Abstract exceeds the 300 word limit.';
            submissionStatus.classList.remove('alert-success');
            submissionStatus.classList.add('alert-danger');
            submissionStatus.classList.remove('d-none');
            return;
        }
        
        // Show loading spinner
        submitButton.disabled = true;
        submitSpinner.classList.remove('d-none');
        
        // Hide any previous messages
        submissionStatus.classList.add('d-none');
        
        // Create FormData object for file upload
        const formData = new FormData(submissionForm);
        
        // Send submission request
        fetch('/submit_article', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Show success message
                submissionStatus.textContent = data.message;
                submissionStatus.classList.remove('alert-danger');
                submissionStatus.classList.add('alert-success');
                submissionStatus.classList.remove('d-none');
                
                // Reset form
                submissionForm.reset();
                abstractWordCount.textContent = '0';
                
                // Redirect to My Submissions page after successful submission
                setTimeout(() => {
                    window.location.href = 'my_submissions.php';
                }, 2000);
            } else {
                // Show error message
                submissionStatus.textContent = data.message;
                submissionStatus.classList.remove('alert-success');
                submissionStatus.classList.add('alert-danger');
                submissionStatus.classList.remove('d-none');
                
                // Reset button
                submitButton.disabled = false;
                submitSpinner.classList.add('d-none');
            }
        })
        .catch(error => {
            console.error('Error during submission:', error);
            submissionStatus.textContent = 'An error occurred during submission. Please try again.';
            submissionStatus.classList.remove('alert-success');
            submissionStatus.classList.add('alert-danger');
            submissionStatus.classList.remove('d-none');
            
            // Reset button
            submitButton.disabled = false;
            submitSpinner.classList.add('d-none');
        });
    });
});
</script>