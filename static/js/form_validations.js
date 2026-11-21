// Form Validation JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Password confirmation validation for signup forms
    const donorForm = document.getElementById('donorSignupForm');
    const volunteerForm = document.getElementById('volunteerSignupForm');
    
    function validatePasswordMatch(form) {
        if (!form) return;
        
        const password1 = form.querySelector('[name="password1"]');
        const password2 = form.querySelector('[name="password2"]');
        const messageDiv = document.getElementById('passwordMatchMessage');
        
        if (password2 && messageDiv) {
            password2.addEventListener('keyup', function() {
                if (password2.value === '') {
                    messageDiv.textContent = '';
                    messageDiv.className = 'form-text';
                } else if (password1.value === password2.value) {
                    messageDiv.textContent = 'Passwords match ✓';
                    messageDiv.className = 'form-text text-success';
                } else {
                    messageDiv.textContent = 'Passwords do not match ✗';
                    messageDiv.className = 'form-text text-danger';
                }
            });
            
            // Validate on form submit
            form.addEventListener('submit', function(e) {
                if (password1.value !== password2.value) {
                    e.preventDefault();
                    messageDiv.textContent = 'Passwords must match before submitting';
                    messageDiv.className = 'form-text text-danger';
                    password2.focus();
                }
            });
        }
    }
    
    validatePasswordMatch(donorForm);
    validatePasswordMatch(volunteerForm);
    
    // Form required field validation
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields');
            }
        });
    });
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});


