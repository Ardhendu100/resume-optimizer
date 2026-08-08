const analyzeBtn = document.getElementById("analyze-btn");
const downloadPdfBtn = document.getElementById("download-pdf-btn");
const downloadTexBtn = document.getElementById("download-tex-btn");


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

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

        body: JSON.stringify({
            job_description: jobDescription
        })

        });



            const data = await response.json();


        console.log("API Response:", data);



        if (data.success) {


                document.getElementById("ats-score").innerText =
                    "Resume compiled successfully ✅";
                // Display ATS results
                const atsDiv = document.getElementById("ats-score");
                atsDiv.innerHTML = `ATS Score: ${data.ats_score}<br>`;
                atsDiv.innerHTML += `Matched Keywords: ${data.matched_keywords.join(", ")}<br>`;
                atsDiv.innerHTML += `Missing Keywords: ${data.missing_keywords.join(", ")}<br>`;
                atsDiv.innerHTML += `Suggestions: ${data.suggestions.join("; ")}`;


                const pdfUrl =
                    `/api/pdf/${data.workspace_id}`;


                document.getElementById("pdfViewer").src = pdfUrl;
                // Enable download buttons
                document.getElementById("download-pdf-btn").disabled = false;
                document.getElementById("download-tex-btn").disabled = false;
                // Store workspace id for download links
                window.currentWorkspaceId = data.workspace_id;


            } else {


                document.getElementById("ats-score").innerText =
                    "Compilation failed ❌";


        }



    }

    catch(error){


            console.error("Error:", error);


            document.getElementById("ats-score").innerText =
                "Server error ❌";

    }


    finally{


        analyzeBtn.disabled = false;

        analyzeBtn.textContent = "Analyze Resume";

    }


});

// Download button handlers
downloadPdfBtn.addEventListener("click", () => {
    if (window.currentWorkspaceId) {
        window.location.href = `/api/download/pdf/${window.currentWorkspaceId}`;
    }
});

downloadTexBtn.addEventListener("click", () => {
    if (window.currentWorkspaceId) {
        window.location.href = `/api/download/tex/${window.currentWorkspaceId}`;
    }
});