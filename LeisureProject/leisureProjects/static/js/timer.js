document.addEventListener('DOMContentLoaded', function() {
    let timer;
    let seconds = 0;
    let isRunning = false;
    let startTime = null;
    let endTime = null;
    const timerDisplay = document.getElementById('timer-display');
    const taskSelect = document.getElementById('task-select');

    // Function to update the timer display
    function updateTimerDisplay() {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        
        const hoursString = hours.toString().padStart(2, '0');
        const minutesString = minutes.toString().padStart(2, '0');
        const secondsString = secs.toString().padStart(2, '0');
        
        timerDisplay.textContent = `${hoursString}:${minutesString}:${secondsString}`;
    }

    // Start button functionality
    document.getElementById('start-button').addEventListener('click', function() {
        if (!isRunning) {
            if (!taskSelect.value) {
                alert('Please select a task before starting the timer.');
                return;
            }
            isRunning = true;
            startTime = new Date();
            timer = setInterval(function() {
                seconds++;
                updateTimerDisplay();
            }, 1000);
            document.getElementById('stop-button').disabled = false;
            document.getElementById('start-button').disabled = true;
        }
    });

    // Stop button functionality
    document.getElementById('stop-button').addEventListener('click', function() {
        if (isRunning) {
            clearInterval(timer);
            isRunning = false;
            endTime = new Date();
            document.getElementById('start-button').disabled = false;
            document.getElementById('stop-button').disabled = true;

            // Send time log to backend
            const taskId = taskSelect.value;
            if (taskId && startTime && endTime) {
                fetch('/tasks/log_time/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        task_id: taskId,
                        start_time: startTime.toISOString(),
                        end_time: endTime.toISOString()
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Time logged successfully.');
                    } else {
                        alert('Failed to log time: ' + (data.error || 'Unknown error'));
                    }
                })
                .catch(error => {
                    alert('Error logging time: ' + error);
                });
            }
        }
    });

    // Reset button functionality
    document.getElementById('reset-button').addEventListener('click', function() {
        clearInterval(timer);
        isRunning = false;
        seconds = 0;
        startTime = null;
        endTime = null;
        updateTimerDisplay();
        document.getElementById('start-button').disabled = false;
        document.getElementById('stop-button').disabled = true;
    });

    // Function to get CSRF token from cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // // Close timer when "X" button is clicked
    // document.getElementById('close-button').addEventListener('click', function() {
    //     document.getElementById('pomodoro-timer').style.display = 'none';
    // });
});
