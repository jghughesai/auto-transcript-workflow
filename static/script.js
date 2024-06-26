const runBtn = document.getElementById("runBtn");
const sideBarContainer = document.getElementById("sideBarContainer");

document.getElementById('apiKeyForm').onsubmit = async (e) => {
    e.preventDefault();
    const apiKey = document.getElementById('api_key').value;  // Ensure this matches the form field ID
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;

    const response = await fetch('/set_api_key', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ api_key: apiKey })  // Ensure the key matches the form field name
    });

    if (response.ok) {
        const data = await response.json();
        const apiKeyForm = document.getElementById('apiKeyForm');
        apiKeyForm.style.display = "none";
        runBtn.disabled = false;
        alert(data.message);
    } else {
        const data = await response.json();
        alert("Failed to set API key. " + (data.error || "Did you type it wrong?"));
    }
};


runBtn.addEventListener("click", () => {
    const elements = document.querySelectorAll('.step-card');
    elements.forEach(element => {
        element.parentNode.removeChild(element);
    });

    fetch("/run_main")
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            displayResponse(data)
        })
        .catch(error => {
            console.error("Error");
        })
})

async function displayResponse(data) {
    if (data === "success") {
        let steps = ["Connected to Google Drive Activity API.", "Retrieved Google Drive activities from inputs folder.", "Downloaded files to local dir.", "Generated AI Summary.", "Your AI summary was successfully uploaded to the outputs folder in your Google Drive!"];
        createSideBarElements(steps);
    }
    else if (data === "failed") {
        let steps = ["No Google Drive activity detected. Perhaps you forgot to add a transcript to the inputs folder?"];
        createSideBarElements(steps);
    }
    else {
        let steps = [data['error']];
        createSideBarElements(steps);
    }
}

async function createSideBarElements(steps) {
    let paraText;
    for (let i = 0; i < steps.length; i++) {
        await delay(2000);
        paraText = steps[i];
        const sideBarItem = document.createElement("div");
        sideBarItem.classList.add("step-card");
        sideBarContainer.append(sideBarItem);
        const sideBarItemPara = document.createElement("p");
        sideBarItemPara.textContent = paraText;
        sideBarItem.append(sideBarItemPara);
    }
}

function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}