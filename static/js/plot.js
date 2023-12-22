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

    const numeric_values_ids = ['tr-impedance', 'tr-angle']
    for (const id of numeric_values_ids) {
        const value = document.getElementById(id).value.trim();
        if (!isNumeric(value)) {
            // Show toast and fail
            showToast('Błąd - trójkąt impedancji', 'Impedancja, i kąt muszą być liczbami rzeczywistymi.', 3000);
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

function addDatapoint(event) {
    const button = event.target;
    const datapoint = button.parentElement.parentElement;
    let id = datapoint.id;
    idList = id.split('-');
    idList[2] = parseInt(idList[2]) + 1;
    id = idList.join('-');
    console.log(id);
    const newDatapoint = datapoint.cloneNode(true);
    newDatapoint.id = id;
    datapoint.parentNode.insertBefore(newDatapoint, datapoint.nextSibling);
}

function addSymbol(event) {
    const button = event.target;
    const symbol = button.parentElement.parentElement;

    // Get id by incrementing the last input id
    inputElement = symbol.querySelector('input');
    let id = inputElement.id;
    idList = id.split('-');
    idList[1] = parseInt(idList[1]) + 1;
    id = idList.join('-');

    const newSymbol = symbol.cloneNode(true);
    newInputElement = newSymbol.querySelector('input');
    newInputElement.id = id;

    newDatapointElement = newSymbol.querySelector('div');
    idList = id.split('-');
    idList.splice(2, 0, "0");
    idList[3] = "datapoint";
    id = idList.join('-');
    newDatapointElement.id = id;
    // newSymbol.id = id;
    symbol.parentNode.insertBefore(newSymbol, symbol.nextSibling);
}

function removeNode(event) {
    const button = event.target;
    const node = button.parentElement.parentElement;
    node.remove();
}

function findOptions(el) {
    const options = el.querySelectorAll('option');
    const parentParent = el.parentElement.parentElement;

    let divs = parentParent.querySelectorAll(':scope > div');
    divs = Array.from(divs);
    divs = divs.splice(1, divs.length - 2);
    let units = [];
    let j = 1;
    divs.forEach((element, index) => {
        units.push(element.querySelector('input').value + " (" + j + ".)");
        j++;
    });
    // Update options
    units.forEach(function(text, index) {
        if (options[index]) {
          // If the option exists, update its text
          options[index].textContent = text;
        } else {
          // If the option doesn't exist, create a new option and append it to the select element
          var newOption = document.createElement('option');
          newOption.textContent = text;
          el.appendChild(newOption);
        }
      });
      
      // Remove extra options if arr2 is shorter than the original options
      if (options.length > units.length) {
        for (var i = units.length; i < options.length; i++) {
          options[i].remove();
        }
      }

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