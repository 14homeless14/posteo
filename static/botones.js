function copiarTexto() {
  const tuNombreNombre = document.getElementById("tuNombre").value;
  const tipoFalla = document.getElementById("tipoFalla");
  const textoSeleccionado = tipoFalla.options[tipoFalla.selectedIndex].text;

  const selecionvalidacion = document.getElementById("status");
  const validacionseleccionado =
    selecionvalidacion.options[selecionvalidacion.selectedIndex].text;

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
  navigator.clipboard
    .writeText(texto)
    .then(() => {
      document.getElementById("miDialogo").showModal();
    })
    .catch((err) => {
      console.error("Error al copiar al portapapeles:", err);
    });
}

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("scraping-form");
  const btn = document.getElementById("btnConsultar");

  form.addEventListener("submit", function () {
    btn.disabled = true;
    btn.value = "Consultando..."; // opcional: cambia el texto
  });
});

// Mostrar el diálogo
document.getElementById("miDialogo").addEventListener("close", function () {
  const btn = document.getElementById("btnConsultar");
  btn.disabled = false;
  btn.value = "Consultar";
});

// Conversión de DMS a Decimal
const DMScoordenadas = document.getElementById("coordenadas").value.trim();

// 🔁 Función que detecta el formato de coordenadas y las convierte a decimales
function convertirCoordenadas(DMScoordenadas) {
  // 🧪 Expresión regular para formato DMS: grados, minutos, segundos (ej. 20°39'34.9"N 103°20'58.6"W)
  const dmsRegex =
    /(\d+)[°º]\s*(\d+)[']\s*([\d.]+)["]?\s*([NSns])[\s,]+(\d+)[°º]\s*(\d+)[']\s*([\d.]+)["]?\s*([EWew])/;

  // 🧪 Expresión regular para formato DM: grados y minutos (ej. 20°39.582'N 103°20.976'W)
  const dmRegex =
    /(\d+)[°º]\s*([\d.]+)[']\s*([NSns])[\s,]+(\d+)[°º]\s*([\d.]+)[']\s*([EWew])/;

  // 🧪 Expresión regular para formato decimal (ej. 20.659694 -103.349611)
  const decRegex = /^([-+]?\d+(\.\d+)?)[\s,]+([-+]?\d+(\.\d+)?)/;

  // 🧭 Validación y conversión para formato DMS
  if (dmsRegex.test(DMScoordenadas)) {
    const match = DMScoordenadas.match(dmsRegex);

    // 🎯 Convertimos latitud y longitud con fórmula: grados + minutos/60 + segundos/3600
    let lat =
      parseFloat(match[1]) +
      parseFloat(match[2]) / 60 +
      parseFloat(match[3]) / 3600;
    let lon =
      parseFloat(match[5]) +
      parseFloat(match[6]) / 60 +
      parseFloat(match[7]) / 3600;

    // 👇 Si es hemisferio sur o oeste, se vuelve negativo
    if (match[4].toUpperCase() === "S") lat *= -1;
    if (match[8].toUpperCase() === "W") lon *= -1;

    return { lat, lon };
  }

  // 🧭 Validación y conversión para formato DM
  if (dmRegex.test(DMScoordenadas)) {
    const match = DMScoordenadas.match(dmRegex);

    let lat = parseFloat(match[1]) + parseFloat(match[2]) / 60;
    let lon = parseFloat(match[4]) + parseFloat(match[5]) / 60;

    if (match[3].toUpperCase() === "S") lat *= -1;
    if (match[6].toUpperCase() === "W") lon *= -1;

    return { lat, lon };
  }

  // 🧭 Validación para coordenadas decimales directas
  if (decRegex.test(DMScoordenadas)) {
    const match = DMScoordenadas.match(decRegex);
    const lat = parseFloat(match[1]);
    const lon = parseFloat(match[3]);
    return { lat, lon };
  }

  // ⚠️ Si no coincide ningún formato, se muestra un mensaje de error
  alert(
    "Formato no reconocido. Ejemplos válidos:\n• DMS: 20°39'34.9\"N 103°20'58.6\"W\n• DM: 20°39.582'N 103°20.976'W\n• Decimal: 20.659694 -103.349611"
  );
  return null;
}

document.getElementById("tipoFalla").addEventListener("change", function () {
  const contenedor = document.getElementById("contenedorArchivos");
  contenedor.innerHTML = ""; // limpia antes de volver a insertar

  const tipo = document.getElementById("tipoFalla").value;

  if (tipo === "TOTAL" || tipo === "PARCIAL") {
    contenedor.insertAdjacentHTML(
      "beforeend",
      `
    <label>Domicilios</label>
    <input type="file" name="imageDomicilio" class="inputImagen" accept="image/*">
    <br>
    <img class="previewImagen" src="#" alt="Imagen" style="display: none; max-width: 1000px; max-height: 1000px;">
    <br>
    <label>MAPEO</label>
    <input type="file" name="imageMapeo" class="inputImagen" accept="image/*">
    <br>
    <img class="previewImagen" src="#" alt="Imagen" style="display: none; max-width: 1000px; max-height: 1000px;">
    <br>
      `
    );
  } else if (tipo === "MCA") {
    contenedor.insertAdjacentHTML(
      "beforeend",
      `
    <label>Domicilios</label>
    <input type="file" name="imageDomicilio" class="inputImagen" accept="image/*">
    <br>
    <img class="previewImagen" src="#" alt="Imagen" style="display: none; max-width: 1000px; max-height: 1000px;">
    <br>
    <label>MAPEO</label>
    <input type="file" name="imageMapeo" class="inputImagen" accept="image/*">
    <br>
    <img class="previewImagen" src="#" alt="Imagen" style="display: none; max-width: 1000px; max-height: 1000px;">
    <br>
      `);
  }
});

// Listener para mostrar previsualización de cualquier archivo cargado
document.addEventListener("change", function (event) {
  if (event.target && event.target.classList.contains('inputImagen')) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function () {
        // Encuentra la <img> justo debajo de este input
        let img = event.target.nextElementSibling;
        while (img && img.tagName !== 'IMG') {
          img = img.nextElementSibling;
        }
        if (img) {
          img.src = reader.result;
          img.style.display = "block";
        }
      };
      reader.readAsDataURL(file);
    }
  }
});
