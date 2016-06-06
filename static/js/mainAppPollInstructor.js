var choice;
var choiceText;
var showCorrect = false;
var pollQuestions = [
  'Attendance',
  'When should the next quiz be?',
  'Which of the following is NOT a UML model?',
  'Who is known as the godmother of software engineering?'
];


var bar_data = {
    data: [["Sunday",1],["Monday", 10], ["Tuesday", 8], ["Wednesday", 4], ["Thursday",2],["Friday", 13],["Saturday",25]],
    color: "#3c8dbc"
  };

$(window).load(function(){
  $('#submitAnswerBtn').hide();
  $('#stopPollBtn').hide();
  $('#quiz-confirmation').hide();
});

var resetPoll = function(){
  /*Populate the menu with a list of polls for the Instructor to select from*/
  console.log("resetPoll ");
  $('#quiz').show();
  $('#submitAnswerBtn').hide();
  $('#stopPollBtn').hide();
  $('#quiz-confirmation').hide();
  $('#quiz').empty();
  /*Somewhere here, the database must be called to in order to fetch the polls.*/
  for(var i = 0; i<pollQuestions.length; i++){
    console.log(i);
    var pollQuestionID = i + 1;
    var pollQuestion = pollQuestions[i];
    var pollhtml =
    '<label class="element-animation1 btn btn-lg btn-primary btn-block" onclick="onPollOptionClick(this)">' +
      '<span class="btn-label">' +
        '<i class="glyphicon glyphicon-chevron-right"></i>' +
      '</span>' +
      '<input type="radio" name="q_answer" value="'+ (pollQuestionID) +'">' + '<div class="choiceText">'+ pollQuestion + '</div>' +
    '</label>';
    console.log(pollhtml);
    $("#quiz").append(pollhtml);
  }
}

var onPollOptionClick= function(clickedTarg){
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
      /*This is where the professor will make a call to the backend to start a poll*/
      $('#loadbar').show();
      $('#submitAnswerBtn').hide();
      $('#quiz').fadeOut();
      setTimeout(function(){
            if (showCorrect){$( "#answer" ).html(  $(this).checking(choice) );}
            $('#quiz-confirmation').fadeIn();
            updateChartData();
            $('#stopPollBtn').fadeIn();
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

var updateChartData = function() {
  /*BAR CHART*/



    $.plot("#bar-chart", [bar_data], {
      grid: {
        borderWidth: 1,
        borderColor: "#f3f3f3",
        tickColor: "#f3f3f3"
      },
      series: {
        bars: {
          show: true,
          barWidth: (3.25 / bar_data["data"].length),
          align: "center"
        }
      },
      xaxis: {
        mode: "categories",
        tickLength: 0
      }
    });
    /* END BAR CHART */
}
