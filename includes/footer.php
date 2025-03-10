    <footer class="footer mt-auto py-4 bg-dark">
        <div class="container">
            <div class="row">
                <div class="col-md-4">
                    <h5>Academic Journal</h5>
                    <p class="text-muted">
                        Publishing high-quality academic research since 2005.
                    </p>
                </div>
                <div class="col-md-4">
                    <h5>Quick Links</h5>
                    <ul class="list-unstyled">
                        <li><a href="index.php" class="text-decoration-none">Home</a></li>
                        <li><a href="submit.php" class="text-decoration-none">Submit Article</a></li>
                        <li><a href="#" class="text-decoration-none">Author Guidelines</a></li>
                        <li><a href="#" class="text-decoration-none">About the Journal</a></li>
                        <li><a href="#" class="text-decoration-none">Contact Us</a></li>
                    </ul>
                </div>
                <div class="col-md-4">
                    <h5>Contact</h5>
                    <address>
                        <strong>Journal Editorial Office</strong><br>
                        123 Academic Way<br>
                        University City, State 12345<br>
                        <i class="bi bi-envelope me-2"></i> journal@example.edu<br>
                        <i class="bi bi-telephone me-2"></i> (555) 123-4567
                    </address>
                </div>
            </div>
            <div class="row mt-3">
                <div class="col-12 text-center">
                    <hr>
                    <p class="text-muted mb-0">
                        &copy; <?php echo date('Y'); ?> Academic Journal Submission System. All rights reserved.
                    </p>
                </div>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JavaScript Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Optional custom JavaScript -->
    <script>
        // Any custom JavaScript can go here
        document.addEventListener('DOMContentLoaded', function() {
            // Enable tooltips
            var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
            var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl)
            });
        });
    </script>
</body>
</html>
