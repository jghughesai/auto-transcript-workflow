const runBtn = document.querySelector("button");

runBtn.addEventListener("click", () => {
    console.log("Hi");
    fetch("/run_main")
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            console.log('Request successful with no data to return');
        })
        .catch(error => {
            console.error("Error:", error);
        })
})