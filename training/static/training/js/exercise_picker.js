let selectedExerciseIds = [];

function openExercisePicker() {

    renderExerciseList();

    const muscleSet = new Set(allExercises.map(ex => ex.primary_muscle));
    const select = document.getElementById("muscle-filter");
    select.innerHTML = '<option value="all">All muscles</option>';
    muscleSet.forEach(muscle => {
        const opt = document.createElement("option");
        opt.value = muscle;
        opt.textContent = muscle;
        select.appendChild(opt);
    });

    selectedExerciseIds = [];
    document.getElementById("exercise-picker").style.display = "flex";
}


function renderExerciseList() {
    const selectedMuscle = document.getElementById("muscle-filter").value;
    const filteredExercises = selectedMuscle === "all"
        ? allExercises
        : allExercises.filter(ex => ex.primary_muscle === selectedMuscle);

    const list = filteredExercises.map(ex => `
        <div class="exercise-option ${selectedExerciseIds.includes(ex.id) ? 'selected' : ''}"
             onclick="toggleExercise(${ex.id})"
             id="exercise-${ex.id}">
            <strong>${ex.name}</strong><br>
            <small>${ex.primary_muscle}</small>
        </div>
    `).join('');

    document.getElementById("exercise-picker-body").innerHTML = list;
}


function toggleExercise(id) {
    const idx = selectedExerciseIds.indexOf(id);
    if (idx > -1) {
        selectedExerciseIds.splice(idx, 1);
        document.getElementById(`exercise-${id}`).classList.remove('selected');
    } else {
        selectedExerciseIds.push(id);
        document.getElementById(`exercise-${id}`).classList.add('selected');
    }
}

function closeExercisePicker() {
    document.getElementById("exercise-picker").style.display = "none";
}

function confirmExerciseSelection() {
    // Log selected IDs
    console.log("Selected exercise IDs:", selectedExerciseIds);

    // Find selected exercises using their IDs
    const selectedExercises = allExercises.filter(ex => selectedExerciseIds.includes(ex.id));

    // Format and insert selected exercises into #selected-exercises div in create-template-modal
    const displayList = selectedExercises.map(ex => `
        <div class="exercise-item">
            <strong>${ex.name}</strong>
            <small>${ex.primary_muscle}</small>
        </div>
    `).join('');

    document.getElementById("selected-exercises").innerHTML = displayList;

    // Optionally: store selectedExercises globally or as hidden input for saving later
    window.selectedExercisesData = selectedExercises;

    // Close the picker modal
    closeExercisePicker();
}