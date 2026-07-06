import os
from tavily import TavilyClient

def get_attraction(city:str,weather:str)->str:
        """
        根据城市和天气，使用Tavily Search API 搜索并返回优化后的旅游景点信息。
        """
        #1.从环境变量中获取Tavily API密钥
        api_key=os.environ.get("TAVILY_API_KEY")
        if not api_key:
                return "错误：未设置Tavily API密钥，请在环境变量中设置TAVILY_API_KEY。"
        
        #2.创建Tavily客户端
        tavily=TavilyClient(api_key=api_key)

        #3.构建一个精确的查询，要求中文结果
        query=f"{city}在{weather}天气下最值得去的景点推荐及理由，请用中文回答"

        try:
                #4.调用API，include_answer=True会返回一个综合性的回答
                response=tavily.search(query=query,search_depth="basic",include_answer=True)

                #5.Tavily返回的结果已经非常干净，可以直接使用
                #response['answer']是一个基于所有搜搜结果的总结性答案
                if response['answer']:
                        return response['answer']
                
                formatted_results=[]
                for result in response.get("results", []):
                        formatted_results.append(f"-{result['title']}:{result['content']}")

                if not formatted_results:
                        return "未找到相关景点信息。"
                
                return "根据搜索，为您找到以下信息：\n" + "\n".join(formatted_results)
        
        except Exception as e:
                return f"错误:执行Tavily搜索时出现问题: {e}"








