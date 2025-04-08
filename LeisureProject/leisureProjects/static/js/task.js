document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('.task-checkbox');

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const taskId = this.dataset.taskId;
            const isCompleted = this.checked;
            
            fetch(`/tasks/${taskId}/toggle/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    completed: isCompleted
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const taskText = this.nextElementSibling;
                    if (isCompleted) {
                        taskText.classList.add('text-decoration-line-through', 'text-muted');
                    } else {
                        taskText.classList.remove('text-decoration-line-through', 'text-muted');
                    }
                } else {
                    this.checked = !isCompleted; // Revert if failed
                }
            });
        });
    });
});

// Helper function to get CSRF token
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
