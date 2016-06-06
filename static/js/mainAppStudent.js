var currentPage = 1;
var intervalID;
function start(){

if(PDFObject.supportsPDFs){
   console.log("Yay, this browser supports inline PDFs.");
} else {
   console.log("Boo, inline PDFs are not supported by this browser");
}
$("#takePollDisplay").toggle();
changePage(1);
setFrameOnAdjust();
//intervalID = setInterval(checkUpdate(),5000);

}

//setInterval(checkUpdate,5000);

function togglePoll(){
  $("#mainAppDisplay").toggle();
  $("#takePollDisplay").toggle();
  resetPoll();
}

function changePage(number){
var numval = String(number);
PDFObject.embed("../static/Planning.pdf", "#presentationFrame",{page: numval,height:"400px",width:"100%" });
}

function prevSlide(){
currentPage = currentPage - 1;
changePage(currentPage);
setFrameOnAdjust();
}

function nextSlide(){
currentPage = currentPage + 1;
changePage(currentPage);
setFrameOnAdjust();
}

function togglePanelBar(){
  console.log("toggleCalled");
  var windowHeight = $(window).height();
  var panelHeight = $("#bottomControlPanel").height();
  var newHeight = windowHeight - panelHeight;
  console.log($(window).height());
  console.log($("#bottomControlPanel").height());

  if (panelHeight < 50){
      setFrameHeight(windowHeight - 160);
  } else {
      setFrameHeight(windowHeight  - 160);
  }
}

function setFrameOnAdjust(){
  console.log("toggleCalled");
  var windowHeight = $(window).height();
  var panelHeight = $("#bottomControlPanel").height();
  //var newHeight = windowHeight - panelHeight;
  console.log($(window).height());
  console.log($("#bottomControlPanel").height());
  setFrameHeight(windowHeight - 135);
  windowHeight = $(window).height();
  setChatHeight( windowHeight - 625);
}



function setFrameHeight(number){
    console.log('setFrame: ',number);
  $("#presentationFrame > .pdfobject").height(number);
//  console.log($("#presentationFrame > .pdfobject").height());
}

function setChatHeight(number){
    console.log('setChat: ',number);
    $("#chatapp-im-disp").height(number);
}
$(window).resize(setFrameOnAdjust);

var checkUpdate = function() {
  console.log(" called CHECKUPDATE FUNCTION ");
}

/*Periodically Check to see if anything has changed on the server: */
setInterval(function(){
  console.log("Called CheckUpdate");
  checkUpdate();
}, 5000);
