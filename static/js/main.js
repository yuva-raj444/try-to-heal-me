document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.querySelector('.drop-zone');
    const fileInput = document.getElementById('fileInput');
    const preview = document.getElementById('preview');
    const submitBtn = document.getElementById('submitBtn');
    const form = document.getElementById('uploadForm');
    let currentObjectURL = null;

    const resetForm = () => {
        if (currentObjectURL) {
            URL.revokeObjectURL(currentObjectURL);
            currentObjectURL = null;
        }
        fileInput.value = '';
        preview.style.display = 'none';
        preview.classList.remove('show');
        preview.src = '';
        submitBtn.disabled = true;
        submitBtn.classList.remove('loading');
        submitBtn.textContent = 'Analyze Image';
    };

    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            if (!files[0].type.startsWith('image/')) {
                alert('Please upload an image file');
                return;
            }
            fileInput.files = files;
            updatePreview();
        }
    });

    fileInput.addEventListener('change', updatePreview);

    function updatePreview() {
        const file = fileInput.files[0];
        if (!file) {
            resetForm();
            return;
        }

        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file');
            resetForm();
            return;
        }

        if (file.size > 10 * 1024 * 1024) {
            alert('File size must be less than 10MB');
            resetForm();
            return;
        }

        if (currentObjectURL) {
            URL.revokeObjectURL(currentObjectURL);
        }

        currentObjectURL = URL.createObjectURL(file);
        preview.style.display = 'block';
        preview.src = currentObjectURL;
        preview.onload = () => preview.classList.add('show');
        submitBtn.disabled = false;
    }

    form.addEventListener('submit', (e) => {
        submitBtn.classList.add('loading');
        submitBtn.textContent = 'Analyzing...';
    });

    // Cleanup on page unload
    window.addEventListener('unload', () => {
        if (currentObjectURL) {
            URL.revokeObjectURL(currentObjectURL);
        }
    });
})
