const chatInput = document.querySelector("#chat-input");
const sendButton = document.querySelector("#send-btn");
const chatContainer = document.querySelector(".chat-container");
const API_KEY = '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';
const themeButton = document.querySelector("#theme-btn");
const deleteButton = document.querySelector("#delete-btn");
const micBtn = document.querySelector("#mic-btn");
const logoutButton = document.querySelector("#logout-btn");

let userText = null;
let initialHeight;

function initializeApp() {
    initialHeight = chatInput.scrollHeight;

    // Attach event listeners after elements are initialized
    themeButton.addEventListener("click", () => {
        document.body.classList.toggle("light-mode");
        localStorage.setItem("theme-color", themeButton.innerText);
        themeButton.innerText = document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode";
    });

    deleteButton.addEventListener("click", (event) => {
        if (event.target === deleteButton) {
            if (confirm("Are you sure want to delete all the chats?")) {
                chatContainer.querySelectorAll('.chat').forEach(chat => chat.remove());
                localStorage.removeItem("all-chats");
                loadDataFromLocalStorage();
            }
        }
    });

    chatInput.addEventListener("input", () => {
        chatInput.style.height = `${initialHeight}px`;
        chatInput.style.height = `${chatInput.scrollHeight}px`;
    });

    chatInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
            e.preventDefault();
            handleOutgoingChat();
        }
    });

    sendButton.addEventListener("click", handleOutgoingChat);
}

window.onload = () => {
    initializeApp();
    loadDataFromLocalStorage();
};

const createElement = (html, className) => {
    const chatDiv = document.createElement("div");
    chatDiv.classList.add("chat", className);
    chatDiv.innerHTML = html;
    return chatDiv;
}

const getChatResponse = async (incomingChatDiv, userText) => {
  const API_URL = "https://api.openai.com/v1/chat/completions";
  const pElement = document.createElement("p");

  const requestOptions = {
      method: 'POST',
      headers: {
          'Authorization': `Bearer ${API_KEY}`,
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          "model": "gpt-3.5-turbo",
          "messages": [{"role": "user", "content": userText}],
          "temperature": 0.7
      })
  }
  try {
      const response = await (await fetch(API_URL, requestOptions)).json();
      pElement.textContent = response.choices[0].message.content.trim();
  } catch (error) {
    pElement.classList.add("error");
      pElement.textContent = "Oops! Something went wrong while retrying the response. Please try again."
  }

  incomingChatDiv.querySelector(".typing-animation").remove();
  
  const chatDetails = incomingChatDiv.querySelector(".chat-details");
  chatDetails.appendChild(pElement);
  chatContainer.scrollTo(0, chatContainer.scrollHeight);
  localStorage.setItem("all-chats", chatContainer.innerHTML);
}

const copyResponse = (copyBtn) => {
  const responseTextElement = copyBtn.parentElement.querySelector("p");
  navigator.clipboard.writeText(responseTextElement.textContent);
  copyBtn.textContent = "done";
  setTimeout(() => copyBtn.textContent = "content_copy", 1000);
}

const speakResponse = (speakBtn) => {
    const responseTextElement = speakBtn.parentElement.querySelector("p");
    const text = responseTextElement.textContent;
    // Function to calculate the chunk size based on the text length
    const calculateChunkSize = (textLength) => {
        // Adjust this factor as needed
        const chunkFactor = 1; //0.05; // 10% of text length
        return Math.max(1, Math.round(textLength * chunkFactor));
    };
    // Clear the synthesis queue
    speechSynthesis.cancel();
    // Calculate the chunk size dynamically based on text length
    const chunkSize = calculateChunkSize(text.length);
    // Chunk and speak the text
    for (let i = 0; i < text.length; i += chunkSize) {
        const chunk = text.substring(i, i + chunkSize);
        const utterance = new SpeechSynthesisUtterance(chunk);
        // Error handling, rate, pitch, and onend events remain unchanged
        utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event.error);
        };
        // Adjust rate and pitch as needed
        utterance.rate = 1.0; // Adjust the rate as needed (default is 1.0)
        utterance.pitch = 0.8; // Adjust the pitch as needed (default is 1.0)
        // Listen to the onend event to chain synthesis
        utterance.onend = () => {
            // Continue with the next chunk or utterance if needed
        };
        // Initiate speech synthesis for each chunk
        speechSynthesis.speak(utterance);
    }
};

const showTypingAnimation = () => {
  const html = `<div class="chat-content">
      <div class="chat-details">
          <img src="static/images/Logo2.png" alt="chatbot-img">
          <div class="typing-animation">
              <div class="typing-dot" style="--delay: 0.2s"></div>
              <div class="typing-dot" style="--delay: 0.3s"></div>
              <div class="typing-dot" style="--delay: 0.4s"></div>
          </div>
      </div>
      <span onclick="copyResponse(this)" class="material-symbols-outlined">content_copy</span>
      <span onclick="speakResponse(this)" class="material-symbols-outlined">select_to_speak</span>
  </div>`;
  const incomingChatDiv = createElement(html, "incoming");
  chatContainer.appendChild(incomingChatDiv);
  chatContainer.scrollTo(0, chatContainer.scrollHeight);
  getChatResponse(incomingChatDiv, userText);
}

const handleOutgoingChat = () => {
    userText = chatInput.value.trim();
    if (!userText) return;

    chatInput.value = "";
    chatInput.style.height = `${initialHeight}px`;
    
    const html = `<div class="chat-content">
        <div class="chat-details">
            <img src="static/images/chat-bot-concept-illustration_114360-5522-modified.png" alt="user-img">
            <p></p>
        </div>
    </div>`;
    const outgoingChatDiv = createElement(html, "outgoing");
    outgoingChatDiv.querySelector("p").textContent = userText;
    document.querySelector(".default-text")?.remove();
    chatContainer.appendChild(outgoingChatDiv);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    setTimeout(showTypingAnimation, 500);
}

micBtn.addEventListener('click', function () {
    var speech = true;
    window.SpeechRecognition = window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.interimResults = true;

    if (speech == true) {
        recognition.start();

        recognition.onresult = function (event) {
            const transcript = Array.from(event.results)
                .map(result => result[0].transcript)
                .join('');

            chatInput.value = transcript;
        };

        recognition.onend = function () {
            handleOutgoingChat();
        };

        recognition.onerror = function (event) {
            console.error('Speech recognition error:', event.error);
        };
    }
});

logoutButton.addEventListener("click", () => {
    if (confirm("Are you sure you want to logout?")) {
        localStorage.removeItem("userToken");
        window.location.href = "/";
    }
});




  /*
themeButton.addEventListener("click", () => {
    document.body.classList.toggle("light-mode");
    localStorage.setItem("theme-color", themeButton.innerText);
    themeButton.innerText = document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode";
});

deleteButton.addEventListener("click", (event) => {
    if (event.target === deleteButton) {
      if (confirm("Are you sure want to delete all the chats?")) {
        chatContainer.querySelectorAll('.chat').forEach(chat => chat.remove());

        localStorage.removeItem("all-chats");
        loadDataFromLocalStorage();
      }
    }
  });

chatInput.addEventListener("input", () => {
    chatInput.style.height = `${initialHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
    if(e.key === "Enter" && !e.shiftKey && window.innerWidth > 800){
        e.preventDefault();
        handleOutgoingChat();
    }
});

sendButton.addEventListener("click", handleOutgoingChat);
*/