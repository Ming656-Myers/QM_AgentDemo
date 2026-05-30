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
        "role": "system",
        "content": system_prompts.SYSTEM_PROMPT
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
    
    #添加用户信息
    messages.append({
        #role表示消息角色，user表示用户输入；#content表示消息内容，即用户真正说的话
        "role": "user",
        "content": user_input
    })
    
    #decision_messages复制messages的内容
    decision_messages = messages.copy()
    #向decision_messages中添加TOOL_PROMPT
    decision_messages.append({
        "role":"system",
        "content":tool_prompts.TOOL_PROMPT
    })

    #获取LLM返回的结果
    agent_reply = chat.chat_with_llm(client, decision_messages)

    #判断是否调用工具
    if "TOOL:" in agent_reply:
        
        #提取参数
        lines = agent_reply.split("\n")
        tool_name = lines[0].replace("TOOL:", "").strip()
        args = lines[1].replace("ARGS:", "").strip()

        if tool_name == "weather_tool":
            
            #这里的tool_replay是Python执行Tool后返回的结果，不是LLM返回的结果
            tool_reply = tools.weather_tool(args)
            
            #observation_messages复制messages的内容
            observation_messages = messages.copy()
            #向observation_messages中添加build_observation_prompt
            observation_messages.append({
                "role":"system",
                "content":system_prompts.build_observation_prompt(tool_reply)
            })

            final_reply = chat.chat_with_llm(client, observation_messages)
            print(f"模型回复：{final_reply}\n")

            #将LLM回复也加入到对话历史
            messages.append({
                "role": "assistant",
                "content": final_reply
            })
    
    else:
        
        #这里的agent_reply才是LLM返回的结果
        print(f"模型回复：{agent_reply}\n")
        #将LLM回复也加入到对话历史
        messages.append({
            "role": "assistant",
            "content": agent_reply
        })