const form = document.getElementById('form1');
const fileInput = document.getElementById('img_uploaded');
const submitButton = document.getElementById('upload');
const statusMessage = document.getElementById('statusMessage');
const fileListMetadata = document.getElementById('fileListMetadata');
const fileNum = document.getElementById('fileNum');
const progressBar = document.querySelector('progress');
const dropArea = document.getElementById('dropArea');

form.addEventListener('submit', handleSubmit);
fileInput.addEventListener('change', handleInputChange);
dropArea.addEventListener('drop', handleDrop);

initDropAreaHighlightOnDrag();

function handleSubmit(event) {
    event.preventDefault();

    showPendingState();

    uploadFiles(fileInput.files);
}

function handleDrop(event) {
    const fileList = event.dataTransfer.files;

    resetFormState();

    try {
        assertFilesValid(fileList);
    } catch (err) {
        updateStatusMessage(err.message);
        return;
    }

    showPendingState();

    uploadFiles(fileList);
}

function handleInputChange(event) {
    resetFormState();

    try {
        assertFilesValid(event.target.files);
    } catch (err) {
        updateStatusMessage(err.message);
        return;
    }

    submitButton.disabled = false;
}

function uploadFiles(files) {
    const url = 'http://127.0.0.1:5000/dirt_detect';
    const method = 'post';

    const xhr = new XMLHttpRequest();

    xhr.upload.addEventListener('progress', event => {
        updateStatusMessage(`⏳ Uploaded ${event.loaded} bytes of ${event.total}`);
        updateProgressBar(event.loaded / event.total);
    });

    xhr.addEventListener('loadend', () => {
        if (xhr.status === 200) {
            updateStatusMessage('✅ Success');
            renderFilesMetadata(files);
        } else {
            updateStatusMessage('❌ Error');
        }

        updateProgressBar(0);
    });

    const data = new FormData();

    for (const file of files) {
        data.append('file', file);
    }

    xhr.open(method, url);
    xhr.send(data);
    
    xhr.onreadystatechange = function(){
        if(xhr.readyState===XMLHttpRequest.DONE){
            var pred = xhr.responseText;
            var jsonResponse = JSON.parse(pred);
            var res = 'Image uploaded is <b>' + jsonResponse['prediction'] +'</b> with accuracy <b>'+jsonResponse['accuracy']+'%</b>';
            document.getElementById("result").innerHTML = res;
        }
    }    
    
}

function renderFilesMetadata(fileList) {
    fileNum.textContent = fileList.length;

    fileListMetadata.textContent = '';

    for (const file of fileList) {
        const name = file.name;
        const type = file.type;
        const size = file.size;

        fileListMetadata.insertAdjacentHTML(
            'beforeend',
            `
        <li>
          <p><strong>Name:</strong> ${name}</p>
          <p><strong>Type:</strong> ${type}</p>
          <p><strong>Size:</strong> ${size} bytes</p>
        </li>`
        );
    }
}

function assertFilesValid(fileList) {
    const allowedTypes = ['image/webp', 'image/jpeg', 'image/png', 'image/jpg'];
    const sizeLimit = 1024 * 1024 * 20; // 20 megabyte

    for (const file of fileList) {
        const { name: fileName, size: fileSize } = file;

        if (!allowedTypes.includes(file.type)) {
            throw new Error(`❌ File "${fileName}" could not be uploaded. Only images with the following types are allowed: WEBP, JPEG, PNG, JPG.`);
        }

        if (fileSize > sizeLimit) {
            throw new Error(`❌ File "${fileName}" could not be uploaded. Only images up to 20 MB are allowed.`);
        }
    }
}

function updateStatusMessage(text) {
    statusMessage.textContent = text;
}

function updateProgressBar(value) {
    const percent = value * 100;
    progressBar.value = Math.round(percent);
}

function showPendingState() {
    submitButton.disabled = true;
    updateStatusMessage('⏳ Pending...')
}

function resetFormState() {
    fileListMetadata.textContent = '';
    fileNum.textContent = '0';

    submitButton.disabled = true;
    updateStatusMessage(`🤷‍♂ Nothing's uploaded`)
}

function initDropAreaHighlightOnDrag() {
    let dragEventCounter = 0;

    dropArea.addEventListener('dragenter', event => {
        event.preventDefault();

        if (dragEventCounter === 0) {
            dropArea.classList.add('highlight');
        }

        dragEventCounter += 1;
    });

    dropArea.addEventListener('dragover', event => {
        event.preventDefault();

        if (dragEventCounter === 0) {
            dragEventCounter = 1;
        }
    });

    dropArea.addEventListener('dragleave', event => {
        event.preventDefault();

        dragEventCounter -= 1;

        if (dragEventCounter <= 0) {
            dragEventCounter = 0;
            dropArea.classList.remove('highlight');
        }
    });

    dropArea.addEventListener('drop', event => {
        event.preventDefault();

        dragEventCounter = 0;
        dropArea.classList.remove('highlight');
    });
}

