//Dibuja las estrellas en funcion de la puntuacion del producto
function drawStars(rating) {
    const maxStars = 5;
    let starsHTML = '';
    const rounded = Math.round(rating);
    for (let i = 0; i < maxStars; i++) {
        if (i < rounded) {
            starsHTML += '<span class="fa fa-star checked"></span>';
        } else {
            starsHTML += '<span class="fa fa-star not_checked"></span>';
        }
    }
    return starsHTML;
}

function updateRating(elemento, newRating){

    const productId = elemento.getAttribute('data-product-id');
    fetch(`http://127.0.0.1:8000/etienda/api/puntuar/${productId}/${newRating}`, {method: 'PUT',})
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));

}


document.addEventListener('DOMContentLoaded', () => {
	// Obtener todos los elementos span con clase .sp
    const span_estrellas = document.querySelectorAll('span.sp');
	// Recorrer todos los elementos span con clase .sp
    span_estrellas.forEach((ele) => {
        const id = ele.dataset.productId;
		// Obtener el producto
        fetch(`http://127.0.0.1:8000/etienda/api/idproducto/${id}`)
            .then(res => res.json())
            .then(res => {
                const rating = res.rating.rate;
                ele.innerHTML = drawStars(rating);

				// Obtener todas las estrellas
                const stars = ele.querySelectorAll('.fa-star');
                stars.forEach((star, index) => {
                    star.addEventListener('click', () => {

                        // Actualizar la visualización de las estrellas
                        stars.forEach((s, i) => {
                            if (i <= index) {
                                s.classList.add('checked');
                                s.classList.remove('not_checked');
                            } else {
                                s.classList.add('not_checked');
                                s.classList.remove('checked');
                            }
                        });

                        // Enviar la nueva calificación a la API
                        updateRating(ele, index+1);
                    });
                });
            })
            .catch(error => alert(`Hay un ${error}.`));
    });
});