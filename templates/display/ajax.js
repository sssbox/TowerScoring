    var ajax_time = 100 ;
    function do_ajax() {
        $.ajax({
            url: "{% url display_update %}",
            data: {next_screen: next_screen, skip_to_screen: skip_to_screen},
            type: "GET",
            timeout: 500,
            success: function(data){
                next_screen = false ;
                skip_to_screen = '';
                if(data.display != current_screen)
                {
                    current_screen = data.display ;
                    $("div.all").hide() ;
                    $("div.all-"+data.display).show() ;
                }
                if(current_screen == 'timer')
                    update_timer(data) ;
                timeout = setTimeout(do_ajax, ajax_time);
            },
            error: function(x, e){
                timeout = setTimeout(do_ajax, ajax_time);
            },
            cache: false
        });
    }
    do_ajax() ;
