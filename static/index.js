document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    var counter = 0;
    // When connected, configure buttons
    socket.on('connect', () => {

        // Each button should emit a "submit vote" event
        document.querySelector('#sendpost').onclick = ()  => {
                const content = document.querySelector("#newPost").value;
                socket.emit('add post', {'content': content});
            };
        });




    // When a new vote is announced, add to the unordered list
    socket.on('conversation', data => {
        const li = document.createElement('li');
        li.innerHTML = `new post: ${data.post_content}`;
        document.querySelector("#postim").append(li);
        document.querySelector("#len").innerHTML = `${data.postlen}`;
    });
});
