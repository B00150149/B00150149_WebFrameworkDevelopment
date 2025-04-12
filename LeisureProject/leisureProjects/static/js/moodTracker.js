document.getElementById('moodRatingForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const formData = new FormData(this);
  
  // Get current project/task from URL if available
  const pathParts = window.location.pathname.split('/');
  if (pathParts.includes('taskList')) {
    const projectId = pathParts[pathParts.indexOf('taskList') + 1];
    formData.append('project', projectId);
  }
  
  fetch('/mood-rating/', {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': '{{ csrf_token }}'
    }
  })
  .then(response => response.json())
  .then(data => {
    const responseDiv = document.getElementById('moodResponse');
    if (data.status === 'success') {
      responseDiv.innerHTML = `
        <div class="alert alert-success">
          Mood recorded successfully!
        </div>
      `;
      this.reset();
    } else {
      responseDiv.innerHTML = `
        <div class="alert alert-danger">
          Error: ${data.errors || 'Unknown error'}
        </div>
      `;
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
});
