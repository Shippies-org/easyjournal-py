<?php
  $pageTitle = "Home - Academic Journal";
  $activePage = "home";
  include('includes/header.php');
  include('includes/navigation.php');
?>

<div class="container my-5">
  <div class="row">
    <div class="col-md-8">
      <h1 class="mb-4">Welcome to the Academic Journal</h1>
      <p class="lead">
        Our journal publishes high-quality research in various academic disciplines. We are dedicated to promoting scholarly excellence and advancing knowledge in the field.
      </p>
      
      <div class="card bg-dark mb-4">
        <div class="card-header">
          <h5 class="mb-0">Recent Publications</h5>
        </div>
        <div class="card-body">
          <p class="card-text">Placeholder for recent publications - will be dynamically populated in future versions.</p>
        </div>
      </div>
      
      <div class="card bg-dark mb-4">
        <div class="card-header">
          <h5 class="mb-0">Upcoming Issues</h5>
        </div>
        <div class="card-body">
          <p class="card-text">Placeholder for upcoming issues - will be dynamically populated in future versions.</p>
        </div>
      </div>
    </div>
    
    <div class="col-md-4">
      <div class="card bg-dark mb-4">
        <div class="card-header">
          <h5 class="mb-0">Journal Information</h5>
        </div>
        <div class="card-body">
          <p>ISSN: XXXX-XXXX</p>
          <p>Publication Frequency: Quarterly</p>
          <p>Peer Review Process: Double-blind</p>
          <p>Acceptance Rate: XX%</p>
        </div>
      </div>
      
      <div class="card bg-dark mb-4">
        <div class="card-header">
          <h5 class="mb-0">Important Dates</h5>
        </div>
        <div class="card-body">
          <p>Submission Deadline: [Date]</p>
          <p>Review Completion: [Date]</p>
          <p>Publication Date: [Date]</p>
        </div>
      </div>
      
      <div class="card bg-dark">
        <div class="card-header">
          <h5 class="mb-0">Contact</h5>
        </div>
        <div class="card-body">
          <p>Email: journal@example.edu</p>
          <p>Phone: (555) 123-4567</p>
        </div>
      </div>
    </div>
  </div>
</div>

<?php include('includes/footer.php'); ?>
