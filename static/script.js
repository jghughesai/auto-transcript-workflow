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

function displayResponse(data) {
    if (data === "success") {
        const sideBarItem = document.createElement("div");
        sideBarItem.classList.add("step-card");
        sideBarContainer.append(sideBarItem);
        const sideBarItemPara = document.createElement("p");
        sideBarItemPara.textContent = "Successfully retrieved the AI generated summary of your transcript and uploaded it to your outputs folder."
        sideBarItem.append(sideBarItemPara);
    }
    else {
        const sideBarItem = document.createElement("div");
        sideBarItem.classList.add("step-card");
        sideBarContainer.append(sideBarItem);
        const sideBarItemPara = document.createElement("p");
        sideBarItemPara.textContent = "No Google Drive activity detected. Perhaps you forgot to add a transcript to the inputs folder?"
        sideBarItem.append(sideBarItemPara);
    }
}