<div class="container my-5">
  <div class="row">
    <div class="col-12">
      <!-- Tabbed interface for reviewer and editor views -->
      <ul class="nav nav-tabs mb-4" id="reviewTabs" role="tablist">
        <li class="nav-item" role="presentation">
          <button class="nav-link active" id="reviewer-tab" data-bs-toggle="tab" data-bs-target="#reviewer" type="button" role="tab" aria-controls="reviewer" aria-selected="true">
            <i class="bi bi-person me-2"></i>Reviewer View
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link" id="editor-tab" data-bs-toggle="tab" data-bs-target="#editor" type="button" role="tab" aria-controls="editor" aria-selected="false">
            <i class="bi bi-pencil-square me-2"></i>Editor View
          </button>
        </li>
      </ul>
      
      <!-- Tab content -->
      <div class="tab-content" id="reviewTabsContent">
        <!-- Reviewer View Tab -->
        <div class="tab-pane fade show active" id="reviewer" role="tabpanel" aria-labelledby="reviewer-tab">
          <h1 class="mb-4">Review Queue</h1>
          <p class="lead">Welcome to the review portal. As a reviewer, you can access and manage manuscripts assigned to you for review.</p>
          
          <!-- Reviews will be loaded dynamically via JavaScript -->
          <div id="reviewerAssignmentsLoading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-3 text-muted">Loading your review assignments...</p>
          </div>
          
          <div id="noAssignmentsMessage" class="alert alert-info d-none">
            <i class="bi bi-info-circle me-2"></i>
            You currently have no pending review assignments.
          </div>
          
          <div class="card bg-dark mb-4">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0">Articles Pending Review</h5>
              <span class="badge bg-primary rounded-pill">3</span>
            </div>
            <div class="card-body">
              <div class="list-group">
                <div class="list-group-item list-group-item-action bg-dark d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="mb-1">Advances in Quantum Computing Algorithms</h6>
                    <p class="mb-1 text-muted small">Submitted: Jan 15, 2023 | Due: Feb 15, 2023</p>
                  </div>
                  <a href="#" class="btn btn-sm btn-outline-primary">Review</a>
                </div>
                <div class="list-group-item list-group-item-action bg-dark d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="mb-1">Climate Change Impact on Biodiversity: A Meta-Analysis</h6>
                    <p class="mb-1 text-muted small">Submitted: Jan 22, 2023 | Due: Feb 22, 2023</p>
                  </div>
                  <a href="#" class="btn btn-sm btn-outline-primary">Review</a>
                </div>
                <div class="list-group-item list-group-item-action bg-dark d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="mb-1">Neural Network Approaches to Natural Language Processing</h6>
                    <p class="mb-1 text-muted small">Submitted: Jan 30, 2023 | Due: Mar 01, 2023</p>
                  </div>
                  <a href="#" class="btn btn-sm btn-outline-primary">Review</a>
                </div>
              </div>
            </div>
          </div>
          
          <div class="card bg-dark mb-4">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0">Completed Reviews</h5>
              <span class="badge bg-success rounded-pill">2</span>
            </div>
            <div class="card-body">
              <div class="list-group">
                <div class="list-group-item list-group-item-action bg-dark d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="mb-1">Emerging Trends in Machine Learning</h6>
                    <p class="mb-1 text-muted small">Reviewed: Jan 10, 2023 | Status: Minor Revisions</p>
                  </div>
                  <span class="badge bg-success">Completed</span>
                </div>
                <div class="list-group-item list-group-item-action bg-dark d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="mb-1">Sustainable Urban Planning: Case Studies from Europe</h6>
                    <p class="mb-1 text-muted small">Reviewed: Jan 05, 2023 | Status: Accepted</p>
                  </div>
                  <span class="badge bg-success">Completed</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="card bg-dark">
            <div class="card-header">
              <h5 class="mb-0">Reviewer Guidelines</h5>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-md-6">
                  <h6 class="mb-3">Review Criteria</h6>
                  <ul class="list-unstyled">
                    <li><i class="bi bi-check-circle me-2"></i> Originality and significance of research</li>
                    <li><i class="bi bi-check-circle me-2"></i> Soundness of methodology</li>
                    <li><i class="bi bi-check-circle me-2"></i> Quality of data analysis</li>
                    <li><i class="bi bi-check-circle me-2"></i> Clarity of presentation</li>
                    <li><i class="bi bi-check-circle me-2"></i> Relevance to field</li>
                  </ul>
                </div>
                <div class="col-md-6">
                  <h6 class="mb-3">Review Timeline</h6>
                  <ul class="list-unstyled">
                    <li><i class="bi bi-clock me-2"></i> Initial assessment: 7 days</li>
                    <li><i class="bi bi-clock me-2"></i> Comprehensive review: 21 days</li>
                    <li><i class="bi bi-clock me-2"></i> Revision review: 14 days</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Editor View Tab -->
        <div class="tab-pane fade" id="editor" role="tabpanel" aria-labelledby="editor-tab">
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h1 class="mb-0">Editorial Dashboard</h1>
            <div>
              <button class="btn btn-outline-secondary me-2">
                <i class="bi bi-funnel me-1"></i> Filter
              </button>
              <button class="btn btn-primary">
                <i class="bi bi-plus me-1"></i> New Issue
              </button>
            </div>
          </div>
          
          <p class="lead">Manage manuscript submissions, assign reviewers, and make publication decisions.</p>
          
          <div class="row mb-4">
            <div class="col-md-3 mb-3">
              <div class="card bg-dark text-center h-100">
                <div class="card-body">
                  <h3 class="display-4">12</h3>
                  <h6 class="text-muted">New Submissions</h6>
                </div>
                <div class="card-footer p-2">
                  <button class="btn btn-sm btn-outline-primary w-100">View All</button>
                </div>
              </div>
            </div>
            <div class="col-md-3 mb-3">
              <div class="card bg-dark text-center h-100">
                <div class="card-body">
                  <h3 class="display-4">8</h3>
                  <h6 class="text-muted">Awaiting Assignment</h6>
                </div>
                <div class="card-footer p-2">
                  <button class="btn btn-sm btn-outline-primary w-100">Assign Reviewers</button>
                </div>
              </div>
            </div>
            <div class="col-md-3 mb-3">
              <div class="card bg-dark text-center h-100">
                <div class="card-body">
                  <h3 class="display-4">15</h3>
                  <h6 class="text-muted">In Review</h6>
                </div>
                <div class="card-footer p-2">
                  <button class="btn btn-sm btn-outline-primary w-100">Check Status</button>
                </div>
              </div>
            </div>
            <div class="col-md-3 mb-3">
              <div class="card bg-dark text-center h-100">
                <div class="card-body">
                  <h3 class="display-4">5</h3>
                  <h6 class="text-muted">Decision Needed</h6>
                </div>
                <div class="card-footer p-2">
                  <button class="btn btn-sm btn-outline-primary w-100">Make Decisions</button>
                </div>
              </div>
            </div>
          </div>
          
          <div class="card bg-dark mb-4">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0">Recent Submissions</h5>
              <div>
                <select class="form-select form-select-sm" style="width: auto; display: inline-block;">
                  <option>All Categories</option>
                  <option>Original Research</option>
                  <option>Review Article</option>
                  <option>Case Study</option>
                </select>
              </div>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-dark">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Title</th>
                      <th>Author</th>
                      <th>Submitted</th>
                      <th>Category</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>SUB-2023-001</td>
                      <td>Advanced Machine Learning in Healthcare Diagnostics</td>
                      <td>John Smith et al.</td>
                      <td>Feb 05, 2023</td>
                      <td>Original Research</td>
                      <td><span class="badge bg-warning">Pending Review</span></td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <button class="btn btn-outline-primary">View</button>
                          <button class="btn btn-outline-success">Assign</button>
                          <button class="btn btn-outline-danger">Reject</button>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td>SUB-2023-002</td>
                      <td>Climate Change Effects on Marine Ecosystems</td>
                      <td>Maria Chen et al.</td>
                      <td>Feb 03, 2023</td>
                      <td>Review Article</td>
                      <td><span class="badge bg-primary">Under Review</span></td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <button class="btn btn-outline-primary">View</button>
                          <button class="btn btn-outline-info">Progress</button>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td>SUB-2023-003</td>
                      <td>Sustainable Energy: A Comprehensive Review</td>
                      <td>Alex Johnson</td>
                      <td>Feb 01, 2023</td>
                      <td>Review Article</td>
                      <td><span class="badge bg-info">Review Complete</span></td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <button class="btn btn-outline-primary">View</button>
                          <button class="btn btn-outline-success">Accept</button>
                          <button class="btn btn-outline-warning">Revise</button>
                          <button class="btn btn-outline-danger">Reject</button>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td>SUB-2023-004</td>
                      <td>Novel Approaches to Quantum Computing</td>
                      <td>Sarah Williams</td>
                      <td>Jan 28, 2023</td>
                      <td>Original Research</td>
                      <td><span class="badge bg-success">Accepted</span></td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <button class="btn btn-outline-primary">View</button>
                          <button class="btn btn-outline-secondary">Publish</button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="card-footer text-end">
              <button class="btn btn-sm btn-outline-primary">View All Submissions</button>
            </div>
          </div>
          
          <div class="card bg-dark mb-4">
            <div class="card-header">
              <h5 class="mb-0">Assign Reviewers</h5>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <label for="submissionSelect" class="form-label">Select Submission</label>
                <select class="form-select" id="submissionSelect">
                  <option selected disabled>Choose a submission to assign reviewers</option>
                  <option>SUB-2023-001: Advanced Machine Learning in Healthcare Diagnostics</option>
                  <option>SUB-2023-005: Neuroplasticity and Learning Outcomes</option>
                  <option>SUB-2023-008: Microplastics in Urban Water Systems</option>
                </select>
              </div>
              
              <div class="mb-3">
                <label class="form-label">Available Reviewers</label>
                <div class="table-responsive">
                  <table class="table table-dark">
                    <thead>
                      <tr>
                        <th>Name</th>
                        <th>Expertise</th>
                        <th>Current Workload</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>Dr. Emily Johnson</td>
                        <td>Machine Learning, Healthcare AI</td>
                        <td>1 active review</td>
                        <td><button class="btn btn-sm btn-outline-primary">Assign</button></td>
                      </tr>
                      <tr>
                        <td>Prof. Michael Davis</td>
                        <td>Healthcare Informatics, Data Science</td>
                        <td>0 active reviews</td>
                        <td><button class="btn btn-sm btn-outline-primary">Assign</button></td>
                      </tr>
                      <tr>
                        <td>Dr. Robert Chen</td>
                        <td>Artificial Intelligence, Neural Networks</td>
                        <td>2 active reviews</td>
                        <td><button class="btn btn-sm btn-outline-primary">Assign</button></td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Review Modal -->
