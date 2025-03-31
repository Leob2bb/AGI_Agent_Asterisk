document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("message");
  const button = document.getElementById("sendBtn");

  button.addEventListener("click", sendMessage);

  input.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  });
});

async function sendMessage() {
  const input = document.getElementById("message");
  const chatbox = document.getElementById("chatbox");

  const userText = input.value.trim();
  if (!userText) return;

  // 사용자 말풍선 추가
  const userBubble = document.createElement("div");
  userBubble.className = "bubble user";
  userBubble.textContent = userText;
  chatbox.appendChild(userBubble);

  input.value = "";

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: userText })
    });

    const data = await response.json();

    const botBubble = document.createElement("div");
    botBubble.className = "bubble bot";
    botBubble.textContent = data.reply;
    chatbox.appendChild(botBubble);
    chatbox.scrollTop = chatbox.scrollHeight;

  } catch (err) {
    console.error("서버 오류:", err);
  }
}
