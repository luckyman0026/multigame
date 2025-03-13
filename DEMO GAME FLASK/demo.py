﻿from flask import Flask, render_template_string
import random
import os

app = Flask(__name__)

# Specify the path for static files (optional, Flask automatically recognizes the 'static' folder)
app.static_folder = 'static'

# User balance information
user_balance = 100

# CSS and JavaScript codes
CSS = """
* {
    box-sizing: border-box;
}

:root {
    --item-height: 100px;
}

body {
    background-image: url('/static/wallpaper.webp');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    position: relative;
}

#container {
    background-color: transparent;
    padding: 50px;
    position: relative;
}

.window {
    position: relative;
    overflow: hidden;
    height: calc(4 * var(--item-height));
}

.window-border {
    width: 610px;
    height: 410px;
    background-size: cover;
    background-position: center;
    padding: 5px;
}

.icon {
    width: 80px;
    height: var(--item-height);
    display: block;
    position: relative;
}

.outer-col {
    overflow-y: hidden;
    width: 100px;
    float: left;
    background-color: #eee;
    background-image: linear-gradient(#16013c, #741a5e, #430155, #16013c);
    height: calc(var(--item-height) * 4);
    position: relative;
}

.col {
    padding: 0 10px;
    will-change: true;
    transform: translateY(calc(-100% + var(--item-height) * 4));
    position: relative;
}

.col img {
    width: 100%;
    height: auto;
    margin: 10px 0;
    position: relative;
    z-index: 3;
    transition: opacity 1s ease-in-out;
}

.col .icon::after {
    content: "";
    clear: both;
    display: block;
    position: absolute;
    top: 50%;
    left: 50%;
    width: 1px;
    height: 1px;
    background-color: white;
    box-shadow: 0 0 35px 30px rgba(12, 0, 14, 0.69);
    z-index: 2;
    border-radius: 100%;
}

#container.spinning .outer-col:nth-of-type(2) .col {
    animation-delay: 0.01s;
}

#container.spinning .outer-col:nth-of-type(3) .col {
    animation-delay: 0.02s;
}

#container.spinning .outer-col:nth-of-type(4) .col {
    animation-delay: 0.03s;
}

#container.spinning .outer-col:nth-of-type(5) .col {
    animation-delay: 0.04s;
}

#container.spinning .outer-col:nth-of-type(6) .col {
    animation-delay: 0.05s;
}

#container.spinning .col {
    animation-name: scroll;
    animation-iteration-count: 1;
    animation-timing-function: cubic-bezier(.65, .97, .72, 1);
}

@keyframes scroll {
    to {
        transform: translateY(0);
    }
}

.balance {
    color: White;
    font-size: 70px;
    font-weight: bold;
    text-align: center;
    position: absolute;
    bottom: -86px;
    left: 50%;
    transform: translateX(-220%);
}

.win-message {
    color: White;
    font-size: 70px;
    font-weight: bold;
    text-align: center;
    margin-top: 20px;
    display: none;
    position: absolute;
    top: -5%;
    left: 75%;
    transform: translate(50%, -50%);
    z-index: 10004;
}

.fade-out {
    opacity: 0;
}

.fade-in {
    opacity: 1;
}

#photo-overlay {
    position: fixed;
    top: 49%;
    left: 49.5%;
    transform: translate(-40%, -50%);
    z-index: 9999;
}

#photo-overlay img {
    max-width: 82%;
    max-height: 82%;
    pointer-events: none;
}

#play-button {
    position: absolute;
    top: 95%;
    left: 50%;
    transform: translate(-50%, -50%);
    cursor: pointer;
    z-index: 10000;
}

#play-button.disabled {
    pointer-events: none;
    opacity: 0.5;
}

#play-button img {
    width: 120px;
    height: auto;
}

#money-overlay {
    position: fixed;
    top: 22%;
    left: 50%;
    transform: translate(30%, -50%);
    z-index: 10003;
    width: 200px;
    height: auto;
}

#money-overlay img {
    width: 270px;
    height: auto;
    pointer-events: none;
}

#happy-overlay {
    position: fixed;
    top: 22%;
    left: 37%;
    transform: translate(-50%, -50%);
    z-index: 10003;
    width: 200px;
    height: auto;
}

#happy-overlay img {
    width: 150%;
    height: auto;
    pointer-events: none;
}

#blnc-overlay {
    position: fixed;
    top: 75%;
    left: 36%;
    transform: translate(-50%, -50%);
    z-index: 10003;
    width: 200px;
    height: auto;
}

#blnc-overlay img {
    width: 150%;
    height: auto;
    pointer-events: none;
}

#freespin-overlay {
    position: fixed;
    top: 75%;
    left: 58%;
    transform: translate(-50%, -50%);
    z-index: 10003;
    width: 200px;
    height: auto;
}

#freespin-overlay img {
    width: 150%;
    height: auto;
    pointer-events: none;
}

#exclamation-button {
    position: absolute;
    top: 270px;
    left: 570px;
    cursor: pointer;
    z-index: 10005;
}

#exclamation-button img {
    width: 80px; /* Button size increased */
    height: auto;
}

#page-overlay {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 10006;
    display: none;
}

#page-overlay img {
    max-width: 100%;
    max-height: 90%;
    pointer-events: none;
}
"""

