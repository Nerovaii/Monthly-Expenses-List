document.addEventListener('DOMContentLoaded', fetchGastos);

function fetchGastos() {
    fetch('http://127.0.0.1:8000/gastos/')
    .then(response => response.json())
    .then(data => {
        const gastosTable = document.getElementById('gastos');
        const totalMontoElement = document.getElementById('totalMonto');
        gastosTable.innerHTML = '';
        let totalMonto = 0;

        data.forEach(gasto => {
            const row = gastosTable.insertRow();
            const formattedMonto = new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'CLP' }).format(gasto.monto);
            totalMonto += gasto.monto;
            row.innerHTML = `<td>${gasto.id}</td>
                             <td>${gasto.categoria}</td>
                             <td>${gasto.descripcion}</td>
                             <td>${formattedMonto}</td>`;
        });

        totalMontoElement.textContent = new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'CLP' }).format(totalMonto);
    })
    .catch(error => {
        console.error('Error fetching gastos:', error);
    });
}

function agregarGasto() {
    const formData = {
        categoria: document.getElementById('categoria').value,
        descripcion: document.getElementById('descripcion').value,
        monto: parseFloat(document.getElementById('monto').value),
    };

    fetch('http://127.0.0.1:8000/gastos/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        // Alert with the new ID if available in the response
        if(data.id) {
            alert('Gasto agregado con éxito: ' + JSON.stringify(data));
        } else {
            alert('Gasto agregado pero no se recibió el ID del servidor');
        }
        fetchGastos(); // Refresh the list to show the new item with the ID
    })
    .catch(error => alert('Error al agregar gasto: ' + error));
}
