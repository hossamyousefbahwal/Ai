import sys
import codecs
# إجبار بايثون على اعتماد الترميز العالمي للعربية لمنع أخطاء الـ ASCII
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

import os
from flask import Flask, request, jsonify
from  google import genai


app = Flask(__name__)

# 🔑 ضع مفتاح الـ API المجاني الخاص بك من Google AI Studio هنا
os.environ["GEMINI_API_KEY"] = "AQ.Ab8RN6I0TcNT6vnYTE5Qv2_bD9R5ghPTs3frq1hOf8oTEzEVtA"

# 🤖 مسار استقبال أسئلة الذكاء الاصطناعي من الويب (يدعم اللغة العربية)
@app.route('/ask-ai', methods=['POST'])
def ask_ai():
    request_data = request.get_json(force=True)
    user_message = request_data.get('message', '')
    
    if not user_message:
        return jsonify({"response": "يوسف يا عبد اكتب سؤال وعجل عشان ماني فاضيلك"})
    
    try:
        # الاتصال بذكاء قوقل الاصطناعي
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=user_message,
        )
        
        # إرجاع الإجابة مع دعم الترميز العربي
        return app.response_class(
            response=jsonify({"response": response.text}).get_data(),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        error_msg = str(e).encode('utf-8', errors='ignore').decode('utf-8')
        return jsonify({"response": f"حدث خطأ في الاتصال بالذكاء الاصطناعي: {error_msg}"})

# المسار الرئيسي للموقع (واجهة شات ذكية وصافية)
@app.route('/')
def home():
    return f"""
    <div style="text-align: center; margin-top: 50px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; direction: rtl; max-width: 600px; margin-left: auto; margin-right: auto; padding: 20px;">
        <h1 style="color: #2b6cb0; margin-bottom: 30px;">المساعد حق حسام بس يا يوسف تفهم🤖☁️</h1>
        
        <!-- 🧠 قسم الشات المتطور -->
        <div style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; background: #ffffff; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05); margin-bottom: 30px;">
            <div id="chat-box" style="height: 350px; border: 1px solid #edf2f7; border-radius: 8px; overflow-y: auto; padding: 15px; text-align: right; background: #f7fafc; margin-bottom: 15px; border-bottom: 3px solid #319795;">
                <p style="color: #a0aec0; margin: 0; text-align: center; padding-top: 150px;">مرحباً بك! اسألني عن أي شيء وسأجيبك فوراً...</p>
            </div>
            <div style="display: flex; gap: 10px;">
                <input type="text" id="user-msg" placeholder="اكتب سؤالك هنا..." onkeypress="handleKeyPress(event)" style="padding: 12px; width: 80%; border: 1px solid #cbd5e0; border-radius: 6px; font-size: 16px; outline: none;">
                <button onclick="sendMessage()" style="padding: 12px; background: #319795; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; width: 20%; font-weight: bold; transition: 0.2s;">إرسال</button>
            </div>
        </div>
        
    </div>

    <!-- 📜 كود جافاسكريبت المحدث للدردشة التفاعلية -->
    <script>
    function handleKeyPress(event) {{
        if (event.key === 'Enter') {{
            sendMessage();
        }}
    }}

    async function sendMessage() {{
        const input = document.getElementById('user-msg');
        const chatBox = document.getElementById('chat-box');
        const msg = input.value.trim();
        if(!msg) return;

        if (chatBox.innerHTML.includes('مرحباً بك!')) {{
            chatBox.innerHTML = '';
        }}

        chatBox.innerHTML += `<div style="margin-bottom: 15px; text-align: right;"><b>👤 أنت:</b><div style="background: #edf2f7; display: inline-block; padding: 10px 15px; border-radius: 8px; margin-top: 5px; max-width: 85%; white-space: pre-line;">${{msg}}</div></div>`;
        input.value = '';
        chatBox.scrollTop = chatBox.scrollHeight;

        const loadingId = 'loading-' + Date.now();
        chatBox.innerHTML += `<div id="${{loadingId}}" style="color: gray; margin-bottom: 15px;">🤖 جاري التفكير...</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;

        const response = await fetch('/ask-ai', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{ message: msg }})
        }});
        const data = await response.json();
        
        document.getElementById(loadingId).remove();
        chatBox.innerHTML += `<div style="margin-bottom: 15px; text-align: right;"><b style="color: #2b6cb0;">🤖 المساعد الذكي:</b><div style="background: #ebf8ff; color: #2b6cb0; display: inline-block; padding: 10px 15px; border-radius: 8px; margin-top: 5px; max-width: 85%; white-space: pre-line;">${{data.response}}</div></div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    }}
    </script>
    """

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
