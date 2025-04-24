let music = document.getElementById('bgMusic');
window.onload = function () {
    // 从全局变量获取游戏背景信息
    const mapInfo = window.mapInfo;
    if (mapInfo && mapInfo.background_image) {
        document.body.style.backgroundImage = `url('${mapInfo.background_image}')`;
    }

    // 自动播放音乐
    music.play();
};

function showModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'flex';
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'none';
}

// 地图切换按钮控制
document.getElementById('toggleMapBtn').addEventListener('click', function () {
    const form = document.getElementById('mapForm');
    form.style.display = form.style.display === 'block'? 'none' : 'block';
});

// 读取信件按钮点击事件
document.getElementById('readBtn').addEventListener('click', function () {
    showModal('readModal');
    document.getElementById('readForm').addEventListener('submit', async function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        try {
            const response = await fetch(window.readUrl, {
                method: 'POST',
                body: formData
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            if (data.error) {
                alert(data.error);
            } else {
                const lettersListArea = document.getElementById('lettersListArea');
                lettersListArea.innerHTML = '';
                data.letters.forEach(letter => {
                    const letterItem = document.createElement('div');
                    letterItem.classList.add('letter-item');
                    letterItem.innerHTML = `
                        <div class="letter-title">${letter.title}</div>
                        <div class="letter-content">${letter.content}</div>
                    `;
                    lettersListArea.appendChild(letterItem);
                });
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
});

// 书写信件按钮点击事件
document.getElementById('writeBtn').addEventListener('click', function () {
    showModal('writeModal');
    document.getElementById('writeForm').addEventListener('submit', async function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        try {
            const response = await fetch(window.writeUrl, {
                method: 'POST',
                body: formData
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            if (data.error) {
                alert(data.error);
            } else {
                const writeMessageArea = document.getElementById('writeMessageArea');
                writeMessageArea.innerHTML = `<div class="message">${data.message}</div>`;
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
});

document.querySelectorAll('.close-btn').forEach(btn => {
    btn.addEventListener('click', function () {
        const modal = this.closest('.modal');
        hideModal(modal.id);
    });
});

// 点击模态框外部关闭
window.addEventListener('click', function (event) {
    if (event.target.classList.contains('modal')) {
        hideModal(event.target.id);
    }
});

// 位置信息显示3秒后淡出
const mapInfo = window.mapInfo;
if (mapInfo) {
    setTimeout(() => {
        const info = document.getElementById('locationInfo');
        if (info) {
            info.style.opacity = '1';
            setTimeout(() => {
                info.style.opacity = '0';
            }, 3000);
        }
    }, 500);
}

// 错误消息显示
const message = window.message;
if (message) {
    alert(message);
}

// 键盘快捷键支持
document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            if (modal.style.display === 'flex') {
                hideModal(modal.id);
            }
        });
    }
});

// 防止页面卸载时音乐停止（可选，根据需求调整）
window.addEventListener('beforeunload', function () {
    music.pause();
});

window.addEventListener('pageshow', function () {
    music.play();
});