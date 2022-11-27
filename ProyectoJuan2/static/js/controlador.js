
// ********************************************** FUNCIONES AUXILIARES *****************************************************
/**
 * Consulta AJAX al servidor por método POST
 * @param {string} urlserver :dirección de envio
 * @param {string} datos     :Data en formato JavaScript object
 * @param {funtion} callBackFuntion :Función de retorno
 */
function mensajeAjax(urlserver, datos, callBackFuntion) {
    
    const csrftoken = getCookie('csrftoken');
    fetch(urlserver, {
        method: 'post',
        credentials: 'same-origin',
        headers:{
            'Accept': 'application/json',
            'X-Requested-With' : 'XMLHttpRequest',
            'x-CSRFToken': csrftoken,
        },
        body: JSON.stringify(datos) // JavaScript objet of data to POST 
    })
        .then(response => response.json()) // convierte la respuesta JSON en data
        .then(data => {
            callBackFuntion(data)
        })
        .catch((error) => {
            console.error('Error', JSON.stringify(error));
        })
} 

/**
 * Lee la cookie del navegador para validar el token de seguridad
 * @param {*} name Nombre de la cookie
 * @returns el contenido de la cookie
 */

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            //Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }   
        }     
    }
    return cookieValue
}
/************************************************EVENTOS DE LISTA**************************************************** */
window.onload = (event) => {
    if (document.getElementById('id_categoriasHoras') !== null) {
        document.getElementById('id_categoriasHoras').addEventListener('change', consultarCategHora, false)
    }

    if (document.getElementById('id_categoriasProveedor') !== null) {
        document.getElementById('id_categoriasProveedor').addEventListener('change', consultarProveedor, false)
    }

    if (document.getElementById('id_categoriasMaterial') !== null) {
        document.getElementById('id_categoriasMaterial').addEventListener('change', consultarCategMaterial, false)
    }

    if (document.getElementById('id_categoriasMedidas') !== null) {
        document.getElementById('id_categoriasMedidas').addEventListener('change', consultarUnidadMedida, false)
    }
};

// **********************************************manejador de eventos********************************************************************

function consultarCategHora() {
    let id = document.getElementById('id_categoriasHoras').value;
    let url = "http://localhost:8000/administracion/hora/";
    let datos = {
        'id': id,        
    };
    mensajeAjax(url, datos, consultarCategHoraResp);

}

function consultarCategHoraResp(data) {
    document.getElementById('id_descripCategHora').value = data['descripCategHora'];
    document.getElementById('id_recargo').value = data['recargo'];
}

//********************************************************************************************************************/

// **************************manejador de eventos******************************************************************** /

function consultarProveedor() {
    let id = document.getElementById('id_categoriasProveedor').value;
    let url = "http://localhost:8000/administracion/proveedor/";
    let datos = {
        'id': id,        
    };
    mensajeAjax(url, datos, consultarProveedorResp);

}

function consultarProveedorResp(data) {
    document.getElementById('id_telefonoProveedor').value = data['telefonoProveedor'];
    document.getElementById('id_nombreProveedor').value = data['nombreProveedor'];
    document.getElementById('id_nitProvedor').value = data['nitProvedor'];
    document.getElementById('id_direccionProveedor').value = data['direccionProveedor'];
    document.getElementById('id_correoProveedor').value = data['correoProveedor'];
}

//********************************************************************************************************************/

// **************************manejador de eventos******************************************************************** /

function consultarCategMaterial() {
    let id = document.getElementById('id_categoriasMaterial').value;
    let url = "http://localhost:8000/administracion/material/";
    let datos = {
        'id': id,        
    };
    mensajeAjax(url, datos, consultarCategMaterialResp);

}

function consultarCategMaterialResp(data) {
    document.getElementById('id_descripCategMaterial').value = data['descripCategMaterial'];
}

//********************************************************************************************************************/

// **************************manejador de eventos******************************************************************** /


function consultarUnidadMedida() {
    let id = document.getElementById('id_categoriasMedidas').value;
    let url = "http://localhost:8000/administracion/medida/";
    let datos = {
        'id': id,        
    };
    mensajeAjax(url, datos, consultarUnidadMedidaResp);

}

function consultarUnidadMedidaResp(data) {
    document.getElementById('id_descripUnidadMedida').value = data['descripUnidadMedida'];
}

//********************************************************************************************************************/

// ************************************ CONSULTAR Y FILTRAR EQUIPO *********************************************** /

function filtrardDescripEquipo() {
    let id = document.getElementById('listaEquipos').value;
    let url = "http://localhost:8000/administracion/equipos/";
    let datos = {
        'id': id,        
    };
    mensajeAjax(url, datos, filtrardDescripEquipoResp);

}

function filtrardDescripEquipoResp(data) {
    document.getElementById('descripEquipo').value = data['descripEquipo'];
    document.getElementById('listaCategoriasMat').value = data['categMaterial'];
}

