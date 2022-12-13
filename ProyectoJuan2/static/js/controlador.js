
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
    document.getElementById("listaEquipos").value = data["equipo"];
    document.getElementById('valorUnitarioEquipo').value = data['valorUnitarioEquipo'];
    document.getElementById('deprecEquipo').value = data['deprecEquipo'];
    document.getElementById('descripEquipoFinca').value = data['descripEquipoFinca'];
}

function filtrarEquipoFinca() {
    let idEquipo = document.getElementById('listaEquipos').value;
    let listaopciones = document.getElementById('listaEquipoFinca').options;

    let caso = 0
    if ( idEquipo > '0') caso += 1;
    
    //Primero deja todo visible
    for (let i = 1; i < listaopciones.length; i++) {
        listaopciones[i].removeAttribute("hidden");
    }

    switch (caso) {
        case 1:    // equipo > 0: Filtrar solo por equipo
            for (let i = 1; i < listaopciones.length; i++) {
                let equipo = listaopciones[i].dataset.equipo;
                if (equipo != idEquipo) {
                  listaopciones[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
    }
}

//+++++++++++++++++++++++++++++++++++++++++ CONSULTAR Y FILTRAR COSTOS INDIRECTOS +++++++++++++++++++++++++++++++++++++++++++++++++++

function filtrardDescripIndirectos() {
    let id = document.getElementById('listaIndirectos').value;
    let url = "http://localhost:8000/gerentes/indirectos/";
    let datos = {
        'id': id,        
    };
    mensajeAjax(url, datos, filtrardDescripIndirectosResp);

}

function filtrardDescripIndirectosResp(data) {
    document.getElementById('fechaPago').value = data['fechaPago'];
    document.getElementById('numFactura').value = data['numFactura'];
    document.getElementById('observacPago').value = data['observacPago'];
    document.getElementById('valorPagado').value = data['valorPagado'];
}


//+++++++++++++++++++++++++++++++++++++++++ CONSULTAR Y FILTRAR INSUMOS DE FINCA  +++++++++++++++++++++++++++++++++++++++++++++++++++

function filtrardDatosInsumoFinca() {
    let id = document.getElementById("listaInsumosFinca").value;
    let url = "http://localhost:8000/gerentes/insumoFinca/";
    let datos = {
        'id': id,        
    };
    mensajeAjax(url, datos, filtrardDatosInsumoFincaResp);

}

function filtrardDatosInsumoFincaResp(data) {
  document.getElementById("listaInsumos").value = data['insumo'];
  document.getElementById("listaUnidades").value = data['unidadmedida'];
  document.getElementById("existenciaInsumo").value = data['existenciaInsumo'];
  document.getElementById("valorUnitarioInsumo").value =data['valorUnitarioInsumo'];
  document.getElementById("descripInsumoFinca").value =data['descripInsumoFinca'];
}

function filtrarInsumosFinca() {
    let idInsumos = document.getElementById('listaInsumos').value;
    let idMedidas = document.getElementById('listaUnidades').value;
    let listaopcionees = document.getElementById('listaInsumosFinca').options;

    let caso = 0
    if ( idInsumos > '0') caso += 1;
    if ( idMedidas > '0') caso += 2;
    
    //Primero deja todo visible
    for (let i = 1; i < listaopcionees.length; i++) {
        listaopcionees[i].removeAttribute("hidden");
    }

    switch (caso) {
        case 1:    //MEDIDAS >0 INSUMO = 0 : FILTRAR SOLO POR MEDIDAS
            for (let i = 1; i < listaopcionees.length; i++) {
                let insumo = listaopcionees[i].dataset.insumo;
                if (insumo != idInsumos) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
 
        case 2:    //INSUMOS >0 MEDIDA = 0 : FILTRA SOLO POR INSUMOS
            for (let i = 1; i < listaopcionees.length; i++) {
                let medida = listaopcionees[i].dataset.medida;
                if (medida != idMedidas) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
        case 3:   //MEDIDAS > 0, INSUMOS > 0: Filtrar por los dos
            for (let i = 1; i < listaopcionees.length; i++) {
                if (listaopcionees[i].dataset.medida != idMedidas  || listaopcionees[i].dataset.insumo != idInsumos) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
    }
}

//+++++++++++++++++++++++++++++++++++++++++ CONSULTAR Y FILTRAR PRODUCTOS +++++++++++++++++++++++++++++++++++++++++++++++++++
function filtrardDescrpProducto() {
    let id = document.getElementById('listaProductos').value;
    let url = "http://localhost:8000/gerentes/productos/";
    let datos = {
        'id': id,        
    };
    mensajeAjax(url, datos, ffiltrardDescrpProductoResp);

}

function ffiltrardDescrpProductoResp(data) {
    document.getElementById('listaMedidas').value = data['unidadMedida'];
    document.getElementById('descripProducto').value = data['descripProducto'];
    document.getElementById('existenciaProducto').value = data['existenciaProducto'];
}

function filtrarProductos() {
    let idMedidas = document.getElementById('listaMedidas').value;
    let listaopciones = document.getElementById('listaProductos').options;

    let caso = 0
    if ( idMedidas > '0') caso += 1;
    
    //Primero deja todo visible
    for (let i = 1; i < listaopciones.length; i++) {
        listaopciones[i].removeAttribute("hidden");
    }

    switch (caso) {
        case 1:  //MEDIDAS > 0 : FILTRAR SOLO POR MEDIDAS
            for (let i = 1; i < listaopciones.length; i++) {
                let medida = listaopciones[i].dataset.medida;
                if (medida != idMedidas) {
                    listaopciones[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
    }
}

//+++++++++++++++++++++++++++++++++++ CONSULTAR Y FILTRAR CLIENTE +++++++++++++++++++++++++++++++++++++++++++++++
function filtrarCliente() {
    
    let id = document.getElementById('listaClientes').value;
    let url = "http://localhost:8000/gerentes/clientes/";
    let datos = {
        'id': id,        
    };
    mensajeAjax(url, datos, filtrarClienteResp);

}

function filtrarClienteResp(data) {
    document.getElementById('nombreCliente').value = data['nombreCliente'];
    document.getElementById('nitCliente').value = data['nitCliente'];
    document.getElementById('telefonoCliente').value = data['telefonoCliente'];
    document.getElementById('correoCliente').value = data['correoCliente'];
    document.getElementById('direccionCliente').value = data['direccionCliente'];
}

//+++++++++++++++++++++++++++++++++++ CONSULTAR Y FILTRAR CULTIVOS +++++++++++++++++++++++++++++++++++++++++++++++

function filtrarDatosCultivo() {
    let id = document.getElementById("listaCultivos").value;
    let url = "http://localhost:8000/gerentes/cultivos/";
    let datos = {
        'id': id,        
    };
    mensajeAjax(url, datos, filtrarDatosCultivoResp);

}

function filtrarDatosCultivoResp(data) {
  document.getElementById("listaMedidas").value = data['unidadMedida'];
  document.getElementById("listaProductos").value = data['producto'];
  document.getElementById("listaLotes").value = data['lote'];
  document.getElementById("fechaSiembra").value =data['fechaSiembra'];
  document.getElementById("fechaCosecha").value =data['fechaCosecha'];
  document.getElementById("cantidadCosecha").value =data['cantidadCosecha'];
  document.getElementById("observacCultivo").value =data['observacCultivo'];
  document.getElementById("activo").value =data['activo'];
}

function filtrarCultivo() {
    let idProductos = document.getElementById('listaProductos').value;
    let idMedidas = document.getElementById('listaMedidas').value;
    let idLotes = document.getElementById('listaLotes').value;
    let listaopcionees = document.getElementById('listaCultivos').options;

    let caso = 0
    if ( idMedidas > '0') caso += 1;
    if ( idProductos > '0') caso += 2;
    if ( idLotes > '0') caso += 3;
    
    //Primero deja todo visible
    for (let i = 1; i < listaopcionees.length; i++) {
        listaopcionees[i].removeAttribute("hidden");
    }

    switch (caso) {
        case 1:    //MEDIDAS >0, PRODUCTOS = 0, LOTES = 0 : FILTRAR SOLO POR MEDIDAS
            for (let i = 1; i < listaopcionees.length; i++) {
                let medida = listaopcionees[i].dataset.medida;
                if (medida != idMedidas) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
 
        case 2:    //PRODUCTOS >0, MEDIDAS = 0, LOTES = 0 : FILTRAR SOLO POR PRODUCTOS
            for (let i = 1; i < listaopcionees.length; i++) {
                let producto = listaopcionees[i].dataset.producto;
                if (producto != idProductos) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;

        case 3:   //LOTE >0, MEDIDAS = 0, PPRODUCTO = 0 : FILTRAR SOLO POR LOTE
            for (let i = 1; i < listaopcionees.length; i++) {
                let lote = listaopcionees[i].dataset.lote;
                if (lote != idLotes) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
        
        case 4, 5, 6:    //FILTRAR POR TODAS LAS CATEGORIAS
            for (let i = 1; i < listaopcionees.length; i++) {
                if (listaopcionees[i].dataset.medida != idMedidas  || listaopcionees[i].dataset.producto != idProductos || listaopcionees[i].dataset.lote != idLotes) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
    }
}


//+++++++++++++++++++++++++++++++++++ CONSULTAR Y FILTRAR COMPRA DE EQUIPOS +++++++++++++++++++++++++++++++++++++++++++++++

function filtrarDatosCompraEquipo() {
    let id = document.getElementById("listaCompraEquipo").value;
    let url = "http://localhost:8000/gerentes/compraEquipo/";
    let datos = {
        'id': id,        
    };
    mensajeAjax(url, datos, filtrarDatosCompraEquipoResp);

}

function filtrarDatosCompraEquipoResp(data) {
  document.getElementById("listaEquipo").value = data['equipo'];
  document.getElementById("listaEquipoFinca").value = data['equipoFinca'];
  document.getElementById("listaProveedores").value = data['proveedor'];
  document.getElementById("fechaCompraEquipo").value =data['fechaCompraEquipo'];
  document.getElementById("numFactura").value =data['numFactura'];
  document.getElementById("cantidadCompraEquipo").value =data['cantidadCompraEquipo'];
  document.getElementById("valorCompraEquipo").value =data['valorCompraEquipo'];
}

function filtrarCompraEquipo() {
    let idEquipoFinca = document.getElementById('listaEquipoFinca').value;
    let idEquipo = document.getElementById('listaEquipo').value;
    let idProveedores = document.getElementById('listaProveedores').value;
    let listaopcionees = document.getElementById('listaCompraEquipo').options;

    let caso = 0
    if ( idEquipo > '0') caso += 1;
    if ( idEquipoFinca > '0') caso += 2;
    if ( idProveedores > '0') caso += 3;
    
    //Primero deja todo visible
    for (let i = 1; i < listaopcionees.length; i++) {
        listaopcionees[i].removeAttribute("hidden");
    }

    switch (caso) {
        case 1:    //EQUIPO >0, EQUIPOFINCA = 0, PROVEEDORES = 0 : FILTRAR SOLO POR EQUIPO
            for (let i = 1; i < listaopcionees.length; i++) {
                let equipo = listaopcionees[i].dataset.equipo;
                if (equipo != idEquipo) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
 
        case 2:   //EQUPO FINCA >0, EQUIPO = 0, PROVEEDORES = 0 : FILTRAR SOLO POR EQUIPO FINCA
            for (let i = 1; i < listaopcionees.length; i++) {
                let equipoFinca = listaopcionees[i].dataset.equipofinca;
                if (equipoFinca != idEquipoFinca) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;

        case 3:   //PROVEEDORES >0, EQUIPO = 0, EQUIPOFINCA = 0 : FILTRAR SOLO POR PROVEEDORES
            for (let i = 1; i < listaopcionees.length; i++) {
                let proveedor = listaopcionees[i].dataset.proveedor;
                if (proveedor != idProveedores) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
        
        case 4, 5, 6:    //FILTRAR POR TODAS LAS CATEGORIAS
            for (let i = 1; i < listaopcionees.length; i++) {
                if (listaopcionees[i].dataset.equipo != idEquipo  || listaopcionees[i].dataset.equipofinca != idEquipoFinca || listaopcionees[i].dataset.proveedor != idProveedores) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
    }
}

//+++++++++++++++++++++++++++++++++++ CONSULTAR Y FILTRAR COMPRA DE INSUMOS +++++++++++++++++++++++++++++++++++++++++++++++

function filtrarDatosCompraInsumo() {
    let id = document.getElementById("listaCompraInsumo").value;
    let url = "http://localhost:8000/gerentes/CompraInsumo/";
    let datos = {
        'id': id,        
    };
    mensajeAjax(url, datos, filtrarDatosCompraInsumoResp);

}

function filtrarDatosCompraInsumoResp(data) {
  document.getElementById("listaInsumo").value = data['insumo'];
  document.getElementById("listaInsumoFinca").value = data['insumoFinca'];
  document.getElementById("listaProveedores").value = data['proveedor'];
  document.getElementById("cantidadCompraInsumo").value =data['cantidadCompraInsumo'];
  document.getElementById("fechaCompraInsumo").value =data['fechaCompraInsumo'];
  document.getElementById("numFactura").value =data['numFactura'];
  document.getElementById("valorCompraInsumo").value =data['valorCompraInsumo'];
}

function filtrarCompraInsumo() {
    let idInsumoFinca = document.getElementById('listaInsumoFinca').value;
    let idInsumo = document.getElementById('listaInsumo').value;
    let idProveedores = document.getElementById('listaProveedores').value;
    let listaopcionees = document.getElementById('listaCompraInsumo').options;

    let caso = 0
    if ( idInsumo > '0') caso += 1;
    if ( idInsumoFinca > '0') caso += 2;
    if ( idProveedores > '0') caso += 3;
    
    //Primero deja todo visible
    for (let i = 1; i < listaopcionees.length; i++) {
        listaopcionees[i].removeAttribute("hidden");
    }

    switch (caso) {
        case 1:    //INSUMO >0, INSUMO FINCA = 0, PROVEEDORES = 0 : FILTRAR SOLO POR INSUMO
            for (let i = 1; i < listaopcionees.length; i++) {
                let insumo = listaopcionees[i].dataset.insumo;
                if (insumo != idInsumo) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
 
        case 2:   //INSUMO FINCA >0, EQUIPO = 0, INSUMO = 0 : FILTRAR SOLO POR INSUMO FINCA
            for (let i = 1; i < listaopcionees.length; i++) {
                let equipofinca = listaopcionees[i].dataset.equipofinca;
                if (equipofinca != idEquipoFinca) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
        break;
        case 3:   //PROVEEDORES >0, EQUIPO = 0, INSUMO FINCA = 0 : FILTRAR SOLO POR INSUMO
            for (let i = 1; i < listaopcionees.length; i++) {
                let proveedor = listaopcionees[i].dataset.proveedor;
                if (proveedor != idProveedores) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
        
        case 4, 5, 6:    //FILTRAR POR TODAS LAS CATEGORIAS
            for (let i = 1; i < listaopcionees.length; i++) {
                if (listaopcionees[i].dataset.insumo != idInsumo  || listaopcionees[i].dataset.insumofinca != idInsumoFinca || listaopcionees[i].dataset.proveedor != idProveedores) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
    }
}

//+++++++++++++++++++++++++++++++++++ CONSULTAR Y FILTRAR LABORES DE EQUIPOS +++++++++++++++++++++++++++++++++++++++++++++++

function filtrarDatosLaborEquipos() {
    let id = document.getElementById("listaEquipoLabor").value;
    let url = "http://localhost:8000/gerentes/equiposLabor/";
    let datos = {
        'id': id,        
    };
    mensajeAjax(url, datos, filtrarDatosLaborEquiposResp);

}

function filtrarDatosLaborEquiposResp(data) {
  document.getElementById("listaCultivos").value = data['cultivo'];
  document.getElementById("listaEquipoFinca").value = data['equipoFinca'];
  document.getElementById("cantidadUsadaEquipo").value =data['cantidadUsadaEquipo'];
  document.getElementById("costo").value =data['costo'];
}

function filtrarLaborEquipo() {
    let idEquipoFinca = document.getElementById('listaEquipoFinca').value;
    let idCultivo = document.getElementById('listaCultivos').value;
    let listaopcionees = document.getElementById('listaEquipoLabor').options;

    let caso = 0
    if ( idCultivo > '0') caso += 1;
    if ( idEquipoFinca > '0') caso += 2;
    
    //Primero deja todo visible
    for (let i = 1; i < listaopcionees.length; i++) {
        listaopcionees[i].removeAttribute("hidden");
    }

    switch (caso) {
        case 1:    //CULTIVO > 0 FILTRAR SOLO POR CULTIVOS:
            for (let i = 1; i < listaopcionees.length; i++) {
                let cultivo = listaopcionees[i].dataset.cultivo;
                if (cultivo != idCultivo) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
 
        case 2:   //EQUIPOS DE FINCA >0 FILTRAR SOLO POR EQUIPO DE FINCA:
            for (let i = 1; i < listaopcionees.length; i++) {
                let equipofinca = listaopcionees[i].dataset.equipofinca;
                if (equipofinca != idEquipoFinca) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;

        
        case 3:    //FILTRAR POR TODAS LAS CATEGORIAS
            for (let i = 1; i < listaopcionees.length; i++) {
                if (listaopcionees[i].dataset.cultivo != idCultivo  || listaopcionees[i].dataset.equipofinca != idEquipoFinca) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
    }
}


//+++++++++++++++++++++++++++++++++++ CONSULTAR Y FILTRAR LABORES DE INSUMOS +++++++++++++++++++++++++++++++++++++++++++++++

function filtrarDatosLaborInsumo() {
    let id = document.getElementById("listaInsumoLabor").value;
    let url = "http://localhost:8000/gerentes/insumoLabor/";
    let datos = {
        'id': id,        
    };
    mensajeAjax(url, datos, filtrarDatosLaborInsumoResp);

}

function filtrarDatosLaborInsumoResp(data) {
  document.getElementById("listaCultivos").value = data['cultivo'];
  document.getElementById("listaInsumosFinca").value = data['insumoFinca'];
  document.getElementById("cantidadUsadaInsumo").value =data['cantidadUsadaInsumo'];
  document.getElementById("costo").value =data['costo'];
}

function filtrarLaborInsumo() {
    let idInsumoFinca = document.getElementById('listaInsumosFinca').value;
    let idCultivo = document.getElementById('listaCultivos').value;
    let listaopcionees = document.getElementById('listaInsumoLabor').options;

    let caso = 0
    if ( idCultivo > '0') caso += 1;
    if ( idInsumoFinca > '0') caso += 2;
    
    //Primero deja todo visible
    for (let i = 1; i < listaopcionees.length; i++) {
        listaopcionees[i].removeAttribute("hidden");
    }

    switch (caso) {
        case 1:    //CULTIVO > 0 FILTRAR SOLO POR CULTIVOS:
            for (let i = 1; i < listaopcionees.length; i++) {
                let cultivo = listaopcionees[i].dataset.cultivo;
                if (cultivo != idCultivo) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
 
        case 2:   //INSUMOS DE FINCA >0 FILTRAR SOLO POR INSUMOS DE FINCA:
            for (let i = 1; i < listaopcionees.length; i++) {
                let insumofinca = listaopcionees[i].dataset.insumofinca;
                if (insumofinca != idInsumoFinca) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;

        
        case 3:    //FILTRAR POR TODAS LAS CATEGORIAS
            for (let i = 1; i < listaopcionees.length; i++) {
                if (listaopcionees[i].dataset.cultivo != idCultivo  || listaopcionees[i].dataset.insumofinca != idInsumoFinca) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
    }
}


//+++++++++++++++++++++++++++++++++++ CONSULTAR Y FILTRAR HORAS DE TRABAJO +++++++++++++++++++++++++++++++++++++++++++++++

function filtrarDatosHoraTrabajo() {
    let id = document.getElementById("listaHorasTrabajo").value;
    let url = "http://localhost:8000/gerentes/horaTrabajo/";
    let datos = {
        'id': id,        
    };
    mensajeAjax(url, datos, filtrarDatosHoraTrabajoResp);

}

function filtrarDatosHoraTrabajoResp(data) {
  document.getElementById("listaCultivos").value = data['cultivo'];
  document.getElementById("listaCategHora").value = data['categHora'];
  document.getElementById("listaTrabajador").value = data['trabajador'];
  document.getElementById("duracionLabor").value =data['duracionLabor'];
  document.getElementById("fechaLabor").value =data['fechaLabor'];
  document.getElementById("costo").value =data['costo'];
  document.getElementById("tipoTrabajo").value =data['tipoTrabajo'];
  document.getElementById("observacLabor").value =data['observacLabor'];
}

function filtrarHorasTrabajo() {
    let idCultivo = document.getElementById('listaCultivos').value;
    let idCategHora = document.getElementById('listaCategHora').value;
    let idTrabajador = document.getElementById('listaTrabajador').value;
    let listaopcionees = document.getElementById('listaHorasTrabajo').options;

    let caso = 0
    if ( idCategHora > '0') caso += 1;
    if ( idCultivo > '0') caso += 2;
    if ( idTrabajador > '0') caso += 3;
    
    //Primero deja todo visible
    for (let i = 1; i < listaopcionees.length; i++) {
        listaopcionees[i].removeAttribute("hidden");
    }

    switch (caso) {
        case 1:    //CATEGHORA >0, CATEG HORA = 0, TRABAJADORES = 0 : FILTRAR SOLO POR CATEGHORA
            for (let i = 1; i < listaopcionees.length; i++) {
                let categHora = listaopcionees[i].dataset.categhora;
                if (categHora != idCategHora) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
 
        case 2:   //CULTIVO >0, CATEG HORA = 0, TRABAJADOR = 0 : FILTRAR SOLO POR CULTIVO
            for (let i = 1; i < listaopcionees.length; i++) {
                let cultivo = listaopcionees[i].dataset.cultivo;
                if (cultivo != idCultivo) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;

        case 3:   //PROVEEDORES >0, EQUIPO = 0, EQUIPOFINCA = 0 : FILTRAR SOLO POR PROVEEDORES
            for (let i = 1; i < listaopcionees.length; i++) {
                let trabajador = listaopcionees[i].dataset.trabajador;
                if (trabajador != idTrabajador) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
        
        case 4, 5, 6:    //FILTRAR POR TODAS LAS CATEGORIAS
            for (let i = 1; i < listaopcionees.length; i++) {
                if (listaopcionees[i].dataset.categhora != idCategHora  || listaopcionees[i].dataset.cultivo != idCultivo || listaopcionees[i].dataset.trabajador != idTrabajador) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
    }
}

//+++++++++++++++++++++++++++++++++++ CONSULTAR Y FILTRAR VENTAS +++++++++++++++++++++++++++++++++++++++++++++++

function filtrarDatosVentas() {
    let id = document.getElementById("listaVentas").value;
    let url = "http://localhost:8000/gerentes/ventas/";
    let datos = {
        'id': id,        
    };
    mensajeAjax(url, datos, filtrarDatosVentasResp);

}

function filtrarDatosVentasResp(data) {
  document.getElementById("listaProducto").value = data['producto'];
  document.getElementById("listaCliente").value = data['cliente'];
  document.getElementById("numFactura").value =data['numFactura'];
  document.getElementById("fechaventa").value =data['fechaventa'];
  document.getElementById("cantidadVenta").value =data['cantidadVenta'];
  document.getElementById("observacVenta").value =data['observacVenta'];
  document.getElementById("valorTotalVentas").value =data['valorTotalVentas'];
}

function filtrarVentas() {
    let idCliente = document.getElementById('listaCliente').value;
    let idProducto = document.getElementById('listaProducto').value;
    let listaopcionees = document.getElementById('listaVentas').options;

    let caso = 0
    if ( idProducto > '0') caso += 1;
    if ( idCliente > '0') caso += 2;
    
    //Primero deja todo visible
    for (let i = 1; i < listaopcionees.length; i++) {
        listaopcionees[i].removeAttribute("hidden");
    }

    switch (caso) {
        case 1:    //PRODUCTO > 0 FILTRAR SOLO POR PRODUCTO:
            for (let i = 1; i < listaopcionees.length; i++) {
                let producto = listaopcionees[i].dataset.producto;
                if (producto != idProducto) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
 
        case 2:   //CLIENTE >0 FILTRAR SOLO POR EQUIPO DE CLIENTE:
            for (let i = 1; i < listaopcionees.length; i++) {
                let cliente = listaopcionees[i].dataset.cliente;
                if (cliente != idCliente) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;

        
        case 3:    //FILTRAR POR TODAS LAS CATEGORIAS
            for (let i = 1; i < listaopcionees.length; i++) {
                if (listaopcionees[i].dataset.producto != idProducto  || listaopcionees[i].dataset.cliente != idCliente) {
                    listaopcionees[i].setAttribute("hidden", "hidden");
                } 
            }
            break;
    }
}