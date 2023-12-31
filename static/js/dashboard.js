//Declaring variables
const sidebar = document.querySelector(".sidebar");
const toggle = document.querySelector(".toggle");
const modeSwitch = document.querySelector(".mode");
const modeText = document.querySelector(".mode-text");
const chatInput = document.querySelector("#chat-input");
const sendButton = document.querySelector("#send-btn");
const chatContainer = document.querySelector(".chat-container");
const deleteButton = document.querySelector("#delete-btn");
const micBtn = document.querySelector("#mic-btn");

let userText = null;
let initialHeight;

function handleScan() {
    const hiddenInput = document.getElementById('hidden-input');

    // Trigger the click event on the hidden file input
    hiddenInput.click();

    // Listen for changes in the file input
    hiddenInput.addEventListener('change', async () => {
        if (!hiddenInput.files || hiddenInput.files.length === 0) {
            console.error("No image selected");
            return;
        }

        const file = hiddenInput.files[0];
        const reader = new FileReader();

        reader.onload = async () => {
            const image = new Image();
            image.onload = async () => {
                try {
                    const { data: { text } } = await Tesseract.recognize(image, 'eng');
                    
                    // Update the textarea with the OCR result
                    const chatInput = document.getElementById('chat-input');
                    chatInput.value = text;

                } catch (error) {
                    console.error("Error recognizing text:", error);
                }
            };
            image.src = reader.result;
        };

        reader.readAsDataURL(file);
    });
}

function initializeApp() {
  initialHeight = chatInput.scrollHeight;

  const body = document.body; // Add this line to define the 'body' variable

  toggle.addEventListener("click", () => {
      sidebar.classList.toggle("close");
  });

  modeSwitch.addEventListener("click", () => {
      body.classList.toggle("dark"); // Use the 'body' variable here
      if (body.classList.contains("dark")) {
          modeText.innerHTML = "Light Mode";
      } else {
          modeText.innerHTML = "Dark Mode";
      }
  });

    //Delete-btn function
    deleteButton.addEventListener("click", (event) => {
        if (event.target === deleteButton) {
            if (confirm("Are you sure want to delete all the chats?")) {
                chatContainer.querySelectorAll('.chat').forEach(chat => chat.remove());
                localStorage.removeItem("all-chats");
                loadDataFromLocalStorage();
            }
        }
    });

    //Input field
    chatInput.addEventListener("input", () => {
        chatInput.style.height = `${initialHeight}px`;
        chatInput.style.height = `${chatInput.scrollHeight}px`;
    });

    //Enter & shift + enter input field functions
    chatInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
            e.preventDefault();
            handleOutgoingChat();
        }
    });

    //send-btn function
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
  const API_URL = "/chat";
  const pElement = document.createElement("p");

  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      "userText": userText
    })
  };

  try {
      const response = await (await fetch(API_URL, requestOptions)).json();
      pElement.textContent = response.message.trim();
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

//Speaker-btn function
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

//Before getting response and displaying
const showTypingAnimation = () => {
  const html = `<div class="chat-content">
      <div class="chat-details">
      <img src="static/images/1_C_LFPy6TagD1SEN5SwmVRQ.jpg" alt="chatbot-img">
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
            <img src="static/images/business+costume+male+man+office+user+icon-1320196264882354682.png" alt="user-img">
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

//Mic-btn to convert the voice to text and provide same to the input field
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

//Customized pop window function
document.addEventListener("DOMContentLoaded", function () {
    const logoutButton = document.getElementById("logout-btn");
    const pop = document.getElementById("pop");
    const confirmLogoutButton = document.getElementById("confirmLogout");
    const cancelLogoutButton = document.getElementById("cancelLogout");

    logoutButton.addEventListener("click", () => {
        pop.classList.add("visible");
    });

    confirmLogoutButton.addEventListener("click", () => {
        localStorage.removeItem("userToken");
        window.location.href = "/";
    });

    cancelLogoutButton.addEventListener("click", () => {
        pop.classList.remove("visible");
    });

    window.addEventListener("click", (event) => {
        if (event.target === pop) {
            pop.classList.remove("visible");
        }
    });
});
