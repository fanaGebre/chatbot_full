document.addEventListener("DOMContentLoaded", function () {
  const chatContainer = document.getElementById("chat-container");
  const chatbotBtn = document.getElementById("chatbot-btn");
  const closeChatBtn = document.getElementById("close-chat");
  const chatBox = document.getElementById("chat-box");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");

  // Toggle chatbot visibility
  chatbotBtn.addEventListener("click", function () {
    chatContainer.classList.toggle("hidden");
  });

  closeChatBtn.addEventListener("click", function () {
    chatContainer.classList.add("hidden");
  });

  function appendMessage(text, sender) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add(sender === "bot" ? "bot-message" : "user-message");
    msgDiv.textContent = text;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll
  }

  function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage(message, "user");
    userInput.value = "";

    fetch("/chatbot", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    })
      .then((response) => response.json())
      .then((data) => appendMessage(data.response, "bot"))
      .catch((error) =>
        appendMessage("Error: Unable to reach chatbot.", "bot")
      );
  }

  sendBtn.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") sendMessage();
  });
});
