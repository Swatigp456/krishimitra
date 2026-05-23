// KrishiMitra Main JavaScript - NO AUTO-REFRESH

// Auto-hide alerts after 5 seconds (only for success/error messages)
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(function(alert) {
            if (alert.classList.contains('alert-dismissible')) {
                const bsAlert = new bootstrap.Alert(alert);
                setTimeout(function() {
                    bsAlert.close();
                }, 5000);
            }
        });
    }, 1000);
});

// Price Alert Setup
function setPriceAlert(cropId, cropName) {
    const targetPrice = prompt(`Enter target price (₹/quintal) for ${cropName}:`);
    if (targetPrice && !isNaN(targetPrice)) {
        fetch('/market/set-alert/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: `crop=${cropId}&target_price=${targetPrice}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('✅ Price alert set successfully!');
            } else {
                alert('❌ Failed to set alert. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('❌ Error setting alert');
        });
    }
}

// Get CSRF Token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Form Validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.addEventListener('submit', function(e) {
            const required = form.querySelectorAll('[required]');
            let valid = true;
            required.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    valid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            if (!valid) {
                e.preventDefault();
                alert('Please fill all required fields.');
            }
        });
    }
}

// Initialize validations
document.addEventListener('DOMContentLoaded', function() {
    validateForm('registration-form');
    validateForm('login-form');
});
// NO location.reload() 
// NO setInterval for weather refresh
// NO auto-refresh functions