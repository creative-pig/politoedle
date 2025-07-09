function addguess() {
    guess = document.getElementById("userguess").value
    createrow(guess)
}

function createrow(name) {
    guesslist = document.getElementById("guesslist")
    guessrow = document.createElement("div")
    guessrow.classList.add("guessrow")

    guessname = document.createElement("div")
    guessname.innerHTML = name
    guessname.classList.add("guessresult")
    guessrow.appendChild(guessname)

    guessname = document.createElement("div")
    guessname.innerHTML = name
    guessname.classList.add("guessresult")
    guessrow.appendChild(guessname)

    guessname = document.createElement("div")
    guessname.innerHTML = name
    guessname.classList.add("guessresult")
    guessrow.appendChild(guessname)

    guessname = document.createElement("div")
    guessname.innerHTML = name
    guessname.classList.add("guessresult")
    guessrow.appendChild(guessname)

    guessname = document.createElement("div")
    guessname.innerHTML = name
    guessname.classList.add("guessresult")
    guessrow.appendChild(guessname)

    guessname = document.createElement("div")
    guessname.innerHTML = name
    guessname.classList.add("guessresult")
    guessrow.appendChild(guessname)

    guesslist.appendChild(guessrow)
}