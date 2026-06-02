from urllib.parse import urlencode
from tools.common import get_json


#天气编码转文本
def weather_code_to_text(code):
    weather_map = {
        0: "晴",
        1: "大致晴朗",
        2: "局部多云",
        3: "阴",
        45: "雾",
        48: "霜雾",
        51: "小毛毛雨",
        53: "中等毛毛雨",
        55: "大毛毛雨",
        61: "小雨",
        63: "中雨",
        65: "大雨",
        71: "小雪",
        73: "中雪",
        75: "大雪",
        80: "小阵雨",
        81: "中等阵雨",
        82: "强阵雨",
        95: "雷暴",
    }
    return weather_map.get(code, f"未知天气代码 {code}")

#查询天气工具
def weather_tool(city):
    city = city.strip()

    if not city:
        return "天气查询失败：城市名为空。"

    geocoding_params = urlencode({
        "name": city,
        "count": 1,
        "language": "zh",
        "format": "json",
    })

    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?{geocoding_params}"
    geocoding_data = get_json(geocoding_url)

    results = geocoding_data.get("results")
    if not results:
        return f"天气查询失败：没有找到城市“{city}”。"

    location = results[0]
    latitude = location["latitude"]
    longitude = location["longitude"]
    resolved_name = location.get("name", city)

    weather_params = urlencode({
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,apparent_temperature,weather_code,wind_speed_10m",
    })

    weather_url = f"https://api.open-meteo.com/v1/forecast?{weather_params}"
    weather_data = get_json(weather_url)

    current = weather_data.get("current")
    if not current:
        return f"天气查询失败：没有获取到“{resolved_name}”的当前天气。"

    temperature = current["temperature_2m"]
    apparent_temperature = current["apparent_temperature"]
    weather_text = weather_code_to_text(current["weather_code"])
    wind_speed = current["wind_speed_10m"]

    return (
        f"{resolved_name}当前天气："
        f"温度 {temperature}°C,"
        f"体感温度 {apparent_temperature}°C,"
        f"天气：{weather_text},"
        f"风速 {wind_speed} km/h。"
    )