$(document).ready(function() {
    $('#search-form input, #search-form select').on('input change', function() {
        $.ajax({
            url: "{% url 'property_list' %}",
            type: "GET",
            data: {
                q: $('#search-query').val(),
                location: $('#search-location').val(),
                category: $('#search-category').val(),
                price_min: $('#search-price-min').val(),
                price_max: $('#search-price-max').val()
            },
            success: function(response) {
                let resultsContainer = $('#search-results');
                resultsContainer.empty();
                response.properties.forEach(property => {
                    resultsContainer.append(`
                        <div class="property-card">
                            <h5>${property.title}</h5>
                            <p>${property.location} - ${property.price} - ${property.category}</p>
                        </div>
                    `);
                });
            }
        });
    });
});

// for sorting
document.addEventListener("DOMContentLoaded", function () {
    const searchForm = document.getElementById("search-form");

    searchForm.addEventListener("input", function () {
        const formData = new FormData(searchForm);
        const params = new URLSearchParams(formData).toString();

        fetch(`/properties/?${params}`, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
        .then(response => response.json())
        .then(data => {
            const resultsContainer = document.getElementById("search-results");
            resultsContainer.innerHTML = ""; // Clear previous results

            data.properties.forEach(property => {
                const propertyCard = `
                    <div class="property-card">
                        <h5>${property.title}</h5>
                        <p>${property.location} - ${property.price} - ${property.category}</p>
                    </div>
                `;
                resultsContainer.innerHTML += propertyCard;
            });
        });
    });
});