        const roomName = JSON.parse(document.getElementById('room-name').textContent);
        const requestUser = JSON.parse(document.getElementById('request-user').textContent);
        const chatSocket = new WebSocket(
            //ngrok
            //'wss://'
            //localhost
            'ws://'
            + window.location.host
            + '/ws/chat/'
            + roomName
            + '/'
        );

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);

            if (data.type === 'user.online_status') {
                const userStatusElement = document.getElementById('user-status');
                if (data.status) {
                    userStatusElement.textContent = 'онлайн';
                } else {
                    const lastOnline = new Date(data.last_online);
                    const now = new Date();
                    const yesterday = new Date(now);
                    yesterday.setDate(now.getDate() - 1);
                    const optionsTime = { hour: 'numeric', minute: 'numeric', hour12: false };
                    const options = {day: 'numeric', month: 'short', minute: 'numeric', hour: 'numeric', hour12: false};

                    if (lastOnline.getDate() === now.getDate() &&
                        lastOnline.getMonth() === now.getMonth() &&
                        lastOnline.getFullYear() === now.getFullYear()) {
                        const formattedTime = lastOnline.toLocaleTimeString('ru-RU', optionsTime);
                        userStatusElement.innerHTML = `Был в сети: сегодня<br> в ${formattedTime}`;
                    } else if (lastOnline.getDate() === yesterday.getDate() &&
                        lastOnline.getMonth() === yesterday.getMonth() &&
                        lastOnline.getFullYear() === yesterday.getFullYear()) {
                        const formattedTime = lastOnline.toLocaleTimeString('ru-RU', optionsTime);
                        userStatusElement.textContent = `Был в сети: вчера в ${formattedTime}`;
                }
                     else {
                        const formattedDate = lastOnline.toLocaleDateString('ru-RU', options);
                        userStatusElement.textContent = `Последний раз в сети:<br> ${formattedDate}`;
                            }
                }

                const userStatusElementChat = document.querySelector('.chat #user-status')
                if (userStatusElementChat) {
                    userStatusElementChat.innerHTML = userStatusElement.innerHTML;
                }
                

            } else {

            const chat = document.getElementById('chat');
            const dateOptions = {hour: 'numeric', minute: 'numeric', day:'numeric', month:'short', hour24: true};
            const messageDate = new Date(data.datetime);
            const today = new Date();
            const yesterday = new Date(today);
            yesterday.setDate(today.getDate() - 1);
            const chat_scroll = document.getElementById('chat_scroll');

            console.log(data);
            
            const isMe = data.user === requestUser;
            const source = isMe ? 'other-message float-right' : 'my-message';
            const name = isMe ? '' : data.user;

            const isToday = messageDate.getDate() === today.getDate() &&
                   messageDate.getMonth() === today.getMonth() &&
                   messageDate.getFullYear() === today.getFullYear();

            const isYesterday = messageDate.getDate() === yesterday.getDate() &&
                   messageDate.getMonth() === yesterday.getMonth() &&
                   messageDate.getFullYear() === yesterday.getFullYear();
  
            let datetime;
            if (isToday) {
                datetime = 'сегодня ' + messageDate.toLocaleString('ru', {hour: 'numeric', minute: 'numeric', hour12: false});
            } else if (isYesterday) {
                datetime = 'вчера ' + messageDate.toLocaleString('ru', {hour: 'numeric', minute: 'numeric', hour12: false});
            } else {
                datetime = messageDate.toLocaleString('ru', dateOptions);
            }
            chat.innerHTML += '<li class="clearfix">' +
                              '<div class="message-data ' + source + 
                              '-data"><span class="message-data-time">' + 
                                datetime + '</span></div>' + 
                              '<div class="message ' + source + '">' +
                              '<strong>' + name + '</strong> ' +
                              data.message + '</div>' +
                              '</li>';
            chat_scroll.scrollTop = chat_scroll.scrollHeight;
            }

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
            
            if (message !== '') {
                chatSocket.send(JSON.stringify({
                    'message': message,
                    'user': requestUser
                }));
                messageInputDom.value = '';
            } 
        };


        //search
        const user_input = $("#user-input")
        const chats_div = $('#replaceable-content')
        const endpoint = '/chat/search/'
        const delay_by_in_ms = 100
        let scheduled_function = false

        let ajax_call = function (endpoint, request_parameters) {
            $.getJSON(endpoint, request_parameters)
                .done(response => {
                    chats_div.fadeTo(200, 0).promise().then(() => {
                        chats_div.html(response['html_from_view'])
                        chats_div.fadeTo(200, 1)
                    })
                })
                
        }
        
        user_input.on('keyup', function () {
            const searchValue = $(this).val()
            if (searchValue === '') {
                replaceOriginalContent();
                return;
            }

            const request_parameters = {
                search: searchValue 
            }
            
        
            if (scheduled_function) {
                clearTimeout(scheduled_function)
            }

            scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
        });

        const initialContent = $('#replaceable-content').html();

        function replaceOriginalContent() {
            chats_div.html(initialContent);
        }

        const user_input_2 = $("#user-input-2")
        const users_div = $('#replace_content_group')
        const endpoint_group = '/chat/search/'
        let scheduled_function_group_add = false

        let ajax_call_group_add = function (endpoint_group, request_parameters) {
            $.getJSON(endpoint_group, request_parameters)
                .done(response => {
                    users_div.fadeTo(200, 0).promise().then(() => {
                        users_div.html(response['html_from_view'])
                        users_div.fadeTo(200, 1)
                    })
                })
                
        }
        
        user_input_2.on('keyup', function () {
            const searchValue = $(this).val()
            if (searchValue === '') {
                replaceOriginalContentGroup();
                return;
            }

            const request_parameters = {
                search: searchValue,
                room_id: roomName,
            }

            if (scheduled_function_group_add) {
                clearTimeout(scheduled_function_group_add)
            }

            scheduled_function_group_add = setTimeout(ajax_call_group_add, delay_by_in_ms, endpoint_group, request_parameters)
        });

        const initialContentGroup = $('#replace_content_group').html();

        function replaceOriginalContentGroup() {
            users_div.html(initialContentGroup);
        }
        
        document.addEventListener("DOMContentLoaded", function() {
            const showParticipantsLink = document.getElementById("show-participants");
            const showParticipantsLinkImage = document.getElementById("show-participants-image");
            const participantsList = document.getElementById("participants-list");
            const participantsListImage = document.getElementById("participants-list-image");
        
            showParticipantsLink.addEventListener("click", function(event) {
                event.preventDefault();
        
                if (participantsList.style.display === "block") {
                    participantsList.style.display = "none";
                } else {
                    participantsList.style.display = "block";
                }
            });


            showParticipantsLinkImage.addEventListener("click", function(event) {
                event.preventDefault();
        
                if (participantsListImage.style.display === "block") {
                    participantsListImage.style.display = "none";
                } else {
                    participantsListImage.style.display = "block";
                }
            });
        });