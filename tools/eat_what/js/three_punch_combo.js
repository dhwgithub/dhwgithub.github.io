$i = 0;
$('#start').click(function(){
    $i++;
    if($i >=6 ){
        $('#start').hide();
        $('#stop').show();
    }
})
$('#stop').click(function(){
    alert('要求还真高，别吃了！')
    $(this).hide();
})