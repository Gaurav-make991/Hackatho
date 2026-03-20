document.querySelector('.login-btn').addEventListener('click', function() {
    window.location.href = 'login.html';
});

document.querySelector('.btn').addEventListener('click', function() {
    window.location.href = 'problem.html';
});


const profileIcon = document.getElementById("profile-icon");
const sidebar = document.getElementById("profile-sidebar");
const closeSidebar = document.getElementById("close-sidebar");
const logoutBtn = document.getElementById("logout-btn");

// Open Sidebar
profileIcon.addEventListener("click", () => {
  sidebar.classList.add("active");
});

// Close Sidebar
closeSidebar.addEventListener("click", () => {
  sidebar.classList.remove("active");
});

// Logout
logoutBtn.addEventListener("click", () => {
  alert("Logged out successfully!");
  sidebar.classList.remove("active");
});

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    const offset = 80; // adjust based on navbar height
    const topPos = target.getBoundingClientRect().top + window.scrollY - offset;
    window.scrollTo({ top: topPos, behavior: "smooth" });
  });
});



// NAVBAR LINKS FIX
document.querySelectorAll('.nav-links a').forEach(link => {
  link.addEventListener('click', function(e) {

    e.preventDefault();

    const targetId = this.getAttribute('href');
    const targetSection = document.querySelector(targetId);

    if(targetSection){
      targetSection.scrollIntoView({
        behavior: "smooth",
        block: "start"
      });
    }

  });
});



