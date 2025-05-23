 // 初始化游
        document.addEventListener('DOMContentLoaded', function () {
            const csrfToken = document.querySelector('input[name="csrf_token"]').value;
            // 自动播放背景音乐
            const bgMusic = document.getElementById('bg-music');
            bgMusic.play().catch(e => console.log("Autoplay prevented:", e));

            // 显示当前位置3秒
            showLocationInfo();

            // 绑定按钮事件
            document.getElementById('next-dialog-btn').addEventListener('click', nextDialog);
            document.getElementById('collect-btn').addEventListener('click', function (e) {
                handleCollect(e, csrfToken);
            });
            document.getElementById('write-btn').addEventListener('click', () => showModal('write-modal'));
            document.getElementById('read-btn').addEventListener('click', () => showModal('read-modal'));
            document.getElementById('map-selector-btn').addEventListener('click', () => showModal('map-selector-modal'));
            // 表单提交事件
            document.getElementById('write-form').addEventListener('submit', function (e) {
                handleWriteSubmit(e, csrfToken);
            });
            document.getElementById('read-form').addEventListener('submit', function (e) {
                handleReadSubmit(e, csrfToken);
            });
            document.getElementById('location-form').addEventListener('submit', function (e) {
                handleLocationChange(e, csrfToken);
            });
        });

        // 显示位置信息3秒
        function showLocationInfo() {
            const locationInfo = document.getElementById('location-info');
            locationInfo.style.opacity = '1';
            setTimeout(() => {
                locationInfo.style.opacity = '0';
            }, 3000);
        }

        // 关闭模态框
        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
        }

        // 显示通知消息
        function showNotification(message, duration = 3000) {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.style.display = 'block';
            setTimeout(() => {
                notification.style.display = 'none';
            }, duration);
        }

        // 处理收集信件
        async function handleCollect(e, csrfToken) {
            e.preventDefault();
            try {
                const response = await fetch("{{ url_for('play.collect') }}", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrfToken
                    }
                });
                const data = await response.json();
                console.log(data+"fsdf");
                if (data.message) {
                    const modalContent = document.getElementById('collected-letter-content');
                    if (data.letter) {
                        modalContent.innerHTML = `
                            <h3>${data.letter.title}</h3>
                            <p>${data.letter.content}</p>
                        `;
                    } else {
                        modalContent.innerHTML = '<p>No letters to collect at this location.</p>';
                    }
                    showModal('collect-modal');
                    showNotification(data.message);
                } else if (data.error) {
                    showNotification(data.error);
                }
            } catch (error) {
                console.error('Error:', error);
                if (error.response && error.response.data && error.response.data.error) {
                    showNotification(error.response.data.error);
                } else {
                    showNotification('Error collecting letter');
                }
            }
        }

        // 处理写信提交
        async function handleWriteSubmit(e, csrfToken) {
            e.preventDefault();
            const formData = new FormData(e.target);
            try {
                const response = await fetch("{{ url_for('play.write') }}", {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken
                    },
                    body: formData
                });
                const data = await response.json();
                if (data.message) {
                    showNotification(data.message);
                    e.target.reset();
                    closeModal('write-modal');
                } else {
                    if (data.error) {
                        showNotification(data.error);
                    } else {
                        showNotification('Error writing letter');
                    }
                }
            } catch (error) {
                console.error('Error:', error);
                if (error.response && error.response.data && error.response.data.error) {
                    showNotification(error.response.data.error);
                } else {
                    showNotification('Error writing letter');
                }
            }
        }

        // 处理读信提交
        async function handleReadSubmit(e, csrfToken) {
            e.preventDefault();
            const formData = new FormData(e.target);
            try {
                const response = await fetch("{{ url_for('play.read') }}", {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken
                    },
                    body: formData
                });
                const data = await response.json();
                const lettersList = document.getElementById('letters-list');
                lettersList.innerHTML = '';
                if (data.letters && data.letters.length > 0) {
                    data.letters.forEach(letter => {
                        const letterItem = document.createElement('div');
                        letterItem.className = 'letter-item';
                        letterItem.innerHTML = `
                            <h4>${letter.title}</h4>
                            <p>${letter.content}</p>
                        `;
                        // 添加点击事件
                        letterItem.addEventListener('click', () => {
                            const modal = document.getElementById('letter-detail-modal');
                            const modalTitle = document.getElementById('letter-modal-title');
                            const modalContent = document.getElementById('letter-modal-content');
                            modalTitle.textContent = letter.title;
                            modalContent.textContent = letter.content;
                            modal.style.display = 'flex';
                            showModal('model');
                        });
                        lettersList.appendChild(letterItem);
                    });
                } else {
                    if (data.error) {
                        lettersList.innerHTML = `<p>${data.error}</p>`;
                    } else {
                        lettersList.innerHTML = '<p>No letters found</p>';
                    }
                }
            } catch (error) {
                console.error('Error:', error);
                lettersList.innerHTML = '<p>Error loading letters</p>';
            }
        }

        // 处理地图切换
        async function handleLocationChange(e, csrfToken) {
            e.preventDefault();
            const formData = new FormData(e.target);
            try {
                const response = await fetch("{{ url_for('play.play') }}", {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken
                    },
                    body: formData
                });
                const newMapData = await response.json();
                document.getElementById('map-display').style.backgroundImage = `url('${newMapData.map_info.background_image}')`;
                document.getElementById('location-info').textContent = newMapData.map_info.address;
                // 获取音频元素
                const audioElement = document.getElementById('bg-music');
                // 获取新的音频文件路径
                const newMusicFile = newMapData.map_info.music_file;
                // 清除现有的 <source> 元素
                while (audioElement.firstChild) {
                    audioElement.removeChild(audioElement.firstChild);
                }
                // 创建新的 <source> 元素并添加到音频元素中
                const sourceMp3 = document.createElement('source');
                sourceMp3.src = newMusicFile;
                sourceMp3.type = 'audio/mpeg';
                audioElement.appendChild(sourceMp3);

                const sourceOgg = document.createElement('source');
                sourceOgg.src = newMusicFile.replace('.mp3', '.ogg');
                sourceOgg.type = 'audio/ogg';
                audioElement.appendChild(sourceOgg);

                // 尝试重新播放音频
                audioElement.load(); // 重新加载音频文件
                audioElement.play().catch(e => console.log("Autoplay prevented:", e));
                updateNPC(newMapData.map_info.npc);
                closeModal("map-selector-modal");

            } catch (error) {
                console.error('Error:', error);
                showNotification('Error changing location');
            }
        }
        function selectImageAndSubmit(box) {
            const playSelect = document.getElementById('play');
            const location_form = document.getElementById('location-form');
            playSelect.value = box.dataset.value;
            location_form.requestSubmit();
        }

