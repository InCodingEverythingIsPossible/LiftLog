// Open the exercise creation modal
function openCreateExerciseModal() {
  document.getElementById("exercise-create-modal").style.display = "flex";
}

// Close the exercise creation modal
function closeCreateExerciseModal() {
  document.getElementById("exercise-create-modal").style.display = "none";
}

// Wait until the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("create-exercise-form");

  // Exit if the form is not found
  if (!form) return;

  // Handle form submission with AJAX
  form.addEventListener("submit", async function (e) {
    e.preventDefault(); // Prevent default form behavior

    const formData = new FormData(form);
    const csrfToken = form.querySelector("[name=csrfmiddlewaretoken]").value;

    try {
      // Send form data via POST to the API endpoint
        const response = await fetch(createExerciseApiUrl, {
          method: "POST",
          headers: {
            "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value,
          },
          body: formData,
        });

      if (!response.ok) {
        throw new Error("Failed to create exercise");
      }

      const newExercise = await response.json();

      // Add the new exercise to the exercise picker UI
      addExerciseToPicker(newExercise);

      // Reset the form and close the modal
      form.reset();
      closeCreateExerciseModal();
    } catch (err) {
      console.error(err);
      alert("Error adding exercise. Please try again.");
    }
  });
});

// Append a new exercise to the global list and re-render the picker UI
function addExerciseToPicker(exercise) {
  // Add the new exercise to the global array
  allExercises.push(exercise);

  // Update the muscle filter options in case the new exercise introduces a new muscle group
  updateMuscleFilterOptions();

  // Re-render the exercise list so the new exercise appears properly filtered and selectable
  renderExerciseList();
}

// Helper function to update muscle filter dropdown based on current allExercises
function updateMuscleFilterOptions() {
  const muscleSet = new Set(allExercises.map(ex => ex.primary_muscle));
  const select = document.getElementById("muscle-filter");
  select.innerHTML = '<option value="all">All muscles</option>';
  muscleSet.forEach(muscle => {
    const opt = document.createElement("option");
    opt.value = muscle;
    opt.textContent = muscle;
    select.appendChild(opt);
  });
}