<div class="modal fade" id="reviewModal" tabindex="-1" aria-labelledby="reviewModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered modal-lg">
    <div class="modal-content bg-dark text-light">
      <div class="modal-header">
        <h5 class="modal-title" id="reviewModalLabel">Submit Review</h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <div id="reviewModalLoading" class="d-flex justify-content-center align-items-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
        
        <div id="reviewModalContent" class="d-none">
          <h6 class="mb-3">Reviewing: <span id="submissionTitle">Title loading...</span></h6>
          
          <div class="row mb-3">
            <div class="col-md-6">
              <div class="card bg-secondary mb-3">
                <div class="card-header">Submission Details</div>
                <div class="card-body">
                  <p class="card-text mb-1"><strong>Authors:</strong> <span id="submissionAuthors"></span></p>
                  <p class="card-text mb-1"><strong>Category:</strong> <span id="submissionCategory"></span></p>
                  <p class="card-text mb-1"><strong>Keywords:</strong> <span id="submissionKeywords"></span></p>
                  <p class="card-text mb-1"><strong>Submitted:</strong> <span id="submissionDate"></span></p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card bg-secondary mb-3">
                <div class="card-header">Review Information</div>
                <div class="card-body">
                  <p class="card-text mb-1"><strong>Due Date:</strong> <span id="reviewDueDate"></span></p>
                  <p class="card-text mb-1"><strong>Review ID:</strong> <span id="reviewId"></span></p>
                  <p class="card-text mb-1"><strong>Status:</strong> <span id="reviewStatus" class="badge bg-warning">Pending</span></p>
                </div>
              </div>
            </div>
          </div>
          
          <div class="row mb-3">
            <div class="col">
              <div class="card bg-secondary">
                <div class="card-header">Abstract</div>
                <div class="card-body">
                  <p class="card-text" id="submissionAbstract"></p>
                </div>
              </div>
            </div>
          </div>
          
          <hr class="my-4">
          
          <form id="reviewForm">
            <input type="hidden" id="currentReviewId" name="review_id">
            
            <div class="mb-3">
              <label for="reviewContent" class="form-label">Review Comments</label>
              <textarea class="form-control bg-dark text-light" id="reviewContent" rows="8" placeholder="Enter your detailed review comments here. Consider the paper's contribution, methodology, writing quality, and significance to the field." required></textarea>
            </div>
            
            <div class="mb-3">
              <label class="form-label">Recommendation</label>
              <div class="bg-secondary p-3 rounded">
                <div class="form-check mb-2">
                  <input class="form-check-input" type="radio" name="reviewDecision" id="decisionAccept" value="accept" required>
                  <label class="form-check-label" for="decisionAccept">
                    <strong class="text-success">Accept</strong> - The paper is ready for publication with minor or no revisions
                  </label>
                </div>
                <div class="form-check mb-2">
                  <input class="form-check-input" type="radio" name="reviewDecision" id="decisionMinorRevisions" value="minor_revisions">
                  <label class="form-check-label" for="decisionMinorRevisions">
                    <strong class="text-primary">Minor Revisions</strong> - The paper requires small changes before acceptance
                  </label>
                </div>
                <div class="form-check mb-2">
                  <input class="form-check-input" type="radio" name="reviewDecision" id="decisionMajorRevisions" value="major_revisions">
                  <label class="form-check-label" for="decisionMajorRevisions">
                    <strong class="text-warning">Major Revisions</strong> - The paper requires significant changes before reconsideration
                  </label>
                </div>
                <div class="form-check">
                  <input class="form-check-input" type="radio" name="reviewDecision" id="decisionReject" value="reject">
                  <label class="form-check-label" for="decisionReject">
                    <strong class="text-danger">Reject</strong> - The paper is not suitable for publication in this journal
                  </label>
                </div>
              </div>
            </div>
            
            <div class="mb-3">
              <label class="form-label">Confidential Comments to Editor (optional)</label>
              <textarea class="form-control bg-dark text-light" id="confidentialComments" rows="3" placeholder="These comments will only be visible to the editor, not the authors."></textarea>
            </div>
            
            <div class="alert alert-info">
              <i class="bi bi-info-circle-fill me-2"></i> Your review will be visible to the editor immediately, but authors will only see it after the editor makes a final decision.
            </div>
          </form>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary" id="submitReviewBtn">Submit Review</button>
      </div>
    </div>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  // Constants for tab handling
  const reviewerTab = document.getElementById('reviewer-tab');
  const editorTab = document.getElementById('editor-tab');
  const reviewerPanel = document.getElementById('reviewer');
  const editorPanel = document.getElementById('editor');
  
  // Elements for the reviewer view
  const reviewerAssignmentsLoading = document.getElementById('reviewerAssignmentsLoading');
  const noAssignmentsMessage = document.getElementById('noAssignmentsMessage');
  
  // Using standard DOM methods instead of :contains()
  const pendingReviewsCard = Array.from(document.querySelectorAll('.card-header')).find(
    header => header.textContent.includes('Articles Pending Review')
  )?.closest('.card');
  const pendingReviewsList = pendingReviewsCard?.querySelector('.list-group');
  
  const completedReviewsCard = Array.from(document.querySelectorAll('.card-header')).find(
    header => header.textContent.includes('Completed Reviews')
  )?.closest('.card');
  const completedReviewsList = completedReviewsCard?.querySelector('.list-group');
  
  // Elements for the editor view
  const submissionSelect = document.getElementById('submissionSelect');
  const submissionsTable = document.querySelector('.table-dark');
  const submissionsTableBody = submissionsTable.querySelector('tbody');
  
  // Show appropriate tab based on user role
  function setupTabs() {
    // This will be dynamic based on user role once we have the proper backend
    const userRole = getUserRole();
    
    if (userRole === 'reviewer') {
      reviewerTab.click(); // Show reviewer tab by default
      editorTab.classList.add('d-none'); // Hide editor tab
    } else if (userRole === 'editor' || userRole === 'admin') {
      editorTab.click(); // Show editor tab by default
    }
  }
  
  // Placeholder function to get user role - replace with actual implementation
  function getUserRole() {
    // In the real implementation, this would be fetched from the server
    // For now, return a placeholder role
    return 'editor'; // Default to reviewer for testing
  }
  
  // Function to load reviewer assignments
  function loadReviewerAssignments() {
    reviewerAssignmentsLoading.classList.remove('d-none');
    
    fetch('/get_submissions')
      .then(response => response.json())
      .then(data => {
        reviewerAssignmentsLoading.classList.add('d-none');
        
        if (data.success) {
          if (data.submissions && data.submissions.length > 0) {
            displayReviewerAssignments(data.submissions);
          } else {
            noAssignmentsMessage.classList.remove('d-none');
            // Hide the pending reviews section
            pendingReviewsCard.classList.add('d-none');
          }
        } else {
          showAlert('danger', 'Error loading assignments: ' + data.message);
        }
      })
      .catch(error => {
        reviewerAssignmentsLoading.classList.add('d-none');
        console.error('Error loading reviewer assignments:', error);
        showAlert('danger', 'Failed to load assignments. Please try again later.');
      });
  }
  
  // Function to display reviewer assignments
  function displayReviewerAssignments(submissions) {
    // Clear existing assignments
    pendingReviewsList.innerHTML = '';
    
    // Add each pending assignment
    const pendingAssignments = submissions.filter(sub => sub.status === 'in_review');
    
    if (pendingAssignments.length > 0) {
      // Update the badge count
      const pendingBadge = pendingReviewsCard.querySelector('.badge');
      pendingBadge.textContent = pendingAssignments.length;
      
      pendingAssignments.forEach(assignment => {
        const submissionDate = new Date(assignment.created_at);
        const dueDate = new Date(submissionDate);
        dueDate.setDate(dueDate.getDate() + 21); // Assume 21 days for review
        
        const assignmentItem = document.createElement('div');
        assignmentItem.className = 'list-group-item list-group-item-action bg-dark d-flex justify-content-between align-items-center';
        assignmentItem.innerHTML = `
          <div>
            <h6 class="mb-1">${assignment.title}</h6>
            <p class="mb-1 text-muted small">
              Submitted: ${submissionDate.toLocaleDateString()} | 
              Due: ${dueDate.toLocaleDateString()}
            </p>
          </div>
          <button class="btn btn-sm btn-outline-primary review-btn" 
                 data-submission-id="${assignment.id}">Review</button>
        `;
        
        pendingReviewsList.appendChild(assignmentItem);
      });
      
      // Add event listeners to the review buttons
      const reviewButtons = pendingReviewsList.querySelectorAll('.review-btn');
      reviewButtons.forEach(button => {
        button.addEventListener('click', function() {
          const submissionId = this.getAttribute('data-submission-id');
          openReviewForm(submissionId);
        });
      });
    } else {
      pendingReviewsCard.classList.add('d-none');
    }
    
    // TODO: Also update the completed reviews section
  }
  
  // Function to open the review form for a submission
  function openReviewForm(submissionId) {
    // Show the modal
    const reviewModal = new bootstrap.Modal(document.getElementById('reviewModal'));
    reviewModal.show();
    
    // Show loading indicator
    document.getElementById('reviewModalLoading').classList.remove('d-none');
    document.getElementById('reviewModalContent').classList.add('d-none');
    
    // Fetch the submission details
    fetch(`/get_submissions?id=${submissionId}`)
      .then(response => response.json())
      .then(data => {
        if (data.success && data.submissions && data.submissions.length > 0) {
          const submission = data.submissions[0];
          
          // Fill in the submission details
          document.getElementById('submissionTitle').textContent = submission.title;
          document.getElementById('submissionAuthors').textContent = submission.authors || submission.author_name || 'Unknown';
          document.getElementById('submissionCategory').textContent = submission.category || 'Not specified';
          document.getElementById('submissionKeywords').textContent = submission.keywords || 'None';
          document.getElementById('submissionAbstract').textContent = submission.abstract || 'No abstract provided';
          
          const submissionDate = new Date(submission.created_at);
          document.getElementById('submissionDate').textContent = submissionDate.toLocaleDateString();
          
          // Calculate and set the due date (21 days from submission)
          const dueDate = new Date(submissionDate);
          dueDate.setDate(dueDate.getDate() + 21);
          document.getElementById('reviewDueDate').textContent = dueDate.toLocaleDateString();
          
          // Set the review ID - in a real implementation, this would be the actual review assignment ID
          const reviewId = `R-${submission.id}-${Date.now()}`;
          document.getElementById('reviewId').textContent = reviewId;
          document.getElementById('currentReviewId').value = reviewId;
          
          // Hide loading, show content
          document.getElementById('reviewModalLoading').classList.add('d-none');
          document.getElementById('reviewModalContent').classList.remove('d-none');
          
          // Set up the submit button event handler
          document.getElementById('submitReviewBtn').onclick = function() {
            submitReview(submission.id);
          };
        } else {
          showAlert('danger', 'Error loading submission details: ' + (data.message || 'Unknown error'));
          reviewModal.hide();
        }
      })
      .catch(error => {
        console.error('Error loading submission details:', error);
        showAlert('danger', 'Failed to load submission details. Please try again later.');
        reviewModal.hide();
      });
  }
  
  // Function to submit a review
  function submitReview(submissionId) {
    const reviewContent = document.getElementById('reviewContent').value.trim();
    const decision = document.querySelector('input[name="reviewDecision"]:checked')?.value;
    const confidentialComments = document.getElementById('confidentialComments').value.trim();
    const reviewId = document.getElementById('currentReviewId').value;
    
    // Validate form
    if (!reviewContent) {
      showAlert('danger', 'Please provide your review comments.');
      return;
    }
    
    if (!decision) {
      showAlert('danger', 'Please select a recommendation.');
      return;
    }
    
    // Show loading state on button
    const submitBtn = document.getElementById('submitReviewBtn');
    const originalBtnText = submitBtn.textContent;
    submitBtn.textContent = 'Submitting...';
    submitBtn.disabled = true;
    
    // Submit the review
    fetch('/submit_review', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        review_id: reviewId,
        content: reviewContent,
        decision: decision,
        confidential_comments: confidentialComments,
        submission_id: submissionId
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Close the modal
        const reviewModal = bootstrap.Modal.getInstance(document.getElementById('reviewModal'));
        reviewModal.hide();
        
        // Show success message
        showAlert('success', 'Review submitted successfully. Thank you for your contribution!');
        
        // Refresh the assignments list
        loadReviewerAssignments();
      } else {
        showAlert('danger', 'Error submitting review: ' + (data.message || 'Unknown error'));
        
        // Reset button
        submitBtn.textContent = originalBtnText;
        submitBtn.disabled = false;
      }
    })
    .catch(error => {
      console.error('Error submitting review:', error);
      showAlert('danger', 'Failed to submit review. Please try again later.');
      
      // Reset button
      submitBtn.textContent = originalBtnText;
      submitBtn.disabled = false;
    });
  }
  
  // Function to load editor dashboard data
  function loadEditorDashboard() {
    // Fetch all submissions
    fetch('/get_submissions')
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          if (data.submissions && data.submissions.length > 0) {
            displayEditorSubmissions(data.submissions);
          }
        } else {
          showAlert('danger', 'Error loading submissions: ' + data.message);
        }
      })
      .catch(error => {
        console.error('Error loading editor dashboard:', error);
        showAlert('danger', 'Failed to load submissions. Please try again later.');
      });
    
    // Fetch reviewers list
    fetch('/get_reviewers')
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          if (data.reviewers && data.reviewers.length > 0) {
            displayReviewers(data.reviewers);
          }
        } else {
          showAlert('danger', 'Error loading reviewers: ' + data.message);
        }
      })
      .catch(error => {
        console.error('Error loading reviewers:', error);
      });
  }
  
  // Function to display editor submissions
  function displayEditorSubmissions(submissions) {
    submissionsTableBody.innerHTML = '';
    
    // Add submissions to the table
    submissions.forEach(submission => {
      const submissionDate = new Date(submission.created_at);
      
      // Determine status badge class
      let statusBadgeClass = 'bg-secondary';
      let statusText = submission.status;
      
      if (submission.status === 'pending') {
        statusBadgeClass = 'bg-warning';
        statusText = 'Pending Review';
      } else if (submission.status === 'in_review') {
        statusBadgeClass = 'bg-primary';
        statusText = 'Under Review';
      } else if (submission.status === 'reviewed') {
        statusBadgeClass = 'bg-info';
        statusText = 'Review Complete';
      } else if (submission.status === 'accepted') {
        statusBadgeClass = 'bg-success';
        statusText = 'Accepted';
      } else if (submission.status === 'rejected') {
        statusBadgeClass = 'bg-danger';
        statusText = 'Rejected';
      } else if (submission.status === 'revisions_requested') {
        statusBadgeClass = 'bg-warning';
        statusText = 'Revisions Requested';
      }
      
      // Generate action buttons based on status
      let actionButtons = '';
      
      if (submission.status === 'pending') {
        actionButtons = `
          <div class="btn-group btn-group-sm">
            <button class="btn btn-outline-primary view-btn" data-submission-id="${submission.id}">View</button>
            <button class="btn btn-outline-success assign-btn" data-submission-id="${submission.id}">Assign</button>
            <button class="btn btn-outline-danger reject-btn" data-submission-id="${submission.id}">Reject</button>
          </div>
        `;
      } else if (submission.status === 'in_review') {
        actionButtons = `
          <div class="btn-group btn-group-sm">
            <button class="btn btn-outline-primary view-btn" data-submission-id="${submission.id}">View</button>
            <button class="btn btn-outline-info progress-btn" data-submission-id="${submission.id}">Progress</button>
          </div>
        `;
      } else if (submission.status === 'reviewed') {
        actionButtons = `
          <div class="btn-group btn-group-sm">
            <button class="btn btn-outline-primary view-btn" data-submission-id="${submission.id}">View</button>
            <button class="btn btn-outline-success accept-btn" data-submission-id="${submission.id}">Accept</button>
            <button class="btn btn-outline-warning revise-btn" data-submission-id="${submission.id}">Revise</button>
            <button class="btn btn-outline-danger reject-btn" data-submission-id="${submission.id}">Reject</button>
          </div>
        `;
      } else {
        actionButtons = `
          <div class="btn-group btn-group-sm">
            <button class="btn btn-outline-primary view-btn" data-submission-id="${submission.id}">View</button>
          </div>
        `;
      }
      
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${submission.id}</td>
        <td>${submission.title}</td>
        <td>${submission.author_name || submission.authors}</td>
        <td>${submissionDate.toLocaleDateString()}</td>
        <td>${submission.category}</td>
        <td><span class="badge ${statusBadgeClass}">${statusText}</span></td>
        <td>${actionButtons}</td>
      `;
      
      submissionsTableBody.appendChild(row);
    });
    
    // Add submission entries to the dropdown
    submissionSelect.innerHTML = '<option selected disabled>Choose a submission to assign reviewers</option>';
    
    const pendingSubmissions = submissions.filter(sub => sub.status === 'pending');
    pendingSubmissions.forEach(submission => {
      const option = document.createElement('option');
      option.value = submission.id;
      option.textContent = `${submission.id}: ${submission.title}`;
      submissionSelect.appendChild(option);
    });
    
    // Add event listeners to buttons
    const viewButtons = document.querySelectorAll('.view-btn');
    viewButtons.forEach(button => {
      button.addEventListener('click', function() {
        const submissionId = this.getAttribute('data-submission-id');
        viewSubmission(submissionId);
      });
    });
    
    const assignButtons = document.querySelectorAll('.assign-btn');
    assignButtons.forEach(button => {
      button.addEventListener('click', function() {
        const submissionId = this.getAttribute('data-submission-id');
        assignReviewer(submissionId);
      });
    });
    
    const decisionButtons = document.querySelectorAll('.accept-btn, .reject-btn, .revise-btn');
    decisionButtons.forEach(button => {
      button.addEventListener('click', function() {
        const submissionId = this.getAttribute('data-submission-id');
        let decision = 'accepted';
        
        if (this.classList.contains('reject-btn')) {
          decision = 'rejected';
        } else if (this.classList.contains('revise-btn')) {
          decision = 'revisions_requested';
        }
        
        makeDecision(submissionId, decision);
      });
    });
    
    // Update statistics in the cards
    const pendingCount = submissions.filter(sub => sub.status === 'pending').length;
    const inReviewCount = submissions.filter(sub => sub.status === 'in_review').length;
    const reviewedCount = submissions.filter(sub => sub.status === 'reviewed').length;
    
    // Find and update the count displays
    const cardCounters = document.querySelectorAll('.display-4');
    cardCounters[0].textContent = pendingCount; // New Submissions
    cardCounters[1].textContent = pendingCount; // Awaiting Assignment
    cardCounters[2].textContent = inReviewCount; // In Review
    cardCounters[3].textContent = reviewedCount; // Decision Needed
  }
  
  // Function to display reviewers in the assignment table
  function displayReviewers(reviewers) {
    // Find the reviewers table
    const reviewerTableHeaders = Array.from(document.querySelectorAll('th')).filter(
      th => th.textContent.includes('Available Reviewers') || th.textContent.includes('Name')
    );
    const reviewersTable = reviewerTableHeaders[0]?.closest('table');
    const reviewersTableBody = reviewersTable?.querySelector('tbody');
    
    if (!reviewersTableBody) {
      console.error('Could not find reviewers table');
      return;
    }
    
    reviewersTableBody.innerHTML = '';
    
    reviewers.forEach(reviewer => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${reviewer.name}</td>
        <td>${reviewer.bio || 'No expertise information available'}</td>
        <td>0 active reviews</td>
        <td><button class="btn btn-sm btn-outline-primary assign-reviewer-btn" data-reviewer-id="${reviewer.id}">Assign</button></td>
      `;
      
      reviewersTableBody.appendChild(row);
    });
    
    // Add event listeners to assign buttons
    const assignButtons = reviewersTableBody.querySelectorAll('.assign-reviewer-btn');
    assignButtons.forEach(button => {
      button.addEventListener('click', function() {
        const reviewerId = this.getAttribute('data-reviewer-id');
        const submissionId = submissionSelect.value;
        
        if (submissionId) {
          assignReviewerToSubmission(submissionId, reviewerId);
        } else {
          alert('Please select a submission first.');
        }
      });
    });
  }
  
  // Function to view a submission
  function viewSubmission(submissionId) {
    alert('View submission ' + submissionId);
    // In a real implementation, you'd show a modal with the submission details
  }
  
  // Function to assign a reviewer
  function assignReviewer(submissionId) {
    // Scroll to the assign reviewers section
    const assignReviewersHeader = Array.from(document.querySelectorAll('.card-header')).find(
      header => header.textContent.includes('Assign Reviewers')
    );
    
    if (assignReviewersHeader) {
      const assignReviewersCard = assignReviewersHeader.closest('.card');
      assignReviewersCard.scrollIntoView({ behavior: 'smooth' });
      
      // Set the selected submission
      submissionSelect.value = submissionId;
    } else {
      console.error('Could not find assign reviewers section');
    }
  }
  
  // Function to assign a reviewer to a submission
  function assignReviewerToSubmission(submissionId, reviewerId) {
    // Get the due date (21 days from now)
    const dueDate = new Date();
    dueDate.setDate(dueDate.getDate() + 21);
    
    fetch('/assign_reviewer', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        submission_id: submissionId,
        reviewer_id: reviewerId,
        due_date: dueDate.toISOString().split('T')[0] // Format as YYYY-MM-DD
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('Reviewer assigned successfully.');
        loadEditorDashboard(); // Refresh the dashboard
      } else {
        alert('Error assigning reviewer: ' + data.message);
      }
    })
    .catch(error => {
      console.error('Error assigning reviewer:', error);
      alert('Failed to assign reviewer. Please try again later.');
    });
  }
  
  // Function to make a decision on a submission
  function makeDecision(submissionId, decision) {
    // Ask for comments
    const comments = prompt('Please provide any comments for this decision:');
    
    fetch('/make_decision', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        submission_id: submissionId,
        decision: decision,
        comments: comments || ''
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('Decision recorded successfully.');
        loadEditorDashboard(); // Refresh the dashboard
      } else {
        alert('Error recording decision: ' + data.message);
      }
    })
    .catch(error => {
      console.error('Error making decision:', error);
      alert('Failed to record decision. Please try again later.');
    });
  }
  
  // Setup based on active tab
  reviewerTab.addEventListener('shown.bs.tab', function() {
    loadReviewerAssignments();
  });
  
  editorTab.addEventListener('shown.bs.tab', function() {
    loadEditorDashboard();
  });
  
  // Function to show an alert message
  function showAlert(type, message) {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Insert at the top of the active panel
    const activePanel = document.querySelector('.tab-pane.active');
    activePanel.insertBefore(alert, activePanel.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
      alert.classList.remove('show');
      setTimeout(() => {
        alert.remove();
      }, 150);
    }, 5000);
  }
  
  // Initialize
  setupTabs();
  
  // Load data for the active tab
  if (reviewerPanel.classList.contains('active')) {
    loadReviewerAssignments();
  } else if (editorPanel.classList.contains('active')) {
    loadEditorDashboard();
  }
});
</script>