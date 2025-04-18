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

});


