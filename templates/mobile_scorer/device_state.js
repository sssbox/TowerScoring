
var device_state = {
    current_state: 'none',
    server_state: 'none',
    is_low: {% if is_low %}true{% else %}false{% endif %},
    is_red: {% if is_red %}true{% else %}false{% endif %},
    tower_code: '{{ tower_name }}',
    match_number: 'x',
    update_title: function(){
        var name = (device_state.is_red) ? 'Red ' : 'Blue ' ;
        name += (device_state.is_low) ? 'Short' : 'Tall' ;
        $("#controller_name").text(name) ;
        $("span.match_number").text(device_state.match_number) ;
    },
    update_tower: function(){
        if(device_state.is_low) {
            $("div.controller-area div.normal-state").removeClass('thirds').addClass('halves') ;
            $("div.controller-area div.center-state").removeClass('whole').addClass('halves') ;
            $("div.hide_for_low").hide() ;
            $("div.hide_for_high").show() ;
        } else {
            $("div.controller-area div.normal-state").removeClass('halves').addClass('thirds') ;
            $("div.controller-area div.center-state").removeClass('halves').addClass('whole') ;
            $("div.hide_for_low").show() ;
            $("div.hide_for_high").hide() ;
        }
        if(device_state.is_red) {
            $("div.center-state div.scoring_cell").removeClass('blue').addClass('red') ;
            $("div.normal-state div.non_dominant_scoring_col div.scoring_cell")
                .removeClass('red').addClass('blue') ;
            $("div.normal-state div.dominant_scoring_col div.scoring_cell")
                .removeClass('blue').addClass('red') ;
        } else {
            $("div.center-state div.scoring_cell").removeClass('red').addClass('blue') ;
            $("div.normal-state div.non_dominant_scoring_col div.scoring_cell")
                .removeClass('blue').addClass('red') ;
            $("div.normal-state div.dominant_scoring_col div.scoring_cell")
                .removeClass('red').addClass('blue') ;
        }
        device_state.update_title() ;
    },
    change_state: function(){
        console.log(device_state.server_state) ;
        if(device_state.current_state == '')
            $("div.initial-state").hide() ;
        if((device_state.server_state == 'normal' 
            || device_state.server_state == 'match_done_not_confirmed')
                && device_state.current_state != 'normal'
                && device_state.current_state != 'center')
        {
            $("div.state").hide() ;
            $("div.normal-state").show() ;
            if(device_state.server_state != 'match_done_not_confirmed')
                $("div.confirm-match-score").hide() ;
            device_state.current_state = 'normal' ;
        }
        if(device_state.server_state == 'match_done_not_confirmed')
        {
            $("div.confirm-match-score").show() ;
            device_state.current_state = 'match_done_not_confirmed' ; 
        }
        else if(device_state.server_state == 'center' )
        {
            $("div.state").hide() ;
            $("div.return-to-normal").hide() ;
            $("div.confirm-match-score").hide() ;
            $("div.center-state").show() ;
            $("div.score_count div.vcenter").text('0');
            device_state.current_state = 'center' ;
        }
        else if(device_state.server_state == 'match_done_confirmed')
        {
            $("div.state").hide() ;
            $("div.match-done-confirmed-state").show() ;
            device_state.current_state = 'match_done_confirmed' ;
        }
        else if(device_state.server_state == 'prematch')
        {
            $("div.state").hide() ;
            $("div.prematch-state").show() ;
            device_state.current_state = 'prematch' ;
        }
        else if(device_state.server_state == 'no_match' 
            && device_state.current_state != 'no_match_reload')
        {
            $("div.state").hide() ;
            $("div.no-match-state").show() ;
            device_state.current_state = 'no_match' ;
        }
        else if(device_state.server_state == 'normal_center_not_confirmed')
        {
            $("div.confirm-match-score").hide() ;
            $("div.return-to-normal").show() ;
            if(device_state.current_state != 'center')
            {
                $("div.state").hide() ;
                $("div.center-state").show() ;
                $("div.score_count div.vcenter").text('0');
            }
            device_state.current_state = 'normal_center_not_confirmed' ;
        }
    },
    update: function(data){
        if(device_state.is_low != data.is_low || device_state.is_red != data.is_red || device_state.match_number != data.match_number)
        {
            device_state.is_low = data.is_low ;
            device_state.is_red = data.is_red ;
            device_state.match_number = data.match_number ;
            device_state.update_tower() ;
        }
        device_state.server_state = data.state ;
        device_state.tower_code = data.tower_name ;
        if(device_state.current_state != device_state.server_state)
            device_state.change_state() ;
    }
}
    
