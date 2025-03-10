<!-- My Submissions Content -->
<div class="container py-5">
    <div class="row mb-4">
        <div class="col-md-8">
            <h1 class="display-5 mb-3">My Submissions</h1>
            <p class="lead text-muted">Track the status of your article submissions and review feedback.</p>
        </div>
        <div class="col-md-4 d-flex align-items-center justify-content-md-end mt-3 mt-md-0">
            <a href="submit.php" class="btn btn-primary">
                <i class="bi bi-plus-circle me-2"></i> Submit New Article
            </a>
        </div>
    </div>
    
    <!-- Status Alert -->
    <div id="statusAlert" class="alert d-none mb-4" role="alert"></div>
    
    <!-- Submissions list -->
    <div class="card shadow-sm mb-4">
        <div class="card-header bg-light py-3">
            <h5 class="mb-0">Your Article Submissions</h5>
        </div>
        <div class="card-body p-0">
            <div class="table-responsive">
                <table class="table table-hover mb-0" id="submissionsTable">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Title</th>
                            <th>Submission Date</th>
                            <th>Status</th>
                            <th class="text-end">Actions</th>
                        </tr>
                    </thead>
                    <tbody id="submissionsList">
                        <tr>
                            <td colspan="5" class="text-center py-4">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>
                                <p class="mt-2 text-muted">Loading your submissions...</p>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- No submissions message (shown when submissions list is empty) -->
    <div id="noSubmissions" class="card shadow-sm mb-4 d-none">
        <div class="card-body py-5 text-center">
            <div class="mb-3">
                <i class="bi bi-file-earmark-x text-muted" style="font-size: 3rem;"></i>
            </div>
            <h4>No Submissions Found</h4>
            <p class="text-muted mb-3">You haven't submitted any articles yet.</p>
            <a href="submit.php" class="btn btn-primary">
                <i class="bi bi-plus-circle me-2"></i> Submit Your First Article
            </a>
        </div>
    </div>
    
    <!-- Submission Details Modal -->
    <div class="modal fade" id="submissionDetailsModal" tabindex="-1" aria-labelledby="submissionDetailsModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="submissionDetailsModalLabel">Submission Details</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div id="submissionDetails">
                        <!-- Details loaded via JavaScript -->
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
// Load submissions when the page loads
document.addEventListener('DOMContentLoaded', function() {
    loadSubmissions();
});

function loadSubmissions() {
    fetch('/get_submissions')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displaySubmissions(data.submissions);
            } else {
                showAlert('danger', 'Error: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error fetching submissions:', error);
            showAlert('danger', 'Failed to load submissions. Please try again later.');
        });
}

