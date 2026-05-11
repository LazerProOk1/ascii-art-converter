const dropZone = document.getElementById('dropZone');
const input = document.getElementById('imageInput');
const preview = document.getElementById('preview');
const previewImg = document.getElementById('previewImg');
const previewName = document.getElementById('previewName');
const convertBtn = document.getElementById('convertBtn');

function showPreview(file) {
  if (!file || !file.type.startsWith('image/')) return;
  const url = URL.createObjectURL(file);
  previewImg.src = url;
  previewName.textContent = file.name;
  preview.hidden = false;
}

input.addEventListener('change', () => {
  if (input.files[0]) showPreview(input.files[0]);
});

dropZone.addEventListener('click', (e) => {
  if (e.target.tagName !== 'LABEL') input.click();
});

dropZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropZone.classList.add('dragover');
});
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropZone.classList.remove('dragover');
  const file = e.dataTransfer.files[0];
  if (file) {
    const dt = new DataTransfer();
    dt.items.add(file);
    input.files = dt.files;
    showPreview(file);
  }
});

document.getElementById('convertForm').addEventListener('submit', () => {
  convertBtn.disabled = true;
  convertBtn.textContent = 'Конвертирую…';
});

function copyArt() {
  const text = document.getElementById('asciiOutput').textContent;
  navigator.clipboard.writeText(text).then(() => {
    const btn = event.target;
    const orig = btn.textContent;
    btn.textContent = 'Скопировано!';
    setTimeout(() => { btn.textContent = orig; }, 1800);
  });
}
