import os
import google.generativeai as genai

# 获取环境变量
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_KEY:
    print("❌ 错误：没有找到 API Key！")
else:
    print(f"✅ 找到 API Key: {GEMINI_KEY[:5]}******")
    
    # 配置 API
    genai.configure(api_key=GEMINI_KEY)

    print("\n🔍 正在查询可用模型列表...\n")
    try:
        # 列出所有模型
        for m in genai.list_models():
            # 我们只关心能生成文本的模型 (generateContent)
            if 'generateContent' in m.supported_generation_methods:
                print(f"👉 发现模型: {m.name}")
    except Exception as e:
        print(f"❌ 查询失败，原因: {e}")
