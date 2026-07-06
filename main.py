import re
import os
from OpenAICompatibleClient import OpenAICompatibleClient
from tool import available_tools


with open("system_prompt", "r", encoding="utf-8") as f:
    agent_system_prompt = f.read()



#1.配置LLM客户端
API_KEY="REDACTED"
base_url="https://api.deepseek.com/v1"
model_id="deepseek-v4-flash"
tavily_api_key="REDACTED"
os.environ["TAVILY_API_KEY"]="REDACTED"

llm=OpenAICompatibleClient(model_id,API_KEY,base_url=base_url)


#2.初始化
user_prompt="你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。"
prompt_history=[f"用户: {user_prompt}"]

print(f"用户输入: {user_prompt}\n"+"="*40)

#3.运行主程序
for i in range(3):
    print(f"---循环{i+1}---")

    #3.1构建prompt
    full_prompt="\n".join(prompt_history)

    #3.2调用LLM生成响应
    llm_output=llm.generate(full_prompt,system_prompt=agent_system_prompt)

    #模型可能会输出多余的thought-action，截断只保留第一对
    match=re.search(r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought|Action:|Observation:)|\Z)',llm_output,re.DOTALL|re.IGNORECASE)
    if match:
        truncated=match.group(1).strip()
        if truncated !=llm_output.strip():
            llm_output=truncated
            print("已截断多余的thought-action部分。")

    print(f"模型输出:\n{llm_output}\n")

    #3.3解析并执行行动
    action_match=re.search(r"Action:\s*([^\n]*)",llm_output)
    if action_match:
        action_str=action_match.group(1).strip()

        #检查是否是结束标记
        if action_str.startswith("Finish["):
            final_answer=action_str[len("Finish["):-1]
            print(f"任务完成，最终答案: {final_answer}")
            break

        #尝试解析函数调用: function_name(arg_name="arg_value",...)
        func_match=re.match(r"(\w+)\((.*)\)",action_str)
        if func_match:
            tool_name=func_match.group(1)
            args_str=func_match.group(2)

            kwargs={}
            if args_str.strip():
                for pair in args_str.split(","):
                    pair=pair.strip()
                    if "=" in pair:
                        key,value=pair.split("=",1)
                        key=key.strip()
                        value=value.strip().strip('"').strip("'")
                        kwargs[key]=value

            if tool_name in available_tools:
                observation=available_tools[tool_name](**kwargs)
            else:
                observation=f"错误：未定义的工具'{tool_name}'"
        else:
            observation=f"错误：无法解析Action格式，期望 function_name(arg=\"value\") 或 Finish[答案]。"
    else:
        #模型未输出Action，不追加乱输出到历史，只给纠正提示
        observation="错误：请严格按照 Thought: ... 和 Action: ... 格式输出。"

    #3.4记录历史
    prompt_history.append(llm_output)
    observation_str=f"Observation: {observation}"
    print(f"{observation_str}\n"+"="*40)
    prompt_history.append(observation_str)
