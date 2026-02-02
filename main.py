import os
import smtplib
import google.generativeai as genai
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# 1. 获取环境变量
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")

# 接收邮件的人（通常发给自己）
TO_EMAIL = GMAIL_USER 

def get_ai_response():
    print("正在让 Gemini 写邮件...")
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # 我们要求 AI 直接生成 HTML 格式，这样邮件里可以有标题、加粗和列表
    prompt = """
    请扮演一个私人助理，给我写一份【每日早报】。
    
    要求：
    1. 内容包含：日期问候、一条国际新闻摘要、一条励志名言、一个生活小建议。
    2. 【关键】：请直接输出 HTML 代码。
       - 使用 <h2> 作为小标题。
       - 使用 <p> 作为正文。
       - 使用 <ul> 和 <li> 来列出要点。
       - 整体风格要简洁、现代。
       - 不要包含 ```html 这种 markdown 标记，只给我纯 HTML 代码。
    """
    
    try:
        response = model.generate_content(prompt)
        # 清理一下可能存在的 markdown 标记
        clean_text = response.text.replace("```html", "").replace("```", "")
        return clean_text
    except Exception as e:
        return f"<p>AI 生成出错: {str(e)}</p>"

def send_email(html_content):
    print("正在连接 Gmail 服务器...")
    
    # 1. 构建邮件对象
    msg = MIMEMultipart()
    msg['From'] = Header(f"Gemini AI <{GMAIL_USER}>", 'utf-8')
    msg['To'] = Header("主人", 'utf-8')
    msg['Subject'] = Header("📅 你的 Gemini 每日早报", 'utf-8')
    
    # 2. 附加 HTML 内容
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    
    try:
        # 3. 连接 Gmail SMTP 服务器 (SSL 端口 465)
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, [TO_EMAIL], msg.as_string())
        server.quit()
        print("✅ 邮件发送成功！")
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")

if __name__ == "__main__":
    if not GEMINI_KEY or not GMAIL_USER or not GMAIL_PASSWORD:
        print("❌ 错误：GitHub Secrets 缺少 GMAIL_USER 或 GMAIL_PASSWORD")
    else:
        ai_html = get_ai_response()
        send_email(ai_html)
