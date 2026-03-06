document.addEventListener('DOMContentLoaded', function() {
    const leaveRequestForm = document.getElementById('leaveRequestForm');
    
    if (leaveRequestForm) {
        leaveRequestForm.addEventListener('submit', function(e) {
            const startDate = new Date(document.querySelector('input[name="start_date"]').value);
            const endDate = new Date(document.querySelector('input[name="end_date"]').value);
            
            if (endDate < startDate) {
                e.preventDefault();
                alert('End date must be after start date');
                return false;
            }
            
            if (startDate < new Date()) {
                e.preventDefault();
                alert('Start date cannot be in the past');
                return false;
            }
        });
    }
    
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 500);
        });
    }, 3000);
});
