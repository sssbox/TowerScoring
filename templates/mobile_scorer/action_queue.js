
var ajax_in_process = false ;
var timeout = null ;

function do_ajax() {
    if(!ajax_in_process)
    {
        clearTimeout(timeout) ;
        ajax_in_process = true ;
        $.ajax({
            url: "{% url match_batch_actions %}",
            data: {'actions': JSON.stringify(actions.queue)},
            type: "GET",
            timeout: 500,
            success: function(data){
                if (data.success==true)
                {
                    if (data.action_ids)
                        actions.dequeue_successful_actions(data.action_ids) ;
                    device_state.update(data.scorer_data) ;
                    if (typeof(callback) == 'function') 
                        callback() ;
                    ajax_in_process = false ;
                    if(Object.keys(actions.queue).length > 0)
                        do_ajax() ;
                    else
                        timeout = setTimeout(do_ajax, 500);
                    last_valid_request = Math.round(new Date().getTime() / 10) ;
                }
            },
            error: function(x, e){
                if (e === 'parsererror')
                    display_error('Invalid JSON returned.') ;
                else if (e === 'timeout')
                    display_error('Timed out.') ;
                else if (e === 'abort')
                    display_error('Ajax request aborted.');
                else if (x.status == 0)
                    display_error('Lost connection.') ;
                else if (x.hasOwnProperty('status'))
                {
                    try
                    {
                        if (x.status == 404)
                            display_error('Got a 404 error.') ;
                        else if (x.status == 500)
                            display_error('Internal server error.') ;
                        else
                            display_error('Unknown Error: ' + x.responseText) ;
                    } catch(whatever) {
                        display_error('Exception printing unknown error.') ;
                    }
                }
                else
                    display_error('Exception printing unknown error.') ;
                ajax_in_process = false ;
                timeout = setTimeout(do_ajax, 500);

            },
            cache: false
        });
    }
}

var actions = {
    next_id: {{ next_id }},
    queue: {},
    init: function(){
//        actions.next_id =
//        actions.queue =
        do_ajax() ;
    },
    update_local_store: function(){
// save actions.queue and actions.next_id
    },
    dequeue_successful_actions: function(action_ids){
        $.each(action_ids, function(done_id){
            delete actions.queue[action_ids[done_id]] ;
            actions.update_local_store() ;
        });
    },
    push: function(action, data, priority, callback){
        actions.queue[actions.next_id] = {action:action, data: data} ;
        actions.update_local_store() ;
        actions.next_id++ ;
        
        if(!ajax_in_process)
            do_ajax() ;
    }
}

actions.init()
