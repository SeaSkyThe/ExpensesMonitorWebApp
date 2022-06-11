var fadeTarget = document.querySelector(".messages");

if(fadeTarget != null){
    function fadeOutEffect() {
    
        var fadeEffect = setInterval(function () {
            if (!fadeTarget.style.opacity) {
                fadeTarget.style.opacity = 1;
            }
            if (fadeTarget.style.opacity > 0) {
                fadeTarget.style.opacity -= 0.1;
            } 
            else {
                fadeTarget.style.display = 'none';
                clearInterval(fadeEffect);
            }
        }, 190);
    }
    
    fadeOutEffect()
}