JS = """
const ICONS = [
    { name: 'apple', weight: 10 },
    { name: 'apricot', weight: 8 },
    { name: 'banana', weight: 6 },
    { name: 'cherry', weight: 5 },
    { name: 'grapes', weight: 4 },
    { name: 'lemon', weight: 3 },
    { name: 'lucky_seven', weight: 2 },
    { name: 'orange', weight: 7 },
    { name: 'pear', weight: 6 },
    { name: 'strawberry', weight: 5 },
    { name: 'watermelon', weight: 4 },
];

const MULTIPLIERS = [
    { value: 0.5, weight: 45 },  // 0.5.webp should appear more frequently
    { value: 1, weight: 10 },
    { value: 5, weight: 4 },
    { value: 10, weight: 2 },
    { value: 25, weight: 1 },
    { value: 50, weight: 0.5 },
    { value: 100, weight: 0.3 },
    { value: 250, weight: 0.01 },  // 250.webp should appear rarely
    { value: 500, weight: 0.01 }, // 500.webp should appear rarely
    { value: 1000, weight: 0.01 } // 1000.webp should appear rarely
];

// Weighted random multiplier selection
function getRandomMultiplier() {
    let totalWeight = MULTIPLIERS.reduce((sum, m) => sum + m.weight, 0);
    let randomNum = Math.random() * totalWeight;
    let weightSum = 0;

    for (let multiplier of MULTIPLIERS) {
        weightSum += multiplier.weight;
        if (randomNum <= weightSum) {
            return multiplier.value;
        }
    }
}

// Weighted random symbol selection
function getRandomIcon() {
    let totalWeight = ICONS.reduce((sum, icon) => sum + icon.weight, 0);
    let randomNum = Math.random() * totalWeight;
    let weightSum = 0;

    for (let icon of ICONS) {
        weightSum += icon.weight;
        if (randomNum <= weightSum) {
            return icon.name;
        }
    }
}

const BASE_SPINNING_DURATION = 2.7;
const COLUMN_SPINNING_DURATION = 0.3;

var cols;
var balance = 100;
var isSpinning = false;
var isCheckingResults = false;
var moneyOverlay = null;
var multiplierIcons = [];

window.addEventListener('DOMContentLoaded', function(event) {
    cols = document.querySelectorAll('.col');
    setInitialItems();
    updateBalance();

    moneyOverlay = document.getElementById('money-overlay');

    document.getElementById('play-button').addEventListener('click', function() {
        if (!isSpinning && !isCheckingResults) {
            spin(this);
        }
    });

    document.getElementById('exclamation-button').addEventListener('click', function(event) {
        event.stopPropagation(); // Prevents overlay from closing when the button is clicked
        document.getElementById('page-overlay').style.display = 'block';
    });

    document.addEventListener('click', function(event) {
        if (event.target.id !== 'exclamation-button') {
            document.getElementById('page-overlay').style.display = 'none';
        }
    });

    document.addEventListener('keydown', function(event) {
        if (event.key === 'ArrowLeft') {
            moveMoneyLeft();
        } else if (event.key === 'ArrowRight') {
            moveMoneyRight();
        }
    });
});

function moveMoneyLeft() {
    let currentLeft = parseInt(moneyOverlay.style.left) || 10;
    moneyOverlay.style.left = (currentLeft - 10) + 'px';
}

function moveMoneyRight() {
    let currentLeft = parseInt(moneyOverlay.style.left) || 10;
    moneyOverlay.style.left = (currentLeft + 10) + 'px';
}

function setInitialItems() {
    let baseItemAmount = 40;

    for (let i = 0; i < cols.length; ++i) {
        let col = cols[i];
        let amountOfItems = baseItemAmount + (i * 3);
        let elms = '';
        let firstFourElms = '';

        for (let x = 0; x < amountOfItems; x++) {
            let icon = getRandomIcon(); // Weighted random selection
            let item = '<div class="icon" data-item="' + icon + '"><img src="/static/' + icon + '.webp"></div>';
            elms += item;

            if (x < 4) firstFourElms += item;
        }
        col.innerHTML = elms + firstFourElms;
    }
}

function spin(elem) {
    if (balance < 10) {
        alert("Insufficient balance!");
        return;
    }

    isSpinning = true;
    balance -= 10;
    updateBalance();

    let duration = BASE_SPINNING_DURATION + randomDuration();

    for (let col of cols) {
        duration += COLUMN_SPINNING_DURATION + randomDuration();
        col.style.animationDuration = duration + "s";
    }

    elem.classList.add('disabled');

    document.getElementById('container').classList.add('spinning');

    window.setTimeout(setResult, BASE_SPINNING_DURATION * 1000 / 2);
    
    window.setTimeout(function () {
        document.getElementById('container').classList.remove('spinning');
        isSpinning = false;
    }.bind(elem), duration * 1000);
}

function setResult() {
    let results = [];
    for (let col of cols) {
        let columnResults = [
            getRandomIcon(), // Weighted random selection
            getRandomIcon(),
            getRandomIcon(),
            getRandomIcon()
        ];
        results.push(columnResults);

        let icons = col.querySelectorAll('.icon img');
        for (let x = 0; x < 4; x++) {
            icons[x].setAttribute('src', '/static/' + columnResults[x] + '.webp');
            icons[(icons.length - 4) + x].setAttribute('src', '/static/' + columnResults[x] + '.webp');
        }
    }

    isCheckingResults = true;
    setTimeout(() => {
        checkForSymbols(results);
        isCheckingResults = false;
        document.getElementById('play-button').classList.remove('disabled');
    }, 5000);
}

function checkForSymbols(results) {
    let symbolCounts = {};
    for (let result of results) {
        for (let symbol of result) {
            if (symbolCounts[symbol]) {
                symbolCounts[symbol]++;
            } else {
                symbolCounts[symbol] = 1;
            }
        }
    }

    // Prize table for 4 symbols
    const prizeMap4 = {
        'lucky_seven': 0.5,
        'orange': 0.5,
        'pear': 0.5,
        'strawberry': 0.5,
        'watermelon': 0.5,
        'apricot': 1,
        'grapes': 1.5,
        'cherry': 2.5,
        'apple': 3,
        'banana': 3.5,
        'lemon': 4
    };

    // Prize table for 6 symbols (1.5 times the 4-symbol prize)
    const prizeMap6 = {
        'lucky_seven': 0.75,
        'orange': 0.75,
        'pear': 0.75,
        'strawberry': 0.75,
        'watermelon': 0.75,
        'apricot': 1.5,
        'grapes': 2.25,
        'cherry': 3.75,
        'apple': 4.5,
        'banana': 5.25,
        'lemon': 6
    };

    // Prize table for 8 symbols (2 times the 4-symbol prize)
    const prizeMap8 = {
        'lucky_seven': 1,
        'orange': 1,
        'pear': 1,
        'strawberry': 1,
        'watermelon': 1,
        'apricot': 2,
        'grapes': 3,
        'cherry': 5,
        'apple': 6,
        'banana': 7,
        'lemon': 8
    };

    let totalWin = 0;

    // Calculate winnings for 4, 6, or 8 symbols
    for (let symbol in symbolCounts) {
        if (symbolCounts[symbol] === 4) {
            let prize = prizeMap4[symbol] || 0;
            totalWin += prize;
            animateSymbols(symbol);
        } else if (symbolCounts[symbol] === 6) {
            let prize = prizeMap6[symbol] || 0; // Separate prize table for 6 symbols
            totalWin += prize;
            animateSymbols(symbol);
        } else if (symbolCounts[symbol] === 8) {
            let prize = prizeMap8[symbol] || 0; // Separate prize table for 8 symbols
            totalWin += prize;
            animateSymbols(symbol);
        }
    }

    if (totalWin > 0) {
        balance += totalWin;
        updateBalance();
        showWinMessage(totalWin);
    }
}

function showWinMessage(prize) {
    let winMessage = document.querySelector('.win-message');
    winMessage.innerText = ` ${prize}`;
    winMessage.style.display = 'block';

    setTimeout(() => {
        winMessage.style.display = 'none';
    }, 3000);
}

function animateSymbols(symbol) {
    let icons = document.querySelectorAll('.icon img');
    let matchingIcons = [];

    icons.forEach(icon => {
        if (icon.getAttribute('src').includes(symbol)) {
            matchingIcons.push(icon);
        }
    });

    matchingIcons.forEach(icon => {
        icon.classList.add('fade-out');
    });

    setTimeout(() => {
        matchingIcons.forEach(icon => {
            let multiplier = getRandomMultiplier();
            icon.setAttribute('src', '/static/X/' + multiplier + '.webp');
            icon.classList.remove('fade-out');
            icon.classList.add('fade-in');
            multiplierIcons.push(icon); // Store multiplier symbols
        });

        // Keep multiplier symbols on the screen
        setTimeout(() => {
            matchingIcons.forEach(icon => {
                icon.classList.remove('fade-in');
            });
        }, 8000);
    }, 1000);
}

function randomDuration() {
    return Math.floor(Math.random() * 10) / 100;
}

function updateBalance() {
    document.querySelector('.balance').innerText = '' + balance + '$';
}
"""

