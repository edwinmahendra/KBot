class Chatbox {
    constructor() {
        this.args = {
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = true;
        this.messages = [];
    }

    display() {
        const {chatBox, sendButton} = this.args;

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    toggleState(chatbox) {
        this.state = !this.state;

        // show or hides the box
        if(this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }

        let currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        let msg1 = { name: "User", message: text1, time: currentTime }
        this.messages.push(msg1);

        fetch('http://127.0.0.1:5001/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
          })
          .then(r => r.json())
          .then(r => {
            console.log(r);
            let currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            let msg2 = { name: "K-Bot", message: r.message, time: currentTime }; // Changed from r.answer to r.message
            this.messages.push(msg2);
            this.updateChatText(chatbox)
            textField.value = ''

        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
          });
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name === "K-Bot")
            {
                html += '<div class="messages__item messages__item--visitor"><div class="message-time">' + item.time + '</div><div class="message-text">' + item.message + '</div></div>'
            }
            else
            {
                html += '<div class="messages__item messages__item--operator"><div class="message-time">' + item.time + '</div><div class="message-text">' + item.message + '</div></div>'
            }
          });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}


const chatbox = new Chatbox();
chatbox.display();