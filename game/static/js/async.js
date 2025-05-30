 // 统一处理 fetch 请求错误
        async function handleFetch(url, options) {
            try {
                const response = await fetch(url, options);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return await response.json();
            } catch (error) {
                console.error('Error:', error);
                showNotification('Network error or server error');
                return null;
            }
        }

        // 处理收集信件
        async function handleCollect(e, csrfToken) {
            e.preventDefault();
            const data = await handleFetch(window.urlConfig.collect, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                }
            });
            if (data) {
                if (data.message) {
                    if (data.letter) {
                        const modal = document.getElementById('letter-detail-modal');
                        const modalTitle = document.getElementById('letter-modal-title');
                        const modalContent = document.getElementById('letter-modal-content');
                        // 处理回信
                        const modalReplyButton = document.getElementById('reply-button');
                        modalReplyButton.removeEventListener('click', modalReplyButton.clickHandler);
                        modalReplyButton.clickHandler = () => replyToLetter(data.letter.writer_id);
                        modalReplyButton.addEventListener('click', modalReplyButton.clickHandler);
                        //
                        modalTitle.textContent = data.letter.title;
                        modalContent.textContent = data.letter.content;
                        //sound effect
                        SoundEffect('letter-send-effect');
                        showModal('letter-detail-modal');
                    }
                    showNotification(data.message);
                } else if (data.error) {
                    showNotification(data.error);
                }
            }
        }

        // 处理写信提交
        async function handleWriteSubmit(e, csrfToken) {
            e.preventDefault();
            console.log("Writing to server");
            const formData = new FormData(e.target);
            // 处理回信
            const replyToId = document.getElementById('reply-to-id').value;
            if (replyToId) {
                formData.append('reply_to_id', replyToId);
                document.getElementById('reply-to-id').value = null;//回信后，清空reply对象
            } else {
                formData.append('reply_to_id', null);
            }
            const data = await handleFetch(window.urlConfig.write, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            });
            if (data) {
                if (data.message) {
                    showNotification(data.message);
                     //动画与音效果
                    if (data.message!=='Can not reply to yourself'){SoundEffect('letter-send-effect');}
                    e.target.reset();
                    closeModal('write-modal');
                } else {
                    if (data.error) {
                        showNotification(data.error);
                    } else {
                        showNotification('Error writing letter');
                    }
                }
            }
        }

        // 处理回信
        function replyToLetter(replyToId) {
            document.getElementById('reply-to-id').value = replyToId;
            showModal('write-modal');
        }

        // 处理读信提交
        async function handleReadSubmit(e, csrfToken) {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = await handleFetch(window.urlConfig.read, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            });
            const lettersList = document.getElementById('letters-list');
            lettersList.innerHTML = '';
            if (data) {
                if (data.letters && data.letters.length > 0) {
                    data.letters.forEach(letter => {
                        const letterItem = document.createElement('div');
                        letterItem.className = 'letter-item';
                        letterItem.innerHTML = `
                            <h4>${letter.title}</h4>
                            <div class="red_dot"></div>

                            <p class="emo-type" style="font-size: 1.6em" >${letter.type}</p>

                        `;
                        //处理不同emo-type的style
                        const emoTypeElement = letterItem.querySelector('.emo-type');
                            switch(letter.type) {
                                case 'happy':
                                    emoTypeElement.style.color = 'rgb(244,143,52)';// 橙色
                                    break;
                                case 'sad':
                                    emoTypeElement.style.color = '#8eb2ef'; // 蓝色
                                    break;
                                case 'suggestion':
                                    emoTypeElement.style.color = 'rgba(44,244,131)';//青色
                                    break;
                                default:
                                    emoTypeElement.style.color = '#d0eeff';
                                    break;
                            }
                        //
                        letterItem.addEventListener('mouseenter', function () {
                            letterItem.style.backgroundColor = emoTypeElement.style.color;
                        });
                        letterItem.addEventListener('mouseleave', function ()  {
                            letterItem.style.backgroundColor = '#f5f5f5';
                        });

                        //处理未读信息
                        const RedDot = letterItem.querySelector('.red_dot');
                        if(letter.Is_viewed === false){
                            RedDot.style.display = 'flex';
                        }
                        // 添加点击事件
                        letterItem.addEventListener('click', () => {
                            const modal = document.getElementById('letter-detail-modal');
                            const modalTitle = document.getElementById('letter-modal-title');
                            const modalContent = document.getElementById('letter-modal-content');
                            // 处理回信
                            const modalReplyButton = document.getElementById('reply-button');
                            modalReplyButton.removeEventListener('click', modalReplyButton.clickHandler);
                            modalReplyButton.clickHandler = () => replyToLetter(letter.writer_id);
                            modalReplyButton.addEventListener('click', modalReplyButton.clickHandler);
                            //
                            modalTitle.textContent = letter.title;
                            modalContent.textContent = letter.content;
                            //处理没读信件
                            if (letter.Is_viewed === false) {
                                RedDot.style.display = 'none';
                                console.log(letter.id);
                                markLetterAsRead(letter.id, csrfToken);
                            }

                            showModal('letter-detail-modal');
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
            }
        }

        // 标记信件为已读
        async function markLetterAsRead(letterId, csrfToken) {
          const response = await handleFetch(window.urlConfig.Is_viewed, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ letterId })
          });

          if (!response.ok) {
            throw new Error('标记信件已读失败');
          }

          return response;
        }

        // 处理地图切换
        async function handleLocationChange(e, csrfToken) {
            e.preventDefault();
            const formData = new FormData(e.target);
            const newMapData = await handleFetch(window.urlConfig.play, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            });
            if (newMapData) {
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
                //NPC
                updateNPC(newMapData.map_info.npc);
                closeModal("map-selector-modal");
            }
        }