console.log("Working")



    


document.addEventListener("DOMContentLoaded", function() {
    console.log("printed")
    var messageContainer = document.getElementById('message-container');
    console.log(messageContainer)
    messageContainer.scrollTop = messageContainer.scrollHeight;
});

// function scrollToBottom() {
//     var messageContainer = document.getElementById('message-container');
//     messageContainer.scrollTop = messageContainer.scrollHeight;
// }

// // Call the scrollToBottom function after a delay to ensure proper scrolling when new messages are added
// setTimeout(scrollToBottom, 100);

// const testing = document.getElementById('testing_chat')
// testing.addEventListener('click',function(){
//     console.log("clicked")
// })




const testing = document.getElementById('testing_chat')
testing.addEventListener('click',function(){
    console.log("clicked")
})



  
  