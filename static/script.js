const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');
let drawing = false;
let points = [];
let originalImageData; // Variable to store the original image data

const toolBtns = document.querySelectorAll(".tool"),
sizeSlider = document.querySelector("#size-slider");
let brushWidth = 1;

document.getElementById('outputimg').style.display = 'none';

function draw(e) {
    if (!drawing) return;
    const rect = canvas.getBoundingClientRect(); // Get the bounding rectangle of the canvas
    const scaleX = canvas.width / rect.width; // Calculate the scale factor for X coordinate
    const scaleY = canvas.height / rect.height; // Calculate the scale factor for Y coordinate
    const x = (e.clientX - rect.left) * scaleX; // Adjusted X coordinate
    const y = (e.clientY - rect.top) * scaleY; // Adjusted Y coordinate
    
    ctx.lineWidth = brushWidth;
    ctx.lineCap = 'round';
    ctx.strokeStyle = '#000';
    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x, y);
    points.push([x, y]);
}

sizeSlider.addEventListener("change", () => brushWidth = sizeSlider.value);


function applyMask() {

    // Show loader
    document.getElementById('loader-container').style.display = 'flex';

    if (points.length >= 3 && originalImageData) { // Check if points and original image data are available
        const canvasData = canvas.toDataURL();  // Convert canvas to base64 data URL
        // Send the points, original image data, and canvas data to the server for processing
        fetch('/apply_mask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ points: points, original_image_data: originalImageData, image_data: canvasData })
        })
            .then(response => response.json())
            .then(data => {

                // Hide loader
                document.getElementById('loader-container').style.display = 'none';
                document.getElementById('output-image').src="static/output.jpg";
                document.getElementById('outputimg').style.display = 'flex';
                
                // Call function to handle processed image data and trigger download
                // console.log(data);
                processed_image_data=data.processed_image_data
            });
    } else {


         // Hide loader
         document.getElementById('loader-container').style.display = 'none';

        alert('Please select region and upload an image.');
    }
}
function downloadProcessedImage() {
    try{
    if (!processed_image_data) {
        console.error('Processed image data is empty.');
        return;
    }
    }
    catch(error)
    {
        alert("Image is not processed yet.");
        return;
    }
    try {
        // Decode the base64 encoded image data
        var decodedImageData = atob(processed_image_data);

        // Convert the decoded data to a Uint8Array
        var arrayBuffer = new ArrayBuffer(decodedImageData.length);
        var uint8Array = new Uint8Array(arrayBuffer);
        for (var i = 0; i < decodedImageData.length; i++) {
            uint8Array[i] = decodedImageData.charCodeAt(i);
        }

        // Create a Blob from the Uint8Array
        var blob = new Blob([uint8Array], { type: 'image/jpeg' });

        // Create a URL for the Blob
        var url = URL.createObjectURL(blob);

        // Create a link element to trigger the download
        var link = document.createElement('a');
        link.href = url;
        link.download = 'processed_image.jpg';

        // Append link to body and trigger download
        document.body.appendChild(link);
        link.click();

        // Cleanup
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Failed to decode and download processed image:', error);
    }
}

canvas.addEventListener('mousedown', () => {
    drawing = true;
    ctx.beginPath();
});

canvas.addEventListener('mouseup', () => {
    drawing = false;
    ctx.closePath();
});

canvas.addEventListener('mousemove', draw);

document.getElementById('imageUploader').addEventListener('change', (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    document.getElementById('outputimg').style.display = 'none';
    reader.onload = (e) => {
        const img = new Image();
        img.src = e.target.result;
        img.onload = () => {
            let newWidth = img.width;
            let newHeight = img.height;

            console.log(`Image width: ${newWidth}, height: ${newHeight}`);
            document.getElementById('drawingCanvas').width = newWidth;
            document.getElementById('drawingCanvas').height = newHeight;
           
            ctx.clearRect(0, 0, newWidth, newHeight);
            ctx.drawImage(img, 0, 0, newWidth, newHeight);
            originalImageData = e.target.result; // Store the original image data
        };
        // fileUploaderContainer.style.display = 'none';
    };

    reader.readAsDataURL(file);
});


window.addEventListener('load', () => {
    // Scroll to the top of the page
    if (performance.navigation.type === 1) {
        // Redirect to the main page URL
        window.location.href = 'http://127.0.0.1:5000/'; 
    }
});