function filtrarEquipos() {
    let idMateriales = document.getElementById('listaCategoriasMat').value;
    let listaopciones = document.getElementById('listaEquipos').options;

    let caso = 0
    if ( idMateriales > '0') caso += 1;
    
    //Primero deja todo visible
    for (let i = 1; i < listaopciones.length; i++) {
        listaopciones[i].removeAttribute("hidden");
    }

    switch (caso) {
        case 1:    // materiales > 0: Filtrar solo por materiales
            for (let i = 1; i < listaopciones.length; i++) {
                let material = listaopciones[i].dataset.material;
                if (material != idMateriales) {
                    listaopciones[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
    }
}
// ************************************ CONSULTAR Y FILTRAR DESCRIPCION DE INSUMOS *********************************************** /

function filtradescripInsumos() {
    let id = document.getElementById('listainsumos').value;
    let url = "http://localhost:8000/administracion/insumos/";
    let datos = {
        'id': id,        
    };
    mensajeAjax(url, datos, filtradescripInsumosResp);

}

function filtradescripInsumosResp(data) {
    document.getElementById('descripInsumo').value = data['descripInsumo'];
    document.getElementById('listaMateriales').value = data['categMaterial'];
    document.getElementById('listaMedidas').value = data['unidadMedida'];
}
    
//+++++++++++++++++++++++++++++++++++++++++++CONSULTAR Y FILTRAR INSUMOS+++++++++++++++++++++++++++++++++++++++

function filtrarInsumos() {
    let idMateriales = document.getElementById('listaMateriales').value;
    let idMedidas = document.getElementById('listaMedidas').value;
    let listaopcionees = document.getElementById('listainsumos').options;

    let caso = 0
    if ( idMedidas > '0') caso += 1;
    if (idMateriales > '0') caso += 2;
    
    //Primero deja todo visible
    for (let i = 1; i < listaopcionees.length; i++) {
        listaopcionees[i].removeAttribute("hidden");
    }

    switch (caso) {
        case 1:    //Unidad en cero, materiales > 0: Filtrar solo por materiales
            for (let i = 1; i < listaopcionees.length; i++) {
                let medida = listaopcionees[i].dataset.medida;
                if (medida != idMedidas) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
 
        case 2:    //caso = 2: materiales en cero, unidad > 0: Filtrar solo por unidad
            for (let i = 1; i < listaopcionees.length; i++) {
                if (listaopcionees[i].dataset.material != idMateriales) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
        case 3:   //caso = 3: Unidad > 0, materiales > 0: Filtrar por los dos
            for (let i = 1; i < listaopcionees.length; i++) {
                if (listaopcionees[i].dataset.medida != idMedidas  || listaopcionees[i].dataset.material != idMateriales) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
    }
}


//+++++++++++++++++++++++++++++++++++ CONSULTAR Y FILTRAR TRABAJADOR +++++++++++++++++++++++++++++++++++++++++++++++
function filtrarTrabajador() {
    
        let id = document.getElementById('listaTrabajador').value;
        let url = "http://localhost:8000/gerentes/trabajadores/";
        let datos = {
            'id': id,        
        };
        mensajeAjax(url, datos, filtrarTrabajadorResp);
    
    }
    
    function filtrarTrabajadorResp(data) {
        document.getElementById('nombreTrabajador').value = data['nombreTrabajador'];
        document.getElementById('nitTrabajador').value = data['nitTrabajador'];
        document.getElementById('telefonoTrabajador').value = data['telefonoTrabajador'];
        document.getElementById('emailTrabajador').value = data['emailTrabajador'];
        document.getElementById('costoHoraTrabajador').value = data['costoHoraTrabajador'];
        document.getElementById('rol').value = data['rol'];
    }


//+++++++++++++++++++++++++++++++++++++++++ CONSULTAR Y FILTRAR LOTES +++++++++++++++++++++++++++++++++++++++++++++++++++
function filtrardDescripLote() {
    let id = document.getElementById('conjuntoLotes').value;
    let url = "http://localhost:8000/gerentes/lotes/";
    let datos = {
        'id': id,        
    };
    mensajeAjax(url, datos, filtrardDescripLoteResp);

}

function filtrardDescripLoteResp(data) {
    document.getElementById('observacLote').value = data['observacLote'];
    document.getElementById('listaMedidas').value = data['unidadMedida'];
    document.getElementById('descripLote').value = data['descripLote'];
    document.getElementById('areaLote').value = data['areaLote'];
}

function filtrarLotes() {
    let idMedidas = document.getElementById('listaMedidas').value;
    let listaopciones = document.getElementById('conjuntoLotes').options;

    let caso = 0
    if ( idMedidas > '0') caso += 1;
    
    //Primero deja todo visible
    for (let i = 1; i < listaopciones.length; i++) {
        listaopciones[i].removeAttribute("hidden");
    }

    switch (caso) {
        case 1:    // medidas > 0: Filtrar solo por medidas
            for (let i = 1; i < listaopciones.length; i++) {
                let medida = listaopciones[i].dataset.medida;
                if (medida != idMedidas) {
                    listaopciones[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
    }
}
//+++++++++++++++++++++++++++++++++++++++++ CONSULTAR Y FILTRAR EQUIPOS DE FINCA  +++++++++++++++++++++++++++++++++++++++++++++++++++

function filtrardDescripEquipoFinca() {
    let id = document.getElementById('listaEquipoFinca').value;
    let url = "http://localhost:8000/gerentes/equipoFinca/";
    let datos = {
        'id': id,        
    };
    mensajeAjax(url, datos, filtrardDescripEquipoFincaResp);

}

function filtrardDescripEquipoFincaResp(data) {
    document.getElementById('existenciaEquipo').value = data['existenciaEquipo'];
    document.getElementById('valorUnitarioEquipo').value = data['valorUnitarioEquipo'];
    document.getElementById('deprecEquipo').value = data['deprecEquipo'];
}