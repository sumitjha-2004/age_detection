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

const BRACKETS = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61+'];

chooseBtn.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  if (!file) return;

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

predictBtn.addEventListener('click', () => {
  predictBtn.disabled = true;
  predictBtn.textContent = 'Analyzing…';
  scanline.classList.add('is-scanning');
  statusLabel.textContent = 'Scanning…';

  // Simulated inference delay — swap this block for a real API call.
  setTimeout(() => {
    scanline.classList.remove('is-scanning');
    predictBtn.disabled = false;
    predictBtn.textContent = 'Run detection';
    statusDot.className = 'status-dot is-done';
    statusLabel.textContent = 'Prediction ready';
    renderResult();
  }, 1200);
});

function renderResult(){
  // Mock distribution — replace with real model output.
  const topIndex = 2; // "21-30"
  const raw = BRACKETS.map((_, i) => {
    if (i === topIndex) return 40 + Math.random() * 15;
    return Math.random() * 18;
  });
  const total = raw.reduce((a, b) => a + b, 0);
  const pcts = raw.map(v => Math.round((v / total) * 100));

  resultIdle.hidden = true;
  resultContent.hidden = false;
  resultValue.textContent = BRACKETS[topIndex];

  const topPct = pcts[topIndex];
  confidenceValue.textContent = `${topPct}%`;
  requestAnimationFrame(() => { confidenceFill.style.width = `${topPct}%`; });

  distributionEl.innerHTML = '';
  BRACKETS.forEach((label, i) => {
    const li = document.createElement('li');
    if (i === topIndex) li.classList.add('is-top');
    li.innerHTML = `
      <span>${label}</span>
      <span class="bar"><span style="width:${pcts[i]}%"></span></span>
      <span class="pct">${pcts[i]}%</span>
    `;
    distributionEl.appendChild(li);
  });
}