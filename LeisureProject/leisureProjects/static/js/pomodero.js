
    // // Pomodoro Timer Logic
    // let timer;
    // let minutes = 25;
    // let seconds = 0;
    // let isRunning = false;

    // // Function to update the timer display
    // function updateTimerDisplay() {
    //     let minutesString = minutes < 10 ? "0" + minutes : minutes;
    //     let secondsString = seconds < 10 ? "0" + seconds : seconds;
    //     document.getElementById('timer-display').textContent = `${minutesString}:${secondsString}`;
    // }

    // // Show Pomodoro timer when "Pomodoro Method" button is clicked
    // document.getElementById('pomodoro-button').addEventListener('click', function() {
    //     document.getElementById('pomodoro-timer').style.display = 'block';
    // });

    // // Start button functionality
    // document.getElementById('start-button').addEventListener('click', function() {
    //     if (!isRunning) {
    //         isRunning = true;
    //         timer = setInterval(function() {
    //             if (seconds === 0) {
    //                 if (minutes === 0) {
    //                     clearInterval(timer);
    //                     isRunning = false;
    //                     alert("Pomodoro session complete! Take a break.");
    //                 } else {
    //                     minutes--;
    //                     seconds = 59;
    //                 }
    //             } else {
    //                 seconds--;
    //             }
    //             updateTimerDisplay();
    //         }, 1000);
    //         document.getElementById('stop-button').disabled = false;
    //         document.getElementById('start-button').disabled = true;
    //     }
    // });

    // // Stop button functionality
    // document.getElementById('stop-button').addEventListener('click', function() {
    //     if (isRunning) {
    //         clearInterval(timer);
    //         isRunning = false;
    //         document.getElementById('start-button').disabled = false;
    //         document.getElementById('stop-button').disabled = true;
    //     }
    // });

    // // Reset button functionality
    // document.getElementById('reset-button').addEventListener('click', function() {
    //     clearInterval(timer);
    //     isRunning = false;
    //     minutes = 25;
    //     seconds = 0;
    //     updateTimerDisplay();
    //     document.getElementById('start-button').disabled = false;
    //     document.getElementById('stop-button').disabled = true;
    // });

    // // Close Pomodoro timer when "X" button is clicked
    // document.getElementById('close-button').addEventListener('click', function() {
    //     document.getElementById('pomodoro-timer').style.display = 'none';
    // });
