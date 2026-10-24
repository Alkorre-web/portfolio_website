const API_URL = 'http://localhost:8000';
let isLoginMode = true;

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    loadArtifacts();
});

// 1. Загрузка артефактов
async function loadArtifacts() {
    const grid = document.getElementById('artifactsGrid');
    grid.innerHTML = '<p class="loading">Загрузка...</p>';

    const category = document.getElementById('categoryFilter').value;
    const tag = document.getElementById('tagFilter').value;

    try {
        let url = `${API_URL}/api/artifacts/`;
        const params = new URLSearchParams();
        if (category) params.append('category', category);
        if (tag) params.append('tag', tag);
        if (params.toString()) url += `?${params.toString()}`;

        const response = await axios.get(url);
        renderArtifacts(response.data);
    } catch (error) {
        console.error('Ошибка загрузки:', error);
        grid.innerHTML = '<p style="color:red">Не удалось загрузить артефакты. Проверьте, запущен ли бэкенд.</p>';
    }
}

function renderArtifacts(artifacts) {
    const grid = document.getElementById('artifactsGrid');
    if (artifacts.length === 0) {
        grid.innerHTML = '<p>Артефакты не найдены.</p>';
        return;
    }

    grid.innerHTML = artifacts.map(item => `
        <div class="artifact-card">
            <h3>${item.title}</h3>
            <p style="color: #6c757d; font-size: 0.9rem;">${item.description}</p>
            <div class="tags">
                ${item.tags ? item.tags.map(t => `<span class="tag">#${t}</span>`).join('') : ''}
            </div>
            <div style="margin-top: 1rem; font-size: 0.85rem; color: #888;">
                Тип: ${item.type} | Файл: ${item.file_name}
            </div>
            <button onclick="openArtifact('${item._id}')" class="btn-primary" style="margin-top: 1rem; font-size: 0.9rem;">
                 Открыть
            </button>
        </div>
    `).join('');
}

// Функция открытия артефакта
async function openArtifact(artifactId) {
    try {
        const response = await axios.get(`${API_URL}/api/artifacts/${artifactId}`);
        const artifact = response.data;

        // Создаём модальное окно
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.style.display = 'block';

        let content = '';
        if (artifact.content_type === 'image/png') {
            // Для PNG показываем картинку
            content = `<img src="data:image/png;base64,${artifact.content}" style="max-width: 100%; height: auto;">`;
        } else {
            // Для Markdown конвертируем в HTML через marked.js
            content = marked.parse(artifact.content);
        }

        modal.innerHTML = `
            <div class="modal-content" style="max-width: 900px; max-height: 85vh; overflow-y: auto;">
                <span class="close" onclick="this.parentElement.parentElement.remove()">&times;</span>
                <h2>${artifact.title}</h2>
                <p style="color: #6c757d;">${artifact.description}</p>
                <div class="markdown-content">
                    ${content}
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Закрытие по клику вне модального окна
        modal.onclick = function(event) {
            if (event.target === modal) {
                modal.remove();
            }
        };
    } catch (error) {
        alert('Ошибка загрузки артефакта');
        console.error(error);
    }
}
// 2. Смена цвета фона
async function changeBackgroundColor() {
    const token = localStorage.getItem('token');
    const headers = token ? { Authorization: `Bearer ${token}` } : {};

    try {
        // Пытаемся вызвать API
        const response = await axios.post(`${API_URL}/api/change-color`, {}, { headers });
        const color = response.data.color || response.data.current_color;
        applyColor(color);
    } catch (error) {
        // Fallback: если эндпоинта нет или ошибка, генерируем цвет локально для демонстрации
        console.warn('API смены цвета недоступен, используем локальную генерацию для демо');
        const r = Math.floor(Math.random() * 256);
        const g = Math.floor(Math.random() * 256);
        const b = Math.floor(Math.random() * 256);
        applyColor(`rgb(${r}, ${g}, ${b})`);
    }
}

function applyColor(color) {
    document.documentElement.style.setProperty('--bg-color', color);
    // Делаем текст белым, если фон темный, и черным, если светлый (простая эвристика)
    document.documentElement.style.setProperty('--card-bg', 'rgba(255, 255, 255, 0.9)');
}

// 3. Аутентификация
function toggleAuthModal() {
    const modal = document.getElementById('authModal');
    modal.style.display = modal.style.display === 'block' ? 'none' : 'block';
}

function toggleAuthMode() {
    isLoginMode = !isLoginMode;
    document.getElementById('modalTitle').innerText = isLoginMode ? 'Вход' : 'Регистрация';
    document.getElementById('authSubmitBtn').innerText = isLoginMode ? 'Войти' : 'Зарегистрироваться';
    document.getElementById('displayName').style.display = isLoginMode ? 'none' : 'block';
    document.querySelector('.switch-auth').innerText = isLoginMode ? 'Нет аккаунта? Зарегистрироваться' : 'Уже есть аккаунт? Войти';
}

async function handleAuth(event) {
    event.preventDefault();
    const password = document.getElementById('password').value;
    const displayName = document.getElementById('displayName').value;
    const endpoint = isLoginMode ? '/api/login' : '/api/register';

    // Примечание: адаптируй payload под реальные поля твоего бэкенда
    const payload = isLoginMode ? { password } : { display_name: displayName, password };

    try {
        const response = await axios.post(`${API_URL}${endpoint}`, payload);
        if (response.data.access_token || response.data.token) {
            localStorage.setItem('token', response.data.access_token || response.data.token);
            toggleAuthModal();
            checkAuth();
            alert(isLoginMode ? 'Успешный вход!' : 'Регистрация успешна!');
        }
    } catch (error) {
        alert('Ошибка аутентификации. Проверьте данные или то, что эндпоинт реализован на бэкенде.');
        console.error(error);
    }
}

function checkAuth() {
    const token = localStorage.getItem('token');
    const btn = document.getElementById('authBtn');
    if (token) {
        btn.innerText = 'Выйти';
        btn.onclick = () => {
            localStorage.removeItem('token');
            checkAuth();
        };
    } else {
        btn.innerText = 'Войти';
        btn.onclick = toggleAuthModal;
    }
}

// Закрытие модального окна при клике вне его
window.onclick = function(event) {
    const modal = document.getElementById('authModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}


