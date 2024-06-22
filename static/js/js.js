const url_json = "data.json";

function noticias_nueva(url_json) {
  fetch(url_json)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);

      let titulo1 = data.infobae[data.infobae.length - 1].title;
      let imagen1 = data.infobae[data.infobae.length - 1].img_url;
      let url1 = data.infobae[data.infobae.length - 1].url;
      let alt_text1 = data.infobae[data.infobae.length - 1].alt_text;
      let source = data.infobae[data.infobae.length -1 ].source
      

      let titulo2 = data.Clarin[data.Clarin.length - 1].title;
      let imagen2 = data.Clarin[data.Clarin.length - 1].img_url;
      let url2 = data.Clarin[data.Clarin.length - 1].url;
      let alt_text2 = data.Clarin[data.Clarin.length - 1].alt_text;
      let source2 = data.Clarin[data.Clarin.length -1 ].source


      let titulo3 = data.LaNacion[data.LaNacion.length - 1].title;
      let imagen3 = data.LaNacion[data.LaNacion.length - 1].img_url;
      let url3 = data.LaNacion[data.LaNacion.length - 1].url;
      let alt_text3 = data.LaNacion[data.LaNacion.length - 1].alt_text;
      let source3 = data.LaNacion[data.LaNacion.length -1 ].source

      let titulo4 = data.TN[data.TN.length - 1].title;
      let imagen4 = data.TN[data.TN.length - 1].img_url;
      let url4 = data.TN[data.TN.length - 1].url;
      let alt_text4 = data.TN[data.TN.length - 1].alt_text;
      let source4 = data.TN[data.TN.length -1 ].source
      
      const contenedorInfobae = document.getElementById("contenedor-Infobae");

      const cardInfobae = `
        <div class="card mb-4 shadow-sm">
        <a href="${url1}" class="text-none">
              <img src="${imagen1}" class="card-img-top" alt="...">
                <div class="card-body">
                
                <h5 class="${titulo1}">Título de la Noticia</h5>
                    <p class="">${alt_text1}</p>
               
                    </div>
             </a>
             <p class="p-3"> Fuente: ${ source}</p>
        </div>
            `;
      contenedorInfobae.innerHTML = cardInfobae; // Usamos '=' para reemplazar el contenido en lugar de '+=' para evitar duplicaciones
    

      const contenedorClarin = document.getElementById("contenedor-Clarin")
      const cardClarin = `
        <div class="card mb-4 shadow-sm">
        <a href="${url2}" class="text-none">
              <img src="${imagen2}" class="card-img-top" alt="...">
                <div class="card-body">
                
                <h5 class="${titulo2}">Título de la Noticia</h5>
                    <p class="">${alt_text2}</p>
               
                    </div>
             </a>
             <p class="p-3"> Fuente: ${ source2}</p>
        </div>
            `;
      contenedorClarin.innerHTML = cardClarin;

      const contenedorTN = document.getElementById("contenedor-TN")
      const cardTN = `
        <div class="card mb-4 shadow-sm">
        <a href="${url3}" class="text-none">
              <img src="${imagen3}" class="card-img-top" alt="...">
                <div class="card-body">
                
                <h5 class="${titulo3}">Título de la Noticia</h5>
                    <p class="">${alt_text3}</p>
               
                    </div>
             </a>
             <p class="p-3"> Fuente: ${ source3}</p>
        </div>
            `;
      contenedorTN.innerHTML = cardTN;

      const contenedorLaNacion = document.getElementById("contenedor-LaNacion")
      const cardLaNacion = `
        <div class="card mb-4 shadow-sm">
        <a href="${url4}" class="text-none">
              <img src="${imagen4}" class="card-img-top" alt="...">
                <div class="card-body">
                
                <h5 class="${titulo4}">Título de la Noticia</h5>
                    <p class="">${alt_text4}</p>
               
                    </div>
             </a>
             <p class="p-3"> Fuente: ${ source4}</p>
        </div>
            `;
      contenedorLaNacion.innerHTML = cardLaNacion;
    
    
    })


    .catch((error) => {
      console.log("Error al cargar la noticia", error);
    });
}

noticias_nueva(url_json);
