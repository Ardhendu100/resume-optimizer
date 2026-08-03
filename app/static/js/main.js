const analyzeBtn = document.getElementById("analyze-btn");

analyzeBtn.addEventListener("click", async () => {

    const jobDescription =
        document.getElementById("job-description").value;

    if (!jobDescription.trim()) {
        alert("Please paste a Job Description.");
        return;
    }

    analyzeBtn.disabled = true;
    analyzeBtn.textContent = "Analyzing...";

    try {

        const response = await fetch("/api/analyze", {
            method: "POST"
        });

        const data = await response.json();

        document.getElementById("ats-score").innerText =
            data.success
                ? "Resume compiled successfully ✅"
                : "Compilation failed ❌";

        console.log(data);

    } catch (err) {
        console.error(err);
    }

    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "Analyze Resume";
});