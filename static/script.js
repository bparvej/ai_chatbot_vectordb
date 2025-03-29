function sendMessage() {
    let userInput = document.getElementById("user-input");
    let chatBox = document.getElementById("chat-box");
    let query = userInput.value.trim();

    if (query === "") return;

    // Display user message
    let userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.textContent = query;
    chatBox.appendChild(userMessage);

    // Clear input
    userInput.value = "";
    
    // Send request to Flask backend
    fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        // Display bot response
        let botMessage = document.createElement("div");
        botMessage.className = "bot-message";
        botMessage.textContent = data.response;
        chatBox.appendChild(botMessage);

        // Auto-scroll to the latest message
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => console.error("Error:", error));
}

// Allow Enter key to send message
function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}
