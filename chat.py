#对话文件
#用户向LLM发送一次对话请求，LLM返回一次回答
import config

def chat_with_llm(client, messages):
    #使用client这个客户端，在它的聊天补全功能中，创建一个新的请求
    response = client.chat.completions.create(
        #指定使用的模型，DeepSeek-V3.2是模型名称
        model=config.MODEL_NAME,

        #messages表示对话历史，传入的messages是一个列表
        messages=messages
    )
    
    #返回llm的回答。response是完整返回结果；choices[0]表示第一个回答；message.content表示回答文本
    return response.choices[0].message.content