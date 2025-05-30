// 初始化游戏
        document.addEventListener('mousemove', function() {
            // 自动播放背景音乐
            const bgMusic = document.getElementById('bg-music');
            bgMusic.play().catch(e => {
               console.log(e);
            });
        });
        document.addEventListener('DOMContentLoaded', function () {
            const csrfToken = document.querySelector('input[name="csrf_token"]').value;
            // 显示当前位置3秒
            showLocationInfo();

            // 绑定按钮事件
            document.getElementById('collect-btn').addEventListener('click', function (e) {
                handleCollect(e, csrfToken);
            });
            document.getElementById('next-dialog-btn').addEventListener('click', nextDialog);
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
            const npcData = JSON.parse(document.getElementById('npc-data').textContent);
            updateNPC(npcData);
        });

        // 显示位置信息3秒
        function showLocationInfo() {
            const locationInfo = document.getElementById('location-info');
            locationInfo.style.opacity = '1';
            setTimeout(() => {
                locationInfo.style.opacity = '0';
            }, 1000);
        }

        //按键音效
        function SoundEffect(AudioId) {
            const BtnSound = document.getElementById(AudioId);
            BtnSound.play();
        }



        // 关闭模态框
        function closeModal(modalId) {
            SoundEffect('btn-sound-effect');
            document.getElementById(modalId).style.display = 'none';
        }

        // 显示通知消息
        function showNotification(message, duration = 3000) {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.style.animationName = 'openLetter';
            notification.style.display = 'block';
            setTimeout(() => {
                notification.style.display = 'none';
            }, duration);
        }

        //切换地图by点击场景图
        function selectImageAndSubmit(box) {
            const playSelect = document.getElementById('play');
            const location_form = document.getElementById('location-form');
            playSelect.value = box.dataset.value;
            location_form.requestSubmit();
            //sound effect
            const AddressChangeSound = document.getElementById('address-change-sound');
            AddressChangeSound.play();
            showLocationInfo();
        }
        //NPC
        function updateNPC(npc){
            document.querySelector('#npc img').src = npc.image;
            document.querySelector('#npc img').alt = npc.image;
            document.querySelector('#npc-dialog h3').textContent = npc.name;
            document.querySelector('#npc-dialog-text').textContent = npc.dialog;
            document.querySelector('.npc-portrait-A').src = npc.image;
            document.querySelector('.npc-portrait-B').src = npc.image;
            document.querySelector('.npc-portrait-A').alt = npc.name;
            document.querySelector('.npc-portrait-B').alt = npc.name;
            updateNPCScript(npc);
        }