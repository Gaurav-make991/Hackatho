const container = document.querySelector('.container');
const LoginLink = document.querySelector('.SignInLink');
const RegisterLink = document.querySelector('.SignUpLink');

RegisterLink.addEventListener('click', () =>{
    container.classList.add('active');
})

LoginLink.addEventListener('click', () => {
    container.classList.remove('active');
})

// document.getElementById("google-login").addEventListener("click", () => {
//   window.open("https://www.google.com/");

  


document.getElementById("google-login").addEventListener("click", () => {
  window.location.href = "/auth/google"; // direct backend route
});

//login with google


