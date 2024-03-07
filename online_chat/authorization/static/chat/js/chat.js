

const roomName = JSON.parse(document.getElementById('room-name').textContent);
const requestUser = JSON.parse(document.getElementById('request-user').textContent);
 
        
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const chat = document.getElementById('chat');
    const dateOptions = {hour: 'numeric', minute: 'numeric', hour24: true};
    const datetime = new Date(data.datetime).toLocaleString('ru', dateOptions);
    const chat_scroll = document.getElementById('chat_scroll');
    console.log(datetime)
    console.log(data);
    const isMe = data.user === requestUser;
    const source = isMe ? 'other-message float-right' : 'my-message';
    const name = isMe ? 'Me' : data.user;
    //document.querySelector('#chat-log').value += (name + ': ' + data.message + '\n');
    chat.innerHTML += '<li class="clearfix">' +
                      '<div class="message-data ' + source + 
                      '-data"><span class="message-data-time">' + 
                        datetime + '</span></div>' + 
                      '<div class="message ' + source + '">' +
                      '<strong>' + name + '</strong> ' +
                      data.message + '</div>' +
                      '</li>';
    chat_scroll.scrollTop = chat_scroll.scrollHeight;
};


chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.key === 'Enter') {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'user': requestUser
    }));
    messageInputDom.value = '';
};