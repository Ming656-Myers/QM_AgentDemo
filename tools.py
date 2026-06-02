#测试流程用的Tool定义

#天气工具
def weather_tool(city):
    return f"{city}今天25度"

#时间工具
def time_tool(location):
    return f"{location}当前时间是上午10点"

#计算工具
def calculator_tool(expression):
    return f"{expression}的计算结果是：暂未实现真实计算"

#建立Tool Registry
#利用字典
TOOL_REGISTRY = {
    "weather_tool": weather_tool,
    "time_tool": time_tool,
    "calculator_tool": calculator_tool,
}