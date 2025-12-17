import base64
import os

# Function to convert local images to base64 (so they display inside HTML)
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

# Encode images once
bot_avatar = get_base64_image("AI LOGO.png")
user_avatar = get_base64_image("User.png")

css = '''
<style>
.chat-message {
    padding: 1.5rem;
    border-radius: 0.8rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: flex-start;
    backdrop-filter: blur(10px);
    background: rgba(20, 20, 20, 0.35);
    border: 1px solid rgba(0, 229, 255, 0.15);
    box-shadow: 0 0 20px rgba(0, 229, 255, 0.1);
}
.chat-message.user {
    background: rgba(45, 10, 70, 0.35);
    border: 1px solid rgba(155, 0, 255, 0.15);
}
.chat-message.bot {
    background: rgba(10, 25, 40, 0.35);
    border: 1px solid rgba(0, 229, 255, 0.15);
}
.chat-message .avatar {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    overflow: hidden;
    margin-right: 1rem;
    flex-shrink: 0;
}
.chat-message .message {
    color: #FFFFFF;
    font-family: 'Poppins', sans-serif;
    line-height: 1.5;
    font-size: 1rem;
}
</style>
'''

bot_template = f'''
<div class="chat-message bot">
    <div class="avatar">
        <img src="data:image/png;base64,{bot_avatar}" style="width: 60px; height: 60px; border-radius: 50%; box-shadow: 0 0 12px #00E5FF;">
    </div>
    <div class="message">{{{{MSG}}}}</div>
</div>
'''

user_template = f'''
<div class="chat-message user">
    <div class="avatar">
        <img src="data:image/png;base64,{user_avatar}" style="width: 60px; height: 60px; border-radius: 50%; box-shadow: 0 0 12px #9B00FF;">
    </div>
    <div class="message">{{{{MSG}}}}</div>
</div>
'''
