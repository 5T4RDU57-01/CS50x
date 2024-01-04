function flagblink () {
    let flag = document.querySelector('.bi');

    if (flag.style.visibility == 'visible') 
    {
        flag.style.visibility = 'hidden'
    }
    else
    {
        flag.style.visibility = 'visible'
    }
}

window.setInterval(flagblink, 500);