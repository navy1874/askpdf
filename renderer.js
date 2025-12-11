// Get DOM elements
const openFileBtn = document.getElementById('openFileBtn');
const welcomeScreen = document.getElementById('welcomeScreen');
const contentDisplay = document.getElementById('contentDisplay');
const pdfViewer = document.getElementById('pdfViewer');
const textViewer = document.getElementById('textViewer');
const imageViewer = document.getElementById('imageViewer');
const textContent = document.getElementById('textContent');
const imageContent = document.getElementById('imageContent');
const fileName = document.getElementById('fileName');

// Handle file opening
openFileBtn.addEventListener('click', async () => {
  try {
    const fileData = await window.electronAPI.openFile();
    
    if (fileData) {
      displayFile(fileData);
    }
  } catch (error) {
    console.error('Error opening file:', error);
    alert('Error opening file: ' + error.message);
  }
});

function displayFile(fileData) {
  // Update file name
  fileName.textContent = fileData.name;
  
  // Hide welcome screen and show content
  welcomeScreen.classList.add('hidden');
  contentDisplay.classList.remove('hidden');
  
  // Hide all viewers
  pdfViewer.classList.add('hidden');
  textViewer.classList.add('hidden');
  imageViewer.classList.add('hidden');
  
  // Clear previous content
  pdfViewer.innerHTML = '';
  textContent.textContent = '';
  imageContent.src = '';
  
  // Display based on file type
  switch (fileData.type) {
    case 'pdf':
      displayPDF(fileData.data);
      break;
    case 'text':
      displayText(fileData.data);
      break;
    case 'image':
      displayImage(fileData.data);
      break;
  }
}

async function displayPDF(base64Data) {
  pdfViewer.classList.remove('hidden');
  
  try {
    // Create an object URL for the PDF
    const binaryData = atob(base64Data);
    const bytes = new Uint8Array(binaryData.length);
    for (let i = 0; i < binaryData.length; i++) {
      bytes[i] = binaryData.charCodeAt(i);
    }
    const blob = new Blob([bytes], { type: 'application/pdf' });
    const url = URL.createObjectURL(blob);
    
    // Create an iframe to display the PDF
    const iframe = document.createElement('iframe');
    iframe.src = url;
    iframe.style.width = '100%';
    iframe.style.height = '100%';
    iframe.style.border = 'none';
    
    pdfViewer.appendChild(iframe);
    
    // Clean up the object URL after the iframe loads
    iframe.onload = () => {
      URL.revokeObjectURL(url);
    };
  } catch (error) {
    console.error('Error rendering PDF:', error);
    pdfViewer.innerHTML = `<div style="padding: 20px; color: red;">Error loading PDF: ${error.message}</div>`;
  }
}

function displayText(content) {
  textViewer.classList.remove('hidden');
  textContent.textContent = content;
}

function displayImage(dataUrl) {
  imageViewer.classList.remove('hidden');
  imageContent.src = dataUrl;
}
