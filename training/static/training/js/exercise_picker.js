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
    const selectedDiv = document.getElementById("selected-exercises");

    const existingIds = new Set();
    document.querySelectorAll("#selected-exercises .exercise-item").forEach(div => {
        existingIds.add(parseInt(div.dataset.exerciseId));
    });

    const newIds = selectedExerciseIds.filter(id => !existingIds.has(id));

    newIds.forEach((id) => {
        const exercise = allExercises.find(e => e.id === id);
        const wrapper = document.createElement("div");
        wrapper.className = "exercise-item";
        wrapper.dataset.exerciseId = id;

        const title = document.createElement("strong");
        title.textContent = exercise.name;

        const setsContainer = document.createElement("div");
        setsContainer.className = "sets-container";

        // Initialize with 1 set
        let setCount = 1;
        const firstSet = createSetInput(setCount++);
        setsContainer.appendChild(firstSet);

        // Add "Add Set" button
        const addSetBtn = document.createElement("button");
        addSetBtn.textContent = "+ Add Set";
        addSetBtn.type = "button";
        addSetBtn.style.marginTop = "0.5rem";
        addSetBtn.onclick = () => {
            const newSet = createSetInput(setCount++);
            setsContainer.appendChild(newSet);
        };

        wrapper.appendChild(title);
        wrapper.appendChild(setsContainer);
        wrapper.appendChild(addSetBtn);

        selectedDiv.appendChild(wrapper);
    });

    closeExercisePicker();
}

// Helper to create one set input
function createSetInput(setNumber = 1, previousValue = "") {
    const wrapper = document.createElement("div");
    wrapper.className = "set-row";
    wrapper.style.marginBottom = "0.5rem";

    // --- Top line with set number, previous info, kg and reps inputs ---
    const topLine = document.createElement("div");
    topLine.style.display = "flex";
    topLine.style.alignItems = "center";
    topLine.style.gap = "0.5rem";

    // Set number label
    const setLabel = document.createElement("span");
    setLabel.textContent = `Set ${setNumber}:`;
    setLabel.style.width = "60px";

    // Previous set info
    const prev = document.createElement("span");
    prev.textContent = previousValue || "Previous: —";
    prev.style.fontSize = "0.85rem";
    prev.style.color = "#777";
    prev.style.width = "120px";

    // kg input
    const kgInput = document.createElement("input");
    kgInput.type = "number";
    kgInput.placeholder = "kg";
    kgInput.min = 0;
    kgInput.style.width = "60px";

    // reps input
    const repsInput = document.createElement("input");
    repsInput.type = "number";
    repsInput.placeholder = "reps";
    repsInput.min = 0;
    repsInput.style.width = "60px";

    topLine.appendChild(setLabel);
    topLine.appendChild(prev);
    topLine.appendChild(kgInput);
    topLine.appendChild(repsInput);

    // --- Bottom line with rest timer input ---
    const timerLine = document.createElement("div");
    timerLine.style.textAlign = "center";
    timerLine.style.marginTop = "0.3rem";

    // Rest timer input (format mm:ss)
    const restInput = document.createElement("input");
    restInput.type = "text";  // Text type to allow mm:ss format
    restInput.placeholder = "Rest (mm:ss)";
    restInput.value = "02:00";  // Default value
    restInput.style.width = "70px";
    restInput.style.fontSize = "0.9rem";
    restInput.style.textAlign = "center";

    timerLine.appendChild(restInput);

    // Append top and bottom lines to wrapper
    wrapper.appendChild(topLine);
    wrapper.appendChild(timerLine);

    return wrapper;
}