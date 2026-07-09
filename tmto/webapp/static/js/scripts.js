document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('file-upload');
    const file = fileInput.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`/predict_${file.type.startsWith('image') ? 'image' : 'video'}/`, {
        method: 'POST',
        body: formData
    });

    if (file.type.startsWith('image')) {
        const blob = await response.blob();
        document.getElementById('input-image').src = URL.createObjectURL(file);
        document.getElementById('output-image').src = URL.createObjectURL(blob);
    } else {
        const videoUrl = URL.createObjectURL(file);
        document.getElementById('input-video').src = videoUrl;
        document.getElementById('output-video').src = URL.createObjectURL(await response.blob());
    }
});

const ws = new WebSocket(`ws://${location.host}/live_feed/`);

ws.onmessage = (event) => {
    const outputImage = document.getElementById('output-image');
    outputImage.src = URL.createObjectURL(event.data);
};
