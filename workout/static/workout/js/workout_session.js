function parseRestTime(restStr) {
  const parts = restStr.split(':');
  return parseInt(parts[0], 10) * 60 + parseInt(parts[1], 10);
}

function formatTime(seconds) {
  const m = Math.floor(seconds / 60).toString().padStart(2, '0');
  const s = (seconds % 60).toString().padStart(2, '0');
  return `${m}:${s}`;
}

function startRestCountdown(id, initialTime) {
  const timerDiv = document.getElementById(id);
  if (!timerDiv) return;

  let timeLeft = initialTime;

  const interval = setInterval(() => {
    if (timeLeft <= 0) {
      clearInterval(interval);
      timerDiv.textContent = "🔥 Ready!";
      timerDiv.style.color = '#4caf50';  // green
    } else {
      timerDiv.textContent = "Rest: " + formatTime(timeLeft);
      timeLeft--;
    }
  }, 1000);

  return interval;
}

// Generic cookie getter (Django-recommended)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


const intervals = {};  // Store interval IDs for each timer

document.addEventListener("DOMContentLoaded", () => {
  const checkboxes = document.querySelectorAll('.set-done-toggle');
  checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function() {
      const timerId = this.dataset.timerId;
      if (this.checked) {
        const timerDiv = document.getElementById(timerId);
        if (!timerDiv) return;

        // Use initial time from data attribute or current text
        const timeStr = timerDiv.dataset.initialTime || timerDiv.textContent.replace('Rest: ', '').trim();
        const seconds = parseRestTime(timeStr);

        // Start countdown and save interval ID
        intervals[timerId] = startRestCountdown(timerId, seconds);
      } else {
        // Stop the countdown and clear interval
        if (intervals[timerId]) {
          clearInterval(intervals[timerId]);
          delete intervals[timerId];
        }
        const timerDiv = document.getElementById(timerId);
        if (timerDiv) {
          // Reset timer display to initial time
          timerDiv.textContent = `Rest: ${timerDiv.dataset.initialTime || '00:00'}`;
        }
      }
    });
  });
});


document.getElementById("finish-workout-btn").addEventListener("click", function () {
    // Get all checkboxes related to completed sets
    const allCheckboxes = document.querySelectorAll('.set-done-toggle');
    const unchecked = Array.from(allCheckboxes).filter(cb => !cb.checked);

    // If there are any unchecked sets, ask user whether to accept default values
    if (unchecked.length > 0) {
        const acceptDefaults = confirm("Some sets are not marked as completed.\nDo you want to accept default values and save the workout?");
        if (!acceptDefaults) return;
    }

    // Prepare data to send
    const data = [];

    // Iterate through each exercise card
    document.querySelectorAll('.exercise-card').forEach(card => {
        const exerciseId = card.dataset.exerciseId;
        const sets = [];

        // Collect data from each set row
        card.querySelectorAll('.set-row').forEach(row => {
            const kg = parseFloat(row.querySelector('.input-kg').value) || 0;
            const reps = parseInt(row.querySelector('.input-reps').value) || 0;
            const done = row.querySelector('.set-done-toggle').checked;

            sets.push({ kg, reps, done });
        });

        // Append to data array
        data.push({ exercise_id: exerciseId, sets });
    });

    // Get CSRF token
    const csrftoken = getCookie("csrftoken");

    // Send data to the backend
    fetch("/api/save_workout/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({ exercises: data })
    })
    .then(res => res.json())
    .then(resp => {
        if (resp.success) {
            alert("Workout successfully saved!");
            window.location.href = "/workouts/";  // Redirect to workout list or summary page
        } else {
            alert("Error: " + (resp.error || "Workout could not be saved."));
        }
    })
    .catch(err => {
        console.error("Save error:", err);
        alert("Network or server error occurred.");
    });
});