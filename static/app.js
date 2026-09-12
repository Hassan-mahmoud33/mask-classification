const imageInput = document.querySelector('#imageInput');
const chooseButton = document.querySelector('#chooseButton');
const predictButton = document.querySelector('#predictButton');
const dropZone = document.querySelector('#dropZone');
const previewFrame = document.querySelector('#previewFrame');
const previewImage = document.querySelector('#previewImage');
const fileName = document.querySelector('#fileName');
const result = document.querySelector('#result');
const resultMark = document.querySelector('#resultMark');
const resultText = document.querySelector('#resultText');
const confidenceText = document.querySelector('#confidenceText');
const errorMessage = document.querySelector('#errorMessage');

let selectedFile = null;

chooseButton.addEventListener('click', () => imageInput.click());
imageInput.addEventListener('change', () => setFile(imageInput.files[0]));

['dragenter', 'dragover'].forEach((eventName) => {
  dropZone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropZone.classList.add('over');
  });
});
['dragleave', 'drop'].forEach((eventName) => {
  dropZone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropZone.classList.remove('over');
  });
});
dropZone.addEventListener('drop', (event) => setFile(event.dataTransfer.files[0]));

function setFile(file) {
  if (!file || !file.type.startsWith('image/')) {
    showError('من فضلك اختار صورة بصيغة JPG أو PNG.');
    return;
  }
  selectedFile = file;
  previewImage.src = URL.createObjectURL(file);
  previewFrame.classList.remove('empty');
  fileName.textContent = file.name;
  predictButton.disabled = false;
  result.hidden = true;
  errorMessage.hidden = true;
}

predictButton.addEventListener('click', async () => {
  if (!selectedFile) return;
  predictButton.disabled = true;
  predictButton.textContent = 'جاري التحليل...';
  errorMessage.hidden = true;

  const formData = new FormData();
  formData.append('image', selectedFile);
  try {
    const response = await fetch('/api/predict', { method: 'POST', body: formData });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'حدث خطأ أثناء التحليل.');
    result.classList.toggle('no-mask', !data.has_mask);
    resultMark.textContent = data.has_mask ? '✓' : '!';
    resultText.textContent = data.has_mask ? 'لابس ماسك' : 'مش لابس ماسك';
    confidenceText.textContent = `نسبة الثقة: ${data.confidence}%`;
    result.hidden = false;
  } catch (error) {
    showError(error.message);
  } finally {
    predictButton.disabled = false;
    predictButton.textContent = 'تحليل الصورة';
  }
});

function showError(message) {
  errorMessage.textContent = message;
  errorMessage.hidden = false;
}
