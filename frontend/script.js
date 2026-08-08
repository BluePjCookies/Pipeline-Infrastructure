const imageInput = document.getElementById("image-input");
const dropZone = document.getElementById("drop-zone");

const previewContainer =
    document.getElementById("preview-container");

const imagePreview =
    document.getElementById("image-preview");

const removeButton =
    document.getElementById("remove-button");

const analyzeButton =
    document.getElementById("analyze-button");

const question =
    document.getElementById("question");

const loading =
    document.getElementById("loading");

const resultContainer =
    document.getElementById("result-container");

const result =
    document.getElementById("result");


let selectedImage = null;


// -------------------------
// File selection
// -------------------------

imageInput.addEventListener("change", function () {

    if (this.files.length > 0) {
        handleImage(this.files[0]);
    }

});


// -------------------------
// Drag and drop
// -------------------------

dropZone.addEventListener("dragover", function (event) {

    event.preventDefault();

    dropZone.classList.add("dragover");

});


dropZone.addEventListener("dragleave", function () {

    dropZone.classList.remove("dragover");

});


dropZone.addEventListener("drop", function (event) {

    event.preventDefault();

    dropZone.classList.remove("dragover");

    const files = event.dataTransfer.files;

    if (files.length > 0) {
        handleImage(files[0]);
    }

});


// -------------------------
// Handle image
// -------------------------

function handleImage(file) {

    if (!file.type.startsWith("image/")) {
        alert("Please select an image.");
        return;
    }

    selectedImage = file;

    const reader = new FileReader();

    reader.onload = function (event) {

        imagePreview.src = event.target.result;

        previewContainer.classList.remove("hidden");

        analyzeButton.disabled = false;

    };

    reader.readAsDataURL(file);
}


// -------------------------
// Remove image
// -------------------------

removeButton.addEventListener("click", function () {

    selectedImage = null;

    imageInput.value = "";

    imagePreview.src = "";

    previewContainer.classList.add("hidden");

    analyzeButton.disabled = true;

});


// -------------------------
// Analyze
// -------------------------

analyzeButton.addEventListener("click", async function () {

    if (!selectedImage) {
        return;
    }

    loading.classList.remove("hidden");

    analyzeButton.disabled = true;

    resultContainer.classList.add("hidden");


    const formData = new FormData();

    formData.append("image", selectedImage);

    try {

        // IMPORTANT:
        // Your OpenAI API key is NOT here.
        //
        // This request goes to YOUR backend.
        const API_URL = "http://127.0.0.1:8000"; // Insert backend address here, points to the server
        const response = await fetch(`${API_URL}/api/analyse`, {
            method: "POST",
            body: formData
        });


        if (!response.ok) {
            throw new Error("Analysis failed.");
        }


        const data = await response.json();
        const mistakes = data.analysis.mistakes;

        result.textContent = mistakes
            .map((mistakes, index) =>
                `Route ${index + 1}: ${mistakes.start} → ${mistakes.stop}`
            )
            .join("\n");


        resultContainer.classList.remove("hidden");


    } catch (error) {

        result.textContent =
            "Something went wrong. Please try again.";

        resultContainer.classList.remove("hidden");

        console.error(error);

    } finally {

        loading.classList.add("hidden");

        analyzeButton.disabled = false;

    }

});