// TITLE CHANGE EFFECT

const titles = ["Full Plate Robotics", "Innovating Tomorrow", "BEST Robotics 2026"];
let currentIndex = 0;

function changeTitle() {
    document.title = titles[currentIndex];
    
    currentIndex = (currentIndex + 1) % titles.length;
}

setInterval(changeTitle, 3000);

// END TITLE CHANGE EFFECT