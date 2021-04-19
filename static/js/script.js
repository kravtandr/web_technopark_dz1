document.getElementById("logout-btn").addEventListener("click", () => {
    document.getElementById("user-block-login").className = "user-block-hidden";
    document.getElementById("user-block-logout").className = "user-block-visible";

});
document.getElementById("login-btn").addEventListener("click", () => {
    document.getElementById("user-block-login").className = "user-block-visible";
    document.getElementById("user-block-logout").className = "user-block-hidden";
});