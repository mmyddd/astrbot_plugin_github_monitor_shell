"""文本工具：长文本截断与消息分片

QQ（OneBot/NapCat/Lagrange 等实现）对单条文本消息长度有限制，
内容过长会导致整条消息发送失败，因此提供截断与分片两个工具。
"""

from typing import List


def truncate_text(text: str, max_length: int, suffix: str = "\n…（内容过长，已截断）") -> str:
    """按最大字符数截断文本，超出时附加提示后缀"""
    text = (text or "").strip()
    if max_length <= 0 or len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + suffix


def split_long_message(text: str, max_length: int) -> List[str]:
    """把超长文本拆分为多条不超过 max_length 的消息

    优先按换行边界拆分，保持段落完整；单行超过 max_length 时硬切。
    输入不超过限制时原样返回单元素列表。
    """
    text = (text or "").strip("\n")
    if max_length <= 0 or len(text) <= max_length:
        return [text] if text else [""]

    chunks: List[str] = []
    current = ""
    for line in text.split("\n"):
        # 单行超长时先硬切
        while len(line) > max_length:
            if current:
                chunks.append(current)
                current = ""
            chunks.append(line[:max_length])
            line = line[max_length:]
        candidate = f"{current}\n{line}" if current else line
        if len(candidate) <= max_length:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = line
    if current:
        chunks.append(current)
    return chunks
