// Verificar si ya hay una sesión activa
document.addEventListener("DOMContentLoaded", () => {
    const usuario = localStorage.getItem("usuario");
    const contrasena = localStorage.getItem("contrasena");

    // Verificar si estamos en la página de inicio de sesión
    if (window.location.pathname === "/" && usuario && contrasena) {
        // Redirigir automáticamente si la sesión está activa
        window.location.href = "/posteo";
    }
});

// Función para manejar el inicio de sesión
function login() {
    const usuario = document.getElementById("usuario").value;
    const contrasena = document.getElementById("contrasena").value;

    // Validar credenciales (esto es solo un ejemplo, deberías hacerlo en el servidor)
    if (usuario === "elorenzo" && contrasena === "pinolillo123") {
        // Guardar el usuario y la contraseña en localStorage
        localStorage.setItem("usuario", usuario);
        localStorage.setItem("contrasena", contrasena);

        // Redirigir a la página de posteo
        window.location.href = "/posteo";
    } else {
        // Mostrar mensaje de error
        const errorMessage = document.getElementById("error-message");
        errorMessage.style.display = "block";
        errorMessage.textContent = "Usuario o contraseña incorrectos.";
    }
}

// Función para cerrar sesión
function logout() {
    localStorage.removeItem("usuario"); // Eliminar el usuario del navegador
    localStorage.removeItem("contrasena"); // Eliminar la contraseña del navegador
    window.location.href = "/"; // Redirigir al inicio de sesión
}