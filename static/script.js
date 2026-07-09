const fileInput   = document.getElementById('fileInput');
const chooseBtn   = document.getElementById('chooseBtn');
const predictBtn  = document.getElementById('predictBtn');
const viewfinder  = document.getElementById('viewfinder');
const preview     = document.getElementById('preview');
const fileName    = document.getElementById('fileName');
const scanline    = document.getElementById('scanline');
const statusDot   = document.getElementById('statusDot');
const statusLabel = document.getElementById('statusLabel');

const resultIdle    = document.getElementById('resultIdle');
const resultContent = document.getElementById('resultContent');
const resultValue   = document.getElementById('resultValue');
const confidenceFill = document.getElementById('confidenceFill');
const confidenceValue = document.getElementById('confidenceValue');
const distributionEl = document.getElementById('distribution');

// Must match model.py's `classes` list exactly, in the same order
const BRACKETS = ['0-2', '3-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', 'more than 70'];

let selectedFile = null;

chooseBtn.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  if (!file) return;

  selectedFile = file;
  fileName.textContent = file.name;

  const reader = new FileReader();
  reader.onload = (e) => {
    preview.src = e.target.result;
    viewfinder.classList.add('has-image');
  };
  reader.readAsDataURL(file);

  predictBtn.disabled = false;
  statusDot.className = 'status-dot is-ready';
  statusLabel.textContent = 'Ready to run';

  resultContent.hidden = true;
  resultIdle.hidden = false;
});

predictBtn.addEventListener('click', async () => {
  if (!selectedFile) return;

  predictBtn.disabled = true;
  predictBtn.textContent = 'Analyzing…';
  scanline.classList.add('is-scanning');
  statusLabel.textContent = 'Scanning…';

  const formData = new FormData();
  formData.append('image', selectedFile);

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.error || `Server error (${response.status})`);
    }

    const data = await response.json();
    renderResult(data);

    statusDot.className = 'status-dot is-done';
    statusLabel.textContent = 'Prediction ready';

  } catch (err) {
    statusLabel.textContent = 'Error — see console';
    console.error('Prediction failed:', err);
    alert(`Prediction failed: ${err.message}`);

  } finally {
    scanline.classList.remove('is-scanning');
    predictBtn.disabled = false;
    predictBtn.textContent = 'Run detection';
  }
});

function renderResult(data){
  const { prediction, confidence, distribution } = data;

  resultIdle.hidden = true;
  resultContent.hidden = false;
  resultValue.textContent = prediction;

  confidenceValue.textContent = `${confidence}%`;
  requestAnimationFrame(() => { confidenceFill.style.width = `${confidence}%`; });

  distributionEl.innerHTML = '';
  BRACKETS.forEach((label) => {
    const pct = distribution[label] ?? 0;
    const li = document.createElement('li');
    if (label === prediction) li.classList.add('is-top');
    li.innerHTML = `
      <span>${label}</span>
      <span class="bar"><span style="width:${pct}%"></span></span>
      <span class="pct">${pct}%</span>
    `;
    distributionEl.appendChild(li);
  });
}