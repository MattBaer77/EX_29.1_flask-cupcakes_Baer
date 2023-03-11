
const BASE_URL = "http://127.0.0.1:5000/api";

// Create HTML for Cupcake list item

function createCupcakeHTML(cupcake) {
    return `
        <div class="m-5" data-cupcake-id=${cupcake.id}>
            <li>
                ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
                <button class="delete btn btn-danger">X</button>
            </li>
            <img class="Cupcake-img m-3 w-25"src="${cupcake.image}"alt="(no image provided)">
        </div>
    `;
}

// Get the cupcakes from API

async function getCupcakes() {
    const resp = await axios.get(`${BASE_URL}/cupcakes`);

    for (let cake of resp.data.cupcakes) {

        $("#all-cupcakes-list").append($(createCupcakeHTML(cake)));

    }

}

// Submit Cupcake Form

$("#new-cupcake-form").on("submit", async function(evt){
    evt.preventDefault();

    let flavor = $('#flavor').val()
    let size = $('#size').val()
    let rating = $('#rating').val()
    let image = $('#image').val()

    data = {
        flavor : flavor,
        size : size,
        rating: rating,
        image: image
    };

    resp = await axios.post(`${BASE_URL}/cupcakes`, data)

    $("#all-cupcakes-list").append($(createCupcakeHTML(resp.data.cupcake)))

})

// Delete Cupcake

$("#all-cupcakes-list").on('click','.delete', async function(evt){
    evt.preventDefault();
    let $cakeToDelete = $(evt.target).closest("div");
    let cakeToDeleteId = $cakeToDelete.attr("data-cupcake-id")

    console.log(cakeToDeleteId)

    await axios.delete(`${BASE_URL}/cupcakes/${cakeToDeleteId}`)

    $cakeToDelete.remove()

})

$(getCupcakes)