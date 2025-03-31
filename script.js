document.addEventListener("DOMContentLoaded", () => {
  // 전송 버튼 클릭 시
  document.getElementById("sendBtn").addEventListener("click", sendMessage);

  // 엔터 키 누를 때도 전송되도록
  document.getElementById("message").addEventListener("keypress", function (e) {
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

  // 서버로 메시지 보내기
  const response = await fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message: userText })
  });

  const data = await response.json();

  // 챗봇 말풍선 추가
  const botBubble = document.createElement("div");
  botBubble.className = "bubble bot";
  botBubble.textContent = data.reply;
  chatbox.appendChild(botBubble);

  // 스크롤 아래로
  chatbox.scrollTop = chatbox.scrollHeight;
}
