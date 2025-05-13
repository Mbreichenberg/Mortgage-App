/* Reset styles for consistent rendering across all browsers */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: Arial, sans-serif; /* Ensure a consistent base font */
}

/* --- Background and general body styles --- */
html {
    height: 100%;
    width: 100%;
    margin: 0;
    padding: 0;
    overflow-x: hidden;
}

body {
    height: 100%;
    width: 100%;
    margin: 0;
    padding: 0;
    overflow-x: hidden;
    background-color: lightblue;
    background-image: url('/static/VWNY.png'); /* Optional, adjust as needed */
    background-size: cover; /* Ensures the background image covers the screen */
    background-position: center; /* Center the background image */
    background-repeat: no-repeat; /* Prevents tiling of the image */
    min-height: 100vh; /* Ensures the body covers the full height of the screen */
    opacity: 0;
    animation: fadeIn 2s ease forwards;
}

/* --- Animations --- */
@keyframes scrollBackground {
    0% {
        background-position: 0 0;
    }
    100% {
        background-position: -4000px 0; /* Adjust based on your image width */
    }
}

@keyframes fadeIn {
    to {
        opacity: 1;
    }
}

/* --- Container and form styling --- */
.container {
    background-color: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    max-width: 1200px; /* Max width to prevent stretching too much on large screens */
    margin: 0 auto; /* Center the container horizontally */
    width: 100%; /* Ensure the container stretches to the full width on small screens */
}

form.form {
    text-align: center;
    margin-top: 20px;
    font-size: 18px;
    padding: 10px 20px;
    font-family: 'Caveat', cursive;
}

.input_box {
    margin-top: 20px;
    font-size: 18px;
    padding: 10px 20px;
    background-color: #fff4e6;
    border: 2px solid black;
    font-family: 'Caveat', cursive;
    box-shadow: 3px 3px 0px 0px black;
}

/* --- Typography --- */

h1 {
    text-align: center;
    font-family: 'Patrick Hand', cursive;
    font-size: 48px;
    color: #222;
    padding-top: 50px;
    padding-bottom: 20px;
    text-shadow: 3px 5px 5px rgba(0, 0, 0, 0.3);
}

h3, h4 {
    color: #28a745;
}

.header {
    position: relative;
    width: 100%;
    height: 100px;
}

.header img {
    position: absolute;
    top: 0;
    left: 0;
    margin-top: -150px;
    height: 600px;
    z-index: 1;
}

.text-center {
    color: lightblue;
}

.header h1 {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    margin: 0;
    font-size: 48px;
    text-align: center;
    z-index: 2;
}

/* --- Buttons and Links --- */
button,
.rough-button {
    font-size: 1rem;
    padding: 0.6rem 1.2rem;
    background-color: #fff4e6;
    border: 2px solid black;
    border-radius: 8px; /* Slightly rounded corners */
    font-family: 'Caveat', cursive;
    box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.1); /* More natural shadow */
    transition: all 0.2s ease-in-out;
    display: inline-block;
    text-align: center;
    cursor: pointer;
    text-decoration: none;
    color: black;
}

/* Button Hover */
button:hover,
.rough-button:hover {
    background-color: #fefcc2;
    box-shadow: 2px 2px 0 #000;
    transform: translate(1px, 1px);
}

/* --- Canvas (for future charts maybe) --- */
canvas {
    max-width: 100%;
    margin: 30px 0;
}

#bmc-button {
    display: inline-block;
    margin: 100px 0 0 100px;
}

#coffee2 {
    align-items: center;
    display: flex;
    justify-content: center;
}

/* --- Media Queries --- */
@media (max-width: 600px) {
    /* Adjust button size for smaller screens */
    button,
    .rough-button {
        font-size: 0.9rem;
        padding: 0.4rem 0.8rem;
    }
}

@media (min-width: 1024px) {
    /* Larger screen styles */
    button,
    .rough-button {
        font-size: 1.2rem; /* Slightly larger font size for better visibility */
        padding: 0.8rem 1.5rem; /* Adjust padding for larger buttons */
    }
}
