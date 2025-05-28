        // 初始化游
        document.addEventListener('DOMContentLoaded', function () {
            // 绑定按钮事件
            document.getElementById('next-dialog-btn').addEventListener('click', nextDialog);
        });
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
    document.getElementById('npc-dialog-text').textContent = dialog.dialog;

    // 显示A图片和名字，隐藏B图片
    const portraitA = document.getElementById('npc-portrait-A');
    const portraitB = document.getElementById('npc-portrait-B');
    const npcName = document.getElementById('npc-name');
    portraitA.src = dialog.image_A;
    portraitA.style.display = 'block';
    portraitB.style.display = 'none';
    npcName.textContent = dialog.name_A || currentNPC.name;
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

    // 切换图片和名字
    const portraitA = document.getElementById('npc-portrait-A');
    const portraitB = document.getElementById('npc-portrait-B');
    const npcName = document.getElementById('npc-name');

    if (currentDialogIndex % 2 === 0) {
        // 偶数索引显示A图片和名字
        portraitA.src = dialog.image_A;
        portraitA.style.display = 'block';
        portraitB.style.display = 'none';
        npcName.textContent = dialog.name_A || currentNPC.name;
    } else {
        // 奇数索引显示B图片和名字
        portraitB.src = dialog.image_B;
        portraitB.style.display = 'block';
        portraitA.style.display = 'none';
        npcName.textContent = dialog.name_B || currentNPC.name;
    }
}

// 修改showModal函数，初始化对话
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'flex';
    const modalContent = modal.querySelector('.modal-content');
    modalContent.style.animationName = 'openLetter';
    //按键音效
    const BtnSound = document.getElementById('btn-sound-effect');
    BtnSound.play();
    if (modalId === 'npc-dialog') {
        currentDialogIndex = 0;
        showCurrentDialog();
    }
    if (modalId === 'letter-detail-modal' || modalId === 'write-modal') {
        const LetterSound = document.getElementById('letter-sound-effect');
        LetterSound.play();
    }

}