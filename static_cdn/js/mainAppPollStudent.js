var choice;
var showCorrect = false;
var pollQuestion = "When should the next quiz be?";
var pollAnswers = [
  'Monday',
  'Tuesday',
  'Wednesday',
  'Friday'
];
$(window).load(function(){
  $('#submitAnswerBtn').hide();
  $('#quiz-confirmation').hide();

});

var resetPoll = function(){
  $('#quiz').show();
  $('#submitAnswerBtn').hide();
  $('#quiz-confirmation').hide();
  $('#pollQuestionField').empty();
  $('#pollQuestionField').append(pollQuestion);
  $('#quiz').empty();
  for(var i = 0; i<pollAnswers.length; i++){
    console.log(i);
    var pollAnswerID = i + 1;
    var pollAnswer = pollAnswers[i];
    var pollhtml =
    '<label class="element-animation1 btn btn-lg btn-primary btn-block" onclick="onAnswerClick(this)">' +
      '<span class="btn-label">' +
        '<i class="glyphicon glyphicon-chevron-right"></i>' +
      '</span>' +
      '<input type="radio" name="q_answer" value="'+ (pollAnswerID) +'">' + '<div class="choiceText">'+ pollAnswer + '</div>' +
    '</label>';
    console.log(pollhtml);
    $("#quiz").append(pollhtml);
  }
}

var onAnswerClick= function(clickedTarg){
  console.log(clickedTarg);
  choice = $(clickedTarg).find('input:radio').val();
  console.log(choice);
  $('#submitAnswerBtn').fadeIn();
}

$(function(){
    var loading = $('#loadbar').hide();
    $(document)
    .ajaxStart(function () {
        loading.show();
    }).ajaxStop(function () {
    	loading.hide();
    });

    $("label.btn").on('click',function () {
    	choice = $(this).find('input:radio').val();
      $('#submitAnswerBtn').fadeIn();
    });

    $("#submitAnswerBtn").on('click',function () {
      $('#loadbar').show();
      $('#submitAnswerBtn').hide();
      $('#quiz').fadeOut();
      setTimeout(function(){
            if (showCorrect){$( "#answer" ).html(  $(this).checking(choice) );}
            $('#quiz-confirmation').fadeIn();
            $('#loadbar').fadeOut();
           /* something else */
      }, 1500);
    });

    $ans = 3;

    $.fn.checking = function(ck) {
        if (ck != $ans)
            return 'INCORRECT';
        else
            return 'CORRECT';
    };
});
