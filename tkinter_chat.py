import tkinter as tk
from tkinter import scrolledtext
from openai import OpenAI

# --- API Client Setup ---
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key="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",  # You can replace this with your own token
)

# --- Chat Function ---
def send_prompt():
    prompt = user_input.get()
    if not prompt.strip():
        return

    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, "You: " + prompt + "\n")
    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)

    user_input.delete(0, tk.END)

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b:novita",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"[Error] {str(e)}"

    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, "Bot: " + reply + "\n\n")
    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)

# --- UI Setup ---
root = tk.Tk()
root.title("GPT-OSS Chat")

chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=25, state=tk.DISABLED)
chat_display.pack(padx=10, pady=10)

user_input = tk.Entry(root, width=70)
user_input.pack(padx=10, pady=5, side=tk.LEFT, expand=True, fill=tk.X)

send_button = tk.Button(root, text="Send", command=send_prompt)
send_button.pack(padx=10, pady=5, side=tk.RIGHT)

# Run app
root.mainloop()
