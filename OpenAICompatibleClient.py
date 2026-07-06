from openai import OpenAI

class OpenAICompatibleClient:
        """
        一个用于调用任何兼容OpenAi接口的LLM服务的客户端
        """

        def __init__(self,model:str,api_key:str,base_url:str):
                self.model=model
                self.api_key=api_key
                self.base_url=base_url
                self.client=OpenAI(api_key=self.api_key,base_url=self.base_url)

        def generate(self,prompt:str,system_prompt:str)->str:
                """
                调用LLM API 生成结果
                """

                print("正在生成结果...")

                try:
                        message=[
                                {"role":"system","content":system_prompt},
                                {"role":"user","content":prompt}
                        ]
                        response=self.client.chat.completions.create(
                                model=self.model,
                                messages=message,
                                temperature=0.7,
                                max_tokens=1024,
                                stream=False
                        )

                        answer=response.choices[0].message.content
                        print("生成结果完成。")
                        return answer
                except Exception as e:
                        print(f"生成结果时发生错误: {e}")
                        return f"错误:生成结果时发生错误: {e}"








