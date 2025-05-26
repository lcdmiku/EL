import json

class NPC:
    def __init__(self, name, image, dialogs=None, ai_api=None, state="normal"):
        self.id = None  # 这里可以根据需要生成唯一ID，暂设为None
        self.name = name
        self.image = image
        self.dialogs = dialogs or []
        self.ai_api = ai_api
        self.state = state
        self.dialog_index = 0
        self.choices = []

    def add_dialog(self, text, state=None, next_index=None):
        """添加对话条目，支持状态变化和跳转"""
        dialog = {"text": text}
        if state:
            dialog["state"] = state
        if next_index is not None:
            dialog["next_index"] = next_index
        self.dialogs.append(dialog)

    def add_choice(self, option_text, next_index):
        """添加对话选项"""
        self.choices.append({
            "option": option_text,
            "next_index": next_index
        })

    def get_current_dialog(self):
        """获取当前对话内容"""
        if 0 <= self.dialog_index < len(self.dialogs):
            return self.dialogs[self.dialog_index]
        return {"text": "（沉默）"}

    def process_choice(self, choice_index):
        """处理用户选择"""
        if 0 <= choice_index < len(self.choices):
            choice = self.choices[choice_index]
            self.dialog_index = choice["next_index"]
            self.choices = []  # 清除选项
            return self.get_current_dialog()
        return {"text": "无效的选择"}

    def next_dialog(self):
        """前进到下一个对话"""
        current = self.get_current_dialog()
        # 检查是否有指定的下一个索引
        next_index = current.get("next_index", self.dialog_index + 1)
        # 检查是否需要改变状态
        if "state" in current:
            self.state = current["state"]

        self.dialog_index = next_index
        return self.get_current_dialog()

    def reset_dialog(self):
        """重置对话状态"""
        self.dialog_index = 0
        self.choices = []

    def to_dict(self, fields=None):
        """转换为字典，包含当前对话状态"""
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "state": self.state,
            "dialog": self.dialogs,
            "choices": self.choices,
            "ai_api": self.ai_api
        }


def create_npc(name, image, dialogs=None, ai_api=None, state="normal"):
    """创建一个示例NPC"""
    npc = NPC(
        name=name,
        image=image,
        dialogs=dialogs,
        ai_api=ai_api,
        state=state
    )
    return npc