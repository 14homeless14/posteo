function copiarTexto() {
  const tuNombreNombre = document.getElementById("tuNombre").value;
  const tipoFalla = document.getElementById("tipoFalla");
  const textoSeleccionado = tipoFalla.options[tipoFalla.selectedIndex].text;

  const selecionvalidacion = document.getElementById("status");
  const validacionseleccionado = selecionvalidacion.options[selecionvalidacion.selectedIndex].text;

  const Titulo = document.getElementById("tituloFalla").value;
  const sucursal = document.getElementById("sucursal").value;
  const TT = document.getElementById("numeroTT").value;
  const OT = document.getElementById("folioOT").value;
  const ctcHub = document.getElementById("ctcHub").value;
  const alarma = document.getElementById("alarma").value;
  const coordenadas = document.getElementById("coordenadas").value;
  const afectacion = document.getElementById("clientesAfectados").value;
  const datosAdicionales = document.getElementById("datosAdicionales").value;
  const fechaCreacion = document.getElementById("fechaAlarm").value;

  // Construir el texto a copiar
  let texto = `*RNOC:* ${tuNombreNombre} *INICIO*\n`;
  texto += `*Titulo de la falla:* ${Titulo}\n`;
  texto += `*TIPO FALLA:* ${textoSeleccionado}\n`;
  texto += `*SUCURSAL:* ${sucursal}\n`;
  texto += `*TT: ${TT} OT: ${OT}*\n`;
  if (ctcHub.trim() !== "") {
    texto += `*CTC o HUB:* ${ctcHub}\n`;
  }
  if (alarma.trim() !== "") {
    texto += `Alarma: *${alarma}*\n`;
  }
  texto += `*COORDENADAS:* ${coordenadas}\n`;
  texto += `*AFECTACIÓN:* ${afectacion}\n`;
  texto += `*Validación:* ${validacionseleccionado}\n`;
  if (datosAdicionales.trim() !== "") {
    texto += `*Datos adicionales:* ${datosAdicionales}\n`;
  }
  texto += `*Fecha de Creación:* ${fechaCreacion}\n`;

  // Mostrar en el <dialog>
  document.getElementById("contenidoDialogo").textContent = texto;


  // Copiar al portapapeles
  navigator.clipboard.writeText(texto).then(() => {
    document.getElementById("miDialogo").showModal();
  }).catch(err => {
    console.error("Error al copiar al portapapeles:", err);
  });
}


  document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('scraping-form');
    const btn = document.getElementById('btnConsultar');

    form.addEventListener('submit', function () {
      btn.disabled = true;
      btn.value = 'Consultando...'; // opcional: cambia el texto
    });
  });

  // Mostrar el diálogo
  document.getElementById("miDialogo").addEventListener("close", function () {
    const btn = document.getElementById('btnConsultar');
    btn.disabled = false;
    btn.value = 'Consultar';
  });
  
  