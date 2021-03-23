//test for iterating over child elements
var langArray = [];
$('#set_images option').each(function(){
  var img = $(this).attr("data-thumbnail");
  var font = $(this).attr("data-font");
  var translate = $(this).attr("data-translate");
  var text = this.innerText;
  
  var value = $(this).val();
  var item = '<li>'+
                '<a onclick="setSwitch(' + value + ');">'+
                    '<img src="'+ img +'" alt="" value="' + value + '" />'+
                    '<span class="'+ font + ' '+ translate +'">'+ text +'</span>'+
                '</a>'+
             '</li>';
  langArray.push(item);
})

$('#select_ul').html(langArray);

//Set the button value to the first el of the array
$('.btn-select').html(langArray[0]);
$('.btn-select').attr('value', 'en');

//change button stuff on click
$('#select_ul li').click(function(){
   var img = $(this).find('img').attr("src");
   var value = $(this).find('img').attr('value');
   var text = this.innerText;
   var item = '<li><img src="'+ img +'" alt="" /><span>'+ text +'</span></li>';
  $('.btn-select').html(item);
  $('.btn-select').attr('value', value);
  $(".select_div").toggle();
  //console.log(value);
});

$(".btn-select").click(function(){
        $(".select_div").toggle();
    });

//check local storage for the lang
var sessionLang = localStorage.getItem('lang');
if (sessionLang){
  //find an item with value of sessionLang
  var langIndex = langArray.indexOf(sessionLang);
  $('.btn-select').html(langArray[langIndex]);
  $('.btn-select').attr('value', sessionLang);
} else {
   var langIndex = langArray.indexOf('ch');
  console.log(langIndex);
  $('.btn-select').html(langArray[langIndex]);
  //$('.btn-select').attr('value', 'en');
}