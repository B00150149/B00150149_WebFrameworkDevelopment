document.addEventListener('DOMContentLoaded', function() {
    let timer;
    let seconds = 0;
    let isRunning = false;
    const timerDisplay = document.getElementById('timer-display');
    const timeInput = document.getElementById('time-input');

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
            isRunning = true;
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
            document.getElementById('start-button').disabled = false;
            document.getElementById('stop-button').disabled = true;
        }
    });

    // Reset button functionality
    document.getElementById('reset-button').addEventListener('click', function() {
        clearInterval(timer);
        isRunning = false;
        seconds = 0;
        updateTimerDisplay();
        document.getElementById('start-button').disabled = false;
        document.getElementById('stop-button').disabled = true;
    });

    // // Close timer when "X" button is clicked
    // document.getElementById('close-button').addEventListener('click', function() {
    //     document.getElementById('pomodoro-timer').style.display = 'none';
    // });
});
