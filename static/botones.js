document.addEventListener("DOMContentLoaded", () => {
  // Referencias a los elementos del DOM
  const dialogo = document.getElementById("miDialogo");
  const abrirBtn = document.getElementById("abrirDialogo");
  const cerrarBtn = document.getElementById("cerrarDialogo");
  const cargar = document.getElementById("cargar");

  // Verificar que los elementos se han cargado correctamente
  console.log(dialogo, abrirBtn, cerrarBtn, cargar);

  // Evento para abrir el diálogo
  abrirBtn.addEventListener("click", () => {
    console.log("Abriendo el diálogo");
    dialogo.showModal(); // Muestra el diálogo
  });

  // Evento para cerrar el diálogo
  cerrarBtn.addEventListener("click", () => {
    console.log("Cerrando el diálogo");
    dialogo.close(); // Cierra el diálogo
  });

  fetch("/scrape") // Realiza la solicitud al servidor Flask
    .then((response) => response.json()) // Convierte la respuesta a JSON
    .then((data) => {
      // Asignar los valores al formulario
      document.getElementById("folioOT").value = data.ticketId;
      document.getElementById("fechaAlarm").value = data.fechaAlarm;
      document.getElementById("descripcion").value = data.descripcion;
      document.getElementById("tituloFalla").value = data.titulo;
      document.getElementById("nodo").value = data.nodo;
      document.getElementById("sucursal").value = data.sistema;
      document.getElementById("numSucursal").value = data.numSucursal;
      document.getElementById("sga").value = data.sga;
      document.getElementById("tiempoTrascurriodeTT").value = data.tiempoDeTT;

      // Mostrar una alerta si el nodo es '0000'
      if (data.nodo === "0000") {
        alert("¡Alerta! El nodo es '0000'.");
      }
    })
    .catch((error) => console.error("Error al obtener los datos:", error));
});

function logout() {
  localStorage.removeItem("usuario"); // Eliminar la sesión del navegador
  window.location.href = "/"; // Redirigir al inicio de sesión
}