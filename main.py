import re
import os
import OpenAICompatibleClient




#1.配置LLM客户端
API_KEY="REDACTED"
base_url="https://api.deepai.com/v1"
model_id="deepseek-chat-3.5"
tavily_api_key="REDACTED"
os.environ["Tavily_API_KEY"]="REDACTED"

llm=OpenAICompatibleClient(model_id,API_KEY,base_url=base_url)

#2.初始化
user_prompt="你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。"
prompt_history=[f"用户: {user_prompt}"]

print(f"用户输入: {user_prompt}\n"+"="*40)

#3.运行主程序
for i in range(5):  #设置最大循环次数
        print(f"---循环{i+1}---\n")

        #3.1构建prompt
        full_prompt="\n".join(prompt_history)

        #3.2调用LLM生成响应
        llm_output=llm.generate(full_prompt,system_prompt=agent_system_prompt)

        #模型可能会输出多余的thought-action,需要截断
        match=re.search(r'(Thought:.*?Action:.*?)(?=\n\s*(?:thought|action:|observation:)|\z)',llm_output,re.DOTALL|re.DOTALL)

        if match:
                truncated=match.group(1).strip()
                if truncated !=llm_output.strip():
                        llm_output=truncated
                        print("已截断多余的thought-action部分。")

                print(f"模型输出:\n{llm_output}\n")
                prompt_history.append(llm_output)

                #3.3解析并执行行动
                action_match=re.search(r"Action:(.*?)",llm_output,re.DOTALL)
                if not action_match:
                        observation=
                        



