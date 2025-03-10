<?php
/**
 * Enhanced Admin Dashboard Template
 * This is a plugin-provided replacement for the standard admin.php template
 */
?>

<div class="container my-5">
    <div class="row">
        <div class="col-12">
            <h1>Enhanced Admin Dashboard</h1>
            <p class="lead">This template is provided by the custom_admin_plugin to demonstrate template overrides.</p>
        </div>
    </div>
    
    <div class="row my-4">
        <div class="col-md-3">
            <div class="card bg-primary text-white mb-4">
                <div class="card-body">
                    <h5 class="card-title">Submissions</h5>
                    <h2 class="display-4">24</h2>
                </div>
                <div class="card-footer d-flex align-items-center justify-content-between">
                    <a class="small text-white stretched-link" href="#">View Details</a>
                    <div class="small text-white"><i class="fas fa-angle-right"></i></div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-success text-white mb-4">
                <div class="card-body">
                    <h5 class="card-title">Published</h5>
                    <h2 class="display-4">15</h2>
                </div>
                <div class="card-footer d-flex align-items-center justify-content-between">
                    <a class="small text-white stretched-link" href="#">View Details</a>
                    <div class="small text-white"><i class="fas fa-angle-right"></i></div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-warning text-white mb-4">
                <div class="card-body">
                    <h5 class="card-title">Pending Review</h5>
                    <h2 class="display-4">7</h2>
                </div>
                <div class="card-footer d-flex align-items-center justify-content-between">
                    <a class="small text-white stretched-link" href="#">View Details</a>
                    <div class="small text-white"><i class="fas fa-angle-right"></i></div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-danger text-white mb-4">
                <div class="card-body">
                    <h5 class="card-title">Rejected</h5>
                    <h2 class="display-4">2</h2>
                </div>
                <div class="card-footer d-flex align-items-center justify-content-between">
                    <a class="small text-white stretched-link" href="#">View Details</a>
                    <div class="small text-white"><i class="fas fa-angle-right"></i></div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="col-lg-8">
            <div class="card mb-4">
                <div class="card-header">
                    <i class="fas fa-table mr-1"></i>
                    Recent Submissions
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-bordered" width="100%" cellspacing="0">
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
                                    <td>S-1001</td>
                                    <td>Machine Learning in Healthcare</td>
                                    <td>Dr. Smith</td>
                                    <td>2025-03-01</td>
                                    <td><span class="badge bg-warning">In Review</span></td>
                                    <td>
                                        <button class="btn btn-sm btn-primary">View</button>
                                        <button class="btn btn-sm btn-success">Assign</button>
                                    </td>
                                </tr>
                                <tr>
                                    <td>S-1002</td>
                                    <td>Sustainable Urban Development</td>
                                    <td>Prof. Johnson</td>
                                    <td>2025-03-02</td>
                                    <td><span class="badge bg-info">Submitted</span></td>
                                    <td>
                                        <button class="btn btn-sm btn-primary">View</button>
                                        <button class="btn btn-sm btn-success">Assign</button>
                                    </td>
                                </tr>
                                <tr>
                                    <td>S-1003</td>
                                    <td>Quantum Computing Applications</td>
                                    <td>Dr. Chen</td>
                                    <td>2025-03-03</td>
                                    <td><span class="badge bg-success">Published</span></td>
                                    <td>
                                        <button class="btn btn-sm btn-primary">View</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-lg-4">
            <div class="card mb-4">
                <div class="card-header">
                    <i class="fas fa-bell mr-1"></i>
                    Notifications
                </div>
                <div class="card-body">
                    <div class="list-group">
                        <a href="#" class="list-group-item list-group-item-action">
                            <div class="d-flex w-100 justify-content-between">
                                <h5 class="mb-1">New Submission</h5>
                                <small>3 hours ago</small>
                            </div>
                            <p class="mb-1">Dr. Smith submitted a new article: "Machine Learning in Healthcare"</p>
                        </a>
                        <a href="#" class="list-group-item list-group-item-action">
                            <div class="d-flex w-100 justify-content-between">
                                <h5 class="mb-1">Review Completed</h5>
                                <small>1 day ago</small>
                            </div>
                            <p class="mb-1">Dr. Andrews completed review of "Sustainable Urban Development"</p>
                        </a>
                        <a href="#" class="list-group-item list-group-item-action">
                            <div class="d-flex w-100 justify-content-between">
                                <h5 class="mb-1">System Update</h5>
                                <small>2 days ago</small>
                            </div>
                            <p class="mb-1">The system has been updated to version 2.3. View changelog.</p>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
// Additional JavaScript specifically for the enhanced admin dashboard
document.addEventListener('DOMContentLoaded', function() {
    console.log("Enhanced admin dashboard loaded via template override");
    
    // We could add chart initialization here using Chart.js
    // This is just a stub to demonstrate how JS could be included
});
</script>