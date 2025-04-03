const paragraphText = "Welcome to Art Spot! A space where creativity thrives! Showcase your art, connect with fellow creators, and share your passion with the world.";

const paragraph = document.getElementById("paragraph");
let index = 0;

function typeText() {
  if (index < paragraphText.length) {
    paragraph.textContent += paragraphText.charAt(index);
    index++;
    setTimeout(typeText, 50); // Adjust typing speed here (lower = faster)
  }
}
  let currentSectionIndex = 0;
  const sections = document.querySelectorAll('section');
  let isScrolling = false; // Prevent multiple triggers

  function scrollToSection(index) {
    if (index >= 0 && index < sections.length) {
      isScrolling = true;
      sections[index].scrollIntoView({ behavior: 'smooth' });

      setTimeout(() => {
        isScrolling = false; // Allow scrolling again after animation completes
      }, 800); // Adjust timing to match smooth scrolling duration
    }
  }

  window.addEventListener('wheel', (event) => {
    if (isScrolling) return; // Prevents multiple scroll triggers

    if (event.deltaY > 0) {
      // Scroll Down
      if (currentSectionIndex < sections.length - 1) {
        currentSectionIndex++;
        scrollToSection(currentSectionIndex);
      }
    } else if (event.deltaY < 0) {
      // Scroll Up
      if (currentSectionIndex > 0) {
        currentSectionIndex--;
        scrollToSection(currentSectionIndex);
      }
    }
  });

//NAVBARFINALLYYY
document.addEventListener("DOMContentLoaded", function () {
const navbar = document.getElementById("hidden-navbar");

document.addEventListener("mousemove", function (event) {
  if (event.clientY <= 60) {
    navbar.style.top = "0"; // Show navbar
  } else if (event.clientY > 100) {
    navbar.style.top = "-60px"; // Hide navbar
  }
});
});

document.querySelector(".magnetic-btn").addEventListener("mousemove", function(e) {
const rect = this.getBoundingClientRect();
const x = e.clientX - rect.left - rect.width / 2;
const y = e.clientY - rect.top - rect.height / 2;
this.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px)`;
});

document.querySelector(".magnetic-btn").addEventListener("mouseleave", function() {
this.style.transform = "translate(0, 0)";
});
