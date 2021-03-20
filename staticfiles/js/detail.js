function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).on('click', '#submit-btn', function(event){
    var data = $('.Storages');
    var storage_data = {};
    console.log(data);
    for(i=0;i<data.length;i++){
        console.log(i);
        var trucks_data = $(data[i]).find($(".Truck"));
        var str_data = $(data[i]).find(".Storage");
        console.log(str_data);
        var storage_id = str_data.find('#storage_id').text();
        for(j=0;j<trucks_data.length;j++){
            var truck_id = $(trucks_data[j]).find('#truck_id').text();
            var coordinate_x = $(trucks_data[j]).find('#point_x_input').val();
            var coordinate_y = $(trucks_data[j]).find('#point_y_input').val();
            if (storage_data[storage_id]) {
                storage_data[storage_id]["trucks_data"][truck_id] = {
                    "coordinate_x" : coordinate_x,
                    "coordinate_y" : coordinate_y,
                };
            } else {
                storage_data[storage_id] = {
                    'trucks_data': {}
                    };
                storage_data[storage_id]["trucks_data"][truck_id] = {
                    "coordinate_x" : coordinate_x,
                    "coordinate_y" : coordinate_y,
                };
            }
        }
    }
    response_data = {
        "storage_data":storage_data
    }
    $.ajax({
            type: "POST",
            url: "coordinate_update/",
            data: {data: JSON.stringify(response_data),
                //csrfmiddlewaretoken: '{{ csrf_token }}'},
                csrfmiddlewaretoken:  getCookie('csrftoken')},
            success: function(response){
                alert("Расчеты произведены, нажмите OK для загрузки");
                window.location.reload() 
            }
        });
});