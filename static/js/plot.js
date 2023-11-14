function showToast(title, content, delay) {
    // Create a wrapping element for stacking toasts
    var toastContainer = document.getElementById('toastContainer');

    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toastContainer';
        toastContainer.className = 'position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }

    // Create a new toast element
    var toastElement = document.createElement('div');
    toastElement.className = 'toast';
    toastElement.setAttribute('role', 'alert');
    toastElement.setAttribute('aria-live', 'assertive');
    toastElement.setAttribute('aria-atomic', 'true');

    // Toast header
    var toastHeader = document.createElement('div');
    toastHeader.className = 'toast-header';
    var strongElement = document.createElement('strong');
    strongElement.className = 'me-auto';
    strongElement.textContent = title;
    var closeButton = document.createElement('button');
    closeButton.type = 'button';
    closeButton.className = 'btn-close';
    closeButton.setAttribute('data-bs-dismiss', 'toast');
    closeButton.setAttribute('aria-label', 'Close');

    // Toast body
    var toastBody = document.createElement('div');
    toastBody.className = 'toast-body';
    toastBody.textContent = content;

    // Assemble toast elements
    toastHeader.appendChild(strongElement);
    toastHeader.appendChild(closeButton);
    toastElement.appendChild(toastHeader);
    toastElement.appendChild(toastBody);

    // Append toast element to the toastContainer
    toastContainer.appendChild(toastElement);

    // Create a new Bootstrap Toast instance and show it
    var toastInstance = new bootstrap.Toast(toastElement, {
        delay: delay
    });

    // Remove the toast element from the DOM when it's hidden
    toastElement.addEventListener('hidden.bs.toast', function () {
        toastContainer.removeChild(toastElement);
    });

    toastInstance.show();
}

function isNumeric(value) {
    return !isNaN(parseFloat(value)) && isFinite(value);
}

async function drawTrojkat() {
    // Load pyodide with needed packages
    const pyodide = await loadPyodide({
        packages: ['matplotlib', 'numpy']
    });

    const numeric_values_ids = ['tr-impedance', 'tr-resistance', 'tr-angle']
    for (const id of numeric_values_ids) {
        const value = document.getElementById(id).value.trim();
        if (!isNumeric(value)) {
            // Show toast and fail
            showToast('Błąd - trójkąt impedancji', 'Impedancja, rezystancja i kąt muszą być liczbami rzeczywistymi.', 3000);
            return;
        }
    }

    // Run python code
    let python_code = ``;
    await fetch("static/python/trojkat-impedancji.py")
        .then((res) => res.text())
        .then((code) => {
            python_code = code;
        })
        .catch((err) => console.error(err));

    try {
        pyodide.runPython(python_code);
    } catch (error) {
        console.error(error)
    }

    const fig = pyodide.globals.get('tr_img');

    // Modify image element
    const fig_element = document.getElementById("tr-plot");
    fig_element.src = fig;
    fig_element.hidden = false;
    fig_element.alt = document.getElementById("tr-title").value;
}

async function drawFazory() {
    const pyodide = await loadPyodide({
        packages: ['matplotlib', 'numpy']
    });

    const numeric_values_ids = ['ph-voltage', 'ph-current', 'ph-angle']
    for (const id of numeric_values_ids) {
        const value = document.getElementById(id).value.trim();
        if (!isNumeric(value)) {
            // Show toast and fail
            showToast('Błąd - wykres fazorowy', 'Napięcie, natężenie i kąt muszą być liczbami rzeczywistymi.', 3000);
            return;
        }
    }

    // Run python code
    let python_code = ``;
    await fetch("static/python/wykres-fazorowy.py")
        .then((res) => res.text())
        .then((code) => {
            python_code = code;
        })
        .catch((err) => console.error(err));

    try {
        pyodide.runPython(python_code);
    } catch (error) {
        console.error(error)
    }

    const fig = pyodide.globals.get('ph_img');

    // Modify image element
    const fig_element = document.getElementById("ph-plot");
    fig_element.src = fig;
    fig_element.hidden = false;
    fig_element.alt = document.getElementById("ph-title").value;
}