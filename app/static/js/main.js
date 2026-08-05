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



        if(data.success){


            document.getElementById("ats-score").innerText =
                "Resume compiled successfully ✅";


            const pdfUrl =
                `/api/pdf/${data.workspace_id}`;


            document.getElementById("pdfViewer").src = pdfUrl;


        }
        else{


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