function displaySubmissions(submissions) {
    const submissionsList = document.getElementById('submissionsList');
    const submissionsTable = document.getElementById('submissionsTable');
    const noSubmissions = document.getElementById('noSubmissions');
    
    // Clear the loading message
    submissionsList.innerHTML = '';
    
    if (submissions.length === 0) {
        // Show the no submissions message
        submissionsTable.closest('.card').classList.add('d-none');
        noSubmissions.classList.remove('d-none');
        return;
    }
    
    // Show the table, hide the no submissions message
    submissionsTable.closest('.card').classList.remove('d-none');
    noSubmissions.classList.add('d-none');
    
    // Add each submission to the table
    submissions.forEach(submission => {
        const row = document.createElement('tr');
        
        // Format the submission date
        const submissionDate = new Date(submission.submission_date);
        const formattedDate = submissionDate.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
        
        // Determine status badge class
        let statusBadgeClass = 'bg-secondary';
        if (submission.status === 'pending_review') {
            statusBadgeClass = 'bg-warning text-dark';
        } else if (submission.status === 'under_review') {
            statusBadgeClass = 'bg-info text-dark';
        } else if (submission.status === 'accepted') {
            statusBadgeClass = 'bg-success';
        } else if (submission.status === 'rejected') {
            statusBadgeClass = 'bg-danger';
        } else if (submission.status === 'revisions_requested') {
            statusBadgeClass = 'bg-primary';
        }
        
        // Format status for display
        let displayStatus = submission.status.replace('_', ' ');
        displayStatus = displayStatus.charAt(0).toUpperCase() + displayStatus.slice(1);
        
        row.innerHTML = `
            <td>${submission.id}</td>
            <td>
                <strong>${submission.title}</strong>
                <div class="text-muted small">${submission.authors}</div>
            </td>
            <td>${formattedDate}</td>
            <td><span class="badge ${statusBadgeClass}">${displayStatus}</span></td>
            <td class="text-end">
                <button class="btn btn-sm btn-outline-primary view-details" 
                        data-submission-id="${submission.id}" 
                        data-bs-toggle="modal" 
                        data-bs-target="#submissionDetailsModal">
                    <i class="bi bi-eye"></i> View
                </button>
            </td>
        `;
        
        submissionsList.appendChild(row);
    });
    
    // Add event listeners to the view details buttons
    document.querySelectorAll('.view-details').forEach(button => {
        button.addEventListener('click', function() {
            const submissionId = this.getAttribute('data-submission-id');
            const submission = submissions.find(s => s.id == submissionId);
            
            if (submission) {
                // Format the status for display
                let displayStatus = submission.status.replace('_', ' ');
                displayStatus = displayStatus.charAt(0).toUpperCase() + displayStatus.slice(1);
                
                // Format the date
                const submissionDate = new Date(submission.submission_date);
                const formattedDate = submissionDate.toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                });
                
                // Determine the right status badge
                let statusBadgeClass = 'bg-secondary';
                if (submission.status === 'pending_review') {
                    statusBadgeClass = 'bg-warning text-dark';
                } else if (submission.status === 'under_review') {
                    statusBadgeClass = 'bg-info text-dark';
                } else if (submission.status === 'accepted') {
                    statusBadgeClass = 'bg-success';
                } else if (submission.status === 'rejected') {
                    statusBadgeClass = 'bg-danger';
                } else if (submission.status === 'revisions_requested') {
                    statusBadgeClass = 'bg-primary';
                }
                
                // Set modal title
                document.getElementById('submissionDetailsModalLabel').textContent = 
                    `Submission #${submission.id}: ${submission.title}`;
                
                // Generate the details HTML
                const detailsHTML = `
                    <div class="row mb-4">
                        <div class="col-md-8">
                            <h5>Manuscript Details</h5>
                            <dl class="row mb-0">
                                <dt class="col-sm-3">Title</dt>
                                <dd class="col-sm-9">${submission.title}</dd>
                                
                                <dt class="col-sm-3">Authors</dt>
                                <dd class="col-sm-9">${submission.authors}</dd>
                                
                                <dt class="col-sm-3">Category</dt>
                                <dd class="col-sm-9">${submission.category}</dd>
                                
                                <dt class="col-sm-3">Keywords</dt>
                                <dd class="col-sm-9">${submission.keywords || 'None provided'}</dd>
                                
                                <dt class="col-sm-3">Submission Date</dt>
                                <dd class="col-sm-9">${formattedDate}</dd>
                            </dl>
                        </div>
                        <div class="col-md-4">
                            <div class="card h-100">
                                <div class="card-body">
                                    <h6 class="card-title">Status</h6>
                                    <span class="badge ${statusBadgeClass} d-block p-2 mb-2">${displayStatus}</span>
                                    
                                    <h6 class="mt-3">Document</h6>
                                    <a href="/uploads/${submission.file_path.split('/').pop()}" class="btn btn-sm btn-outline-primary" target="_blank">
                                        <i class="bi bi-file-earmark-text me-1"></i> View Manuscript
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-12">
                            <h5>Abstract</h5>
                            <div class="card mb-3">
                                <div class="card-body">
                                    <p>${submission.abstract}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-12">
                            <h5>Cover Letter</h5>
                            <div class="card">
                                <div class="card-body">
                                    <p>${submission.cover_letter || 'No cover letter provided.'}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                
                document.getElementById('submissionDetails').innerHTML = detailsHTML;
            }
        });
    });
}

function showAlert(type, message) {
    const alert = document.getElementById('statusAlert');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = message;
    alert.classList.remove('d-none');
    
    // Hide the loading indicators
    document.getElementById('submissionsList').innerHTML = '';
}
</script>