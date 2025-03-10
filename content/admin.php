<div class="container my-5">
  <div class="row">
    <div class="col-12">
      <h1 class="mb-4">Admin Dashboard</h1>
      <p class="lead">Manage journal submissions, reviewers, and publications from this admin panel.</p>
      
      <!-- This is a placeholder - would be populated from database in future -->
      <div class="alert alert-info">
        <i class="bi bi-info-circle me-2"></i>
        This is a placeholder page. In the actual implementation, this would be a password-protected area with admin functionality.
      </div>
      
      <div class="row mb-4">
        <div class="col-md-3 mb-4">
          <div class="card bg-dark text-center h-100">
            <div class="card-body">
              <h2 class="display-4">25</h2>
              <h6 class="text-muted">New Submissions</h6>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-4">
          <div class="card bg-dark text-center h-100">
            <div class="card-body">
              <h2 class="display-4">42</h2>
              <h6 class="text-muted">In Review</h6>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-4">
          <div class="card bg-dark text-center h-100">
            <div class="card-body">
              <h2 class="display-4">18</h2>
              <h6 class="text-muted">Accepted</h6>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-4">
          <div class="card bg-dark text-center h-100">
            <div class="card-body">
              <h2 class="display-4">7</h2>
              <h6 class="text-muted">Rejected</h6>
            </div>
          </div>
        </div>
      </div>
      
      <div class="row">
        <div class="col-lg-8">
          <div class="card bg-dark mb-4">
            <div class="card-header">
              <h5 class="mb-0">Recent Submissions</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-dark">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Title</th>
                      <th>Author</th>
                      <th>Date</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>1023</td>
                      <td>Machine Learning Applications in Healthcare</td>
                      <td>John Smith</td>
                      <td>Feb 1, 2023</td>
                      <td><span class="badge bg-warning">Pending</span></td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <button class="btn btn-outline-primary">View</button>
                          <button class="btn btn-outline-secondary">Assign</button>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td>1022</td>
                      <td>Sustainable Energy Solutions</td>
                      <td>Maria Chen</td>
                      <td>Jan 29, 2023</td>
                      <td><span class="badge bg-info">In Review</span></td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <button class="btn btn-outline-primary">View</button>
                          <button class="btn btn-outline-secondary">Track</button>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td>1021</td>
                      <td>Advances in Genetic Engineering</td>
                      <td>David Kumar</td>
                      <td>Jan 27, 2023</td>
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
          </div>
          
          <div class="card bg-dark">
            <div class="card-header">
              <h5 class="mb-0">Reviewer Assignments</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-dark">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Reviewer</th>
                      <th>Article</th>
                      <th>Assigned</th>
                      <th>Due</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>2045</td>
                      <td>Dr. Emily Johnson</td>
                      <td>Machine Learning Applications in Healthcare</td>
                      <td>Feb 2, 2023</td>
                      <td>Feb 23, 2023</td>
                      <td><span class="badge bg-warning">Pending</span></td>
                    </tr>
                    <tr>
                      <td>2044</td>
                      <td>Prof. Robert Chen</td>
                      <td>Sustainable Energy Solutions</td>
                      <td>Jan 30, 2023</td>
                      <td>Feb 20, 2023</td>
                      <td><span class="badge bg-info">In Progress</span></td>
                    </tr>
                    <tr>
                      <td>2043</td>
                      <td>Dr. Sarah Patel</td>
                      <td>Advances in Genetic Engineering</td>
                      <td>Jan 28, 2023</td>
                      <td>Feb 18, 2023</td>
                      <td><span class="badge bg-success">Completed</span></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-lg-4">
          <div class="card bg-dark mb-4">
            <div class="card-header">
              <h5 class="mb-0">Admin Actions</h5>
            </div>
            <div class="card-body">
              <div class="d-grid gap-2">
                <button class="btn btn-outline-primary">Manage Submissions</button>
                <button class="btn btn-outline-primary">Manage Reviewers</button>
                <button class="btn btn-outline-primary">Manage Users</button>
                <button class="btn btn-outline-primary">Publication Settings</button>
                <button class="btn btn-outline-primary">Journal Settings</button>
                <button class="btn btn-outline-primary">Export Reports</button>
              </div>
            </div>
          </div>
          
          <div class="card bg-dark mb-4">
            <div class="card-header">
              <h5 class="mb-0">Publication Schedule</h5>
            </div>
            <div class="card-body">
              <ul class="list-group list-group-flush bg-transparent">
                <li class="list-group-item bg-transparent d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="mb-0">Volume 45, Issue 1</h6>
                    <small class="text-muted">March 2023</small>
                  </div>
                  <span class="badge bg-warning rounded-pill">In Progress</span>
                </li>
                <li class="list-group-item bg-transparent d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="mb-0">Volume 45, Issue 2</h6>
                    <small class="text-muted">June 2023</small>
                  </div>
                  <span class="badge bg-secondary rounded-pill">Planned</span>
                </li>
                <li class="list-group-item bg-transparent d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="mb-0">Volume 45, Issue 3</h6>
                    <small class="text-muted">September 2023</small>
                  </div>
                  <span class="badge bg-secondary rounded-pill">Planned</span>
                </li>
              </ul>
            </div>
          </div>
          
          <div class="card bg-dark">
            <div class="card-header">
              <h5 class="mb-0">System Status</h5>
            </div>
            <div class="card-body">
              <ul class="list-group list-group-flush bg-transparent">
                <li class="list-group-item bg-transparent d-flex justify-content-between align-items-center">
                  <span>Database</span>
                  <span class="badge bg-success">Online</span>
                </li>
                <li class="list-group-item bg-transparent d-flex justify-content-between align-items-center">
                  <span>Email Service</span>
                  <span class="badge bg-success">Online</span>
                </li>
                <li class="list-group-item bg-transparent d-flex justify-content-between align-items-center">
                  <span>File Storage</span>
                  <span class="badge bg-success">Online</span>
                </li>
                <li class="list-group-item bg-transparent d-flex justify-content-between align-items-center">
                  <span>Last Backup</span>
                  <span>Feb 1, 2023 03:00 AM</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>