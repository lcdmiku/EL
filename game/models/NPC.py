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


    def to_dict(self, fields=None):
        """转换为字典，包含当前对话状态"""
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "state": self.state,
            "dialogs": self.dialogs,
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