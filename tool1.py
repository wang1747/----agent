import requests

def get_weather(city:str)->str:
        """
        通过调用 wttr.in API 获取指定城市的天气信息。
        """
        #API端点，我们请求JSON格式的数据
        url =f"https://wttr.in/{city}?format=j1"

        try:
                #发起请求
                response = requests.get(url)
                #检查响应状态码
                response.raise_for_status()
                #解析JSON数据
                data = response.json()
                #获取天气信息
                current_condition = data['current_condition'][0]
                weather_desc = current_condition['weatherDesc'][0]['value']
                temperature = current_condition['temp_C']

                return f"{city}的当前天气: {weather_desc}, 温度: {temperature}°C"

        except requests.RequestException as e:
                #处理网络错误
                return f"错误：查询天气信息时发生网络错误: {e}"
        
        except (KeyError, IndexError) as e:
                #处理数据解析错误
                return f"错误：解析天气数据失败，可能是城市名称无效: {e}"
        
        









