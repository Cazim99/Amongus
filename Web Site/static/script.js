
function burgerBtnOnClick() {
    btn = document.getElementById("burger-btn")
    if(!btn.className.includes("is-active")){
        document.getElementById("navbarmenu").classList.add("is-active")
        btn.classList.add("is-active")
    }else{
        document.getElementById("navbarmenu").classList.remove("is-active")
        btn.classList.remove("is-active")
    }
}


function logoImageOnClick(){
    logo_image = document.getElementById("nav-logo-image")
    if (logo_image.src.includes("1")){
        while(logo_image.src.includes("1")){
            logo_image.src = logo_image.src.replace("/static/images/dice1.png", "/static/images/dice" + String(Math.floor(Math.random() * 7) + 1) + ".png")
        }
    }
}


function sendChat(){
    chat = document.getElementById("chat-input").value
    userName = document.getElementById("user").getAttribute("name")

    var current_date = new Date().toLocaleTimeString('en-US', { hour12: false, 
        hour: "numeric", 
        minute: "numeric"});

    window.location = "/home?chat=[" + current_date + "] " + userName+ ": "+chat
}