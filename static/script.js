async function sendMessage() {
    const input = document.getElementById("message");
    const chatbox = document.getElementById("chatbox");
  
    const userText = input.value;
    if (!userText.trim()) return;
  
    chatbox.innerHTML += `<div><b>사용자:</b> ${userText}</div>`;
    input.value = "";
  
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: userText })
    });
  
    const data = await response.json();
    chatbox.innerHTML += `<div><b>챗봇:</b> ${data.reply}</div>`;
    chatbox.scrollTop = chatbox.scrollHeight;
  }
  