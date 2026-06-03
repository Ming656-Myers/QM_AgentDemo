import streamlit as st

import chat
import config
import llm_client
from prompts.system_prompts import SYSTEM_PROMPT, build_observation_prompt
from prompts.tool_prompts import TOOL_PROMPT
from tools.registry import TOOL_REGISTRY


st.set_page_config(
    page_title="QM_AgentDemo",
    page_icon="QM",
    layout="wide",
)


def init_messages():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]


def reset_messages():
    st.session_state.messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]


def build_tool_decision_messages(user_input):
    return [
        {
            "role": "system",
            "content": TOOL_PROMPT,
        },
        {
            "role": "user",
            "content": user_input,
        },
    ]


def parse_tool_decision(decision_reply):
    lines = decision_reply.split("\n")

    if len(lines) < 2:
        return None, None

    tool_name = lines[0].replace("TOOL:", "").strip()
    args = lines[1].replace("ARGS:", "").strip()

    return tool_name, args


def call_agent(client, user_input, model_name):
    decision_reply = chat.chat_with_llm(
        client,
        build_tool_decision_messages(user_input),
        model_name=model_name,
    ).strip()

    if decision_reply.startswith("TOOL:"):
        tool_name, args = parse_tool_decision(decision_reply)

        if tool_name not in TOOL_REGISTRY:
            return f"未注册的工具：{tool_name}"

        tool_reply = TOOL_REGISTRY[tool_name](args)
        observation_messages = st.session_state.messages.copy()
        observation_messages.append(
            {
                "role": "assistant",
                "content": decision_reply,
            }
        )
        observation_messages.append(
            {
                "role": "user",
                "content": build_observation_prompt(tool_reply),
            }
        )

        return chat.chat_with_llm(
            client,
            observation_messages,
            model_name=model_name,
        )

    if decision_reply == "NO_TOOL":
        return chat.chat_with_llm(
            client,
            st.session_state.messages,
            model_name=model_name,
        )

    return f"工具决策输出格式错误：{decision_reply}"


init_messages()

with st.sidebar:
    st.header("API 配置")
    api_key = st.text_input("API Key", type="password")
    base_url = st.text_input("Base URL", value=config.BASE_URL)
    model_name = st.text_input("模型名称", value=config.MODEL_NAME)

    st.divider()
    if st.button("清空对话记录", use_container_width=True):
        reset_messages()
        st.rerun()

st.title("QM_AgentDemo")
st.caption("Web 版 Agent 基础调用页面")

for message in st.session_state.messages:
    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("请输入你的问题或论文写作材料")

if user_input:
    if not api_key:
        st.error("请先在左侧填写 API Key。")
        st.stop()

    user_message = {
        "role": "user",
        "content": user_input,
    }
    st.session_state.messages.append(user_message)

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("模型正在生成回复..."):
            try:
                client = llm_client.create_client(
                    api_key=api_key,
                    base_url=base_url,
                )
                reply = call_agent(
                    client,
                    user_input,
                    model_name,
                )
            except Exception as exc:
                st.error(f"模型调用失败：{exc}")
                st.stop()

        st.markdown(reply)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply,
        }
    )