// 全局变量存储当前对话状态
let currentDialogIndex = 0;
let currentNPC = null;

// 更新NPC对话框
function updateNPCScript(npc) {
    currentNPC = npc;
    currentDialogIndex = 0;
    if (npc.dialog && npc.dialog.length > 0) {
        const firstDialog = npc.dialog[0];
        const portraitA = document.getElementById('npc-portrait-A');
        portraitA.src = firstDialog.image_A || '/static/images/default_npc.png';
    }
    showCurrentDialog();
}

// 显示当前对话
function showCurrentDialog() {
    if (!currentNPC || !currentNPC.dialog || currentDialogIndex >= currentNPC.dialog.length) {
        closeModal('npc-dialog');
        return;
    }

    const dialog = currentNPC.dialog[currentDialogIndex];
    console.log('Current dialog:',dialog);
    document.getElementById('npc-dialog-text').textContent = dialog.dialog;

    // 显示A图片，隐藏B图片
    const portraitA = document.getElementById('npc-portrait-A');
    const portraitB = document.getElementById('npc-portrait-B');
    console.log('Setting image A:',dialog.image_A);
    portraitA.src = dialog.image_A;
    portraitA.style.display = 'block';
    portraitB.style.display = 'none';
}

// 下一段对话
function nextDialog() {
    if (!currentNPC || !currentNPC.dialog) return;

    currentDialogIndex++;
    if (currentDialogIndex >= currentNPC.dialog.length) {
        closeModal('npc-dialog');
        return;
    }

    const dialog = currentNPC.dialog[currentDialogIndex];
    document.getElementById('npc-dialog-text').textContent = dialog.dialog;

    // 切换图片
    const portraitA = document.getElementById('npc-portrait-A');
    const portraitB = document.getElementById('npc-portrait-B');

    if (currentDialogIndex % 2 === 0) {
        // 偶数索引显示A图片
        portraitA.src = dialog.image_A;
        portraitA.style.display = 'block';
        portraitB.style.display = 'none';
    } else {
        // 奇数索引显示B图片
        portraitB.src = dialog.image_B;
        portraitB.style.display = 'block';
        portraitA.style.display = 'none';
    }
}

// 修改showModal函数，初始化对话
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'flex';
    const modalContent = modal.querySelector('.modal-content');
    modalContent.style.animationName = 'openLetter';

    if (modalId === 'npc-dialog') {
        currentDialogIndex = 0;
        showCurrentDialog();
    }
}