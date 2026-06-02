from tools.weather import weather_tool


#查询时间测试工具
def time_tool(location):
    return f"{location}当前时间工具暂未实现真实调用。"

#简单计算测试工具
def calculator_tool(expression):
    return f"{expression}的计算工具暂未实现真实调用。"

#工具注册表
TOOL_REGISTRY = {
    "weather_tool": weather_tool,
    "time_tool": time_tool,
    "calculator_tool": calculator_tool,
}