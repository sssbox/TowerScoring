
var ajax_in_process = false ;

function do_ajax() {
    if(!ajax_in_process)
    {
        ajax_in_process = true ;
        $.ajax({
            url: "{% url match_batch_actions %}",
            data: {'actions': JSON.stringify(actions.queue)},
            type: "GET",
            success: function(data){
                if (data.success==true)
                {
                    if (data.action_ids)
                        actions.dequeue_successful_actions(data.action_ids) ;
                    if (typeof(callback) == 'function') 
                        callback() ;
                    ajax_in_process = false ;
                    if(Object.keys(actions.queue).length > 0)
                        do_ajax() ;
                }
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
