import tcod as libtcod

import textwrap


class Message:
    def __init__(self, text, color=libtcod.white):
        self.text = text
        self.color = color


class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        # 必要に応じてメッセージを複数行に分割
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # 既にバッファがいっぱいの場合は最初の行を削除して新しい行を入れるスペースを確保
            if len(self.messages) == self.height:
                del self.messages[0]

            # 新しい行を Message オブジェクトとして追加
            self.messages.append(Message(line, message.color))