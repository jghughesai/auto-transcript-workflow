const runBtn = document.querySelector("button");
const sideBarContainer = document.getElementById("sideBarContainer");

runBtn.addEventListener("click", () => {
    console.log("Hi");
    fetch("/run_main")
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            console.log("Server Response: ", data)
            displayResponse(data)
        })
        .catch(error => {
            console.error("Error:", error);
        })
})

async function displayResponse(data) {
    if (data === "success") {
        let steps = ["Connected to Google Drive Activity API.", "Retrieved Google Drive activities from inputs folder.", "Downloaded files to local dir.", "Generated AI Summary.", "Your AI summary was successfully uploaded to the outputs folder in your Google Drive!"]
        createSideBarElements(steps);
    }
    else {
        let steps = ["No Google Drive activity detected. Perhaps you forgot to add a transcript to the inputs folder?"]
        createSideBarElements(steps);
    }
}

async function createSideBarElements(steps) {
    let paraText;
    console.log("Waiting for 2 seconds...")
    await delay(2000);
    console.log("2 seconds have passed")
    for (let i = 0; i < steps.length; i++) {
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