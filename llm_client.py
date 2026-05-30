#LLM客户端文件
#创建一个OpenAI client对象，后续所有的大模型请求都通过client发送
from openai import OpenAI
from dotenv import load_dotenv
import config
import os

#读取当前目录下的.env文件，会把.env中的内容加载到环境变量中
load_dotenv()

def create_client():

    client = OpenAI(
        #从环境变量中读取API Key
        api_key=os.getenv(config.API_KEY_ENV),
        #设置请求的基础URL，默认是https://api.openai.com/v1。如果使用的是SiliconFlow的API，需要修改为https://api.siliconflow.cn/v1
        base_url=config.BASE_URL
    )

    return client