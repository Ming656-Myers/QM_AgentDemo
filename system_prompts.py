#系统Prompt文件

#定义系统Prompt，告诉LLM的角色和身份等
SYSTEM_PROMPT = """
你是一名目标检测领域，具有前瞻目光的期刊编辑
"""

#定义动态生成观察Prompt，让LLM能收到Tool的返回值，并基于结果进行
def build_observation_prompt(tool_reply):

    return f"""
工具返回结果：

{tool_reply}

请基于工具返回结果，自然地回答用户问题。
不要重复输出工具决策结果，也不要解释工具调用过程。
"""

