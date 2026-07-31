function toggleTheme(){
  document.body.classList.toggle("dark");
  document.querySelector(".toggle").innerText =
    document.body.classList.contains("dark") ? "☀️" : "🌙";
}

function showLoader(){
  document.getElementById("loginBtn").classList.add("loading");
  document.getElementById("loginBtn").innerText="Signing in...";
  document.getElementById("loader").style.display="block";
}
