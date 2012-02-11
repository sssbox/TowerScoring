function update_timer(data){
    console.log(data) ;
    $("#timer_title").text(data.practice + " Match " + data.match.id) ;
    $("#timer_main_timer").text(data.timer) ;
    $("#timer_red_score").text(data.match.red_score) ;
    $("#timer_blue_score").text(data.match.blue_score) ;

    var timer_cell = $("#timer_blue_on_center") ;
    if(data.blue_timer == '00') {
        timer_cell.text('') ;
        timer_cell.parents('.third-wide-edges').removeClass('blue').removeClass('border-top') ;
    } else {
        timer_cell.text(data.blue_timer) ;
        timer_cell.parents('.third-wide-edges').addClass('blue').addClass('border-top') ;
    }
    var timer_cell = $("#timer_red_on_center") ;
    if(data.red_timer == '00') {
        timer_cell.text('') ;
        timer_cell.parents('.third-wide-edges').removeClass('red').removeClass('border-top') ;
    } else {
        timer_cell.text(data.red_timer) ;
        timer_cell.parents('.third-wide-edges').addClass('red').addClass('border-top') ;
    }
}
