var jwt = null
function secure_get_with_token(endpoint, data_to_send, on_success_callback, on_fail_callback){
	xhr = new XMLHttpRequest();
	function setHeader(xhr) {
		xhr.setRequestHeader('Authorization', 'Bearer:'+jwt);
	}
	function get_and_set_new_jwt(data){
		console.log(data);
		jwt  = data.token
		on_success_callback(data)
	}
	$.ajax({
		url: endpoint,
		data : data_to_send,
	    'Content-Type': 'application/json',
	        type: 'GET',
		datatype: 'json',
		success: on_success_callback,
		error: on_fail_callback,
		beforeSend: setHeader
	});
}
function secure_post_with_token_with_fetch(endpoint, data_to_send, on_success_callback, on_fail_callback){

  xhr = new XMLHttpRequest();
        function setHeader(xhr) {
                xhr.setRequestHeader('Authorization', 'Bearer:'+jwt);
        }
        function get_and_set_new_jwt(data){
                console.log(data);
                jwt  = data.token
                on_success_callback(data)
        }
        $.ajax({
                url: endpoint,
                data : data_to_send,
            'Content-Type': 'application/json',
                type: 'POST',
                datatype: 'json',
                success: on_success_callback,
                error: on_fail_callback,
                beforeSend: setHeader
        });
    
    /*fetch(endpoint, {
                  method: 'POST', // or 'PUT'                                                                                                                                                                                         
                  headers: {
                      'Content-Type': 'application/json',
                  },
                  body: JSON.stringify(data),
              })
                  .then(response => response.json())
                  .then(data => {
                      console.log('Success:', on_success_callback);
                  })
                  .catch((error) => {
                      console.error('Error:', on_fail_callback);
                  });

    
    xhr = new XMLHttpRequest();
        function setHeader(xhr) {
                xhr.setRequestHeader('Authorization', 'Bearer:'+jwt);
        }
        function get_and_set_new_jwt(data){
                console.log(data);
                jwt  = data.token
                on_success_callback(data)
        }
        $.ajax({
                url: endpoint,
                data : data_to_send,
                type: 'POST',
                datatype: 'json',
                success: on_success_callback,
                error: on_fail_callback,
                beforeSend: setHeader
        });*/
}