@app.route('/')
def index():
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Sloty</title>
        <style>{CSS}</style>
        <script>{JS}</script>
    </head>
    <body>

    <div id="container">
        <div class="window-border">
            <div class="window">
                <div class="outer-col">
                    <div class="col"></div>
                </div>
                <div class="outer-col">
                    <div class="col"></div>
                </div>
                <div class="outer-col">
                    <div class="col"></div>
                </div>
                <div class="outer-col">
                    <div class="col"></div>
                </div>
                <div class="outer-col">
                    <div class="col"></div>
                </div>
                <div class="outer-col">
                    <div class="col"></div>
                </div>
            </div>
        </div>

        <div id="play-button">
            <img src="/static/play.webp" alt="Play">
        </div>

        <div class="balance">Balance: {user_balance}$</div>
        <div class="win-message">Win 20$</div>
    </div>

    <div id="photo-overlay">
        <img src="/static/photo.webp" alt="Photo">
    </div>

    <div id="money-overlay">
        <img src="/static/money.webp" alt="Money">
    </div>

    <div id="happy-overlay">
        <img src="/static/happy.webp" alt="Happy">
    </div>

    <div id="blnc-overlay">
        <img src="/static/blnc.webp" alt="blnc">
    </div>

    <div id="freespin-overlay">
        <img src="/static/freespin.webp" alt="freespin">
    </div>

    <div id="exclamation-button">
        <img src="/static/Exclamation.webp" alt="Exclamation">
    </div>

    <div id="page-overlay">
        <img src="/static/page.webp" alt="Page">
    </div>

    </body>
    </html>
    """
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=True, port=5000)