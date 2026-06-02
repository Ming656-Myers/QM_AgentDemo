import llm_client
import system_prompts
import tool_prompts
import chat
import tools

#创建一个OpenAI client对象
client = llm_client.create_client()
print("\n欢迎使用QM_AgentDemo!（输入'Q'或'q'结束对话）\n")

#保存对话历史，添加系统信息
messages = [
    {
        #role表示消息角色，system表示系统消息；#content表示消息内容，即给系统拟定的前提条件
        "role":"system",
        "content":system_prompts.SYSTEM_PROMPT
    }
]

#向大模型开启循环对话请求
while True:

    #获取用户输入
    user_input = input("你：")

    #程序结束条件
    if user_input.lower() in['Q', 'q']:
        print("对话结束")
        break
    
    #decision_messages不能复制messages的内容。工具决策要作为一个独立的任务，只看当前用户的输入，不看历史对话
    #1.先单独做LLM工具决策
    decision_messages = [
        {
            "role":"system",
            "content":tool_prompts.TOOL_PROMPT
        },
        {
            "role":"user",
            "content":user_input
        }
    ]

    #获取LLM返回的结果
    decision_reply = chat.chat_with_llm(client, decision_messages)
    decision_reply = decision_reply.strip()

    #2.将用户输入加入到正式聊天历史
    messages.append({
        #role表示消息角色，user表示用户输入；#content表示消息内容，即用户真正说的话
        "role": "user",
        "content": user_input
    })

    #3.判断是否调用工具
    #调用工具
    if decision_reply.startswith("TOOL:"):
        
        #提取参数
        lines = decision_reply.split("\n")
        tool_name = lines[0].replace("TOOL:", "").strip()
        args = lines[1].replace("ARGS:", "").strip()

        if tool_name == "weather_tool":
            
            #这里的tool_replay是Python执行Tool后返回的结果，不是LLM返回的结果
            tool_reply = tools.weather_tool(args)
            
            #observation_messages复制messages的内容
            observation_messages = messages.copy()

            #将LLM上一轮的决策结果添加到observation_messages中
            observation_messages.append({
                "role":"assistant",
                "content":decision_reply
            })

            #向observation_messages中添加build_observation_prompt
            observation_messages.append({
                "role":"user",
                "content":system_prompts.build_observation_prompt(tool_reply)
            })

            final_reply = chat.chat_with_llm(client, observation_messages)
            print(f"模型回复：{final_reply}\n")

            #将LLM回复也加入到对话历史
            messages.append({
                "role": "assistant",
                "content": final_reply
            })
    
    #不调用工具
    elif decision_reply == "NO_TOOL":
        
        final_reply = chat.chat_with_llm(client, messages)
        
        #这里的final_reply才是LLM返回的结果
        print(f"模型回复：{final_reply}\n")
        #将LLM回复也加入到对话历史
        messages.append({
            "role": "assistant",
            "content": final_reply
        })

    #第一次LLM工具决策输出格式错误
    else:

        print(f"工具决策输出格式错误：{decision_reply}\n")