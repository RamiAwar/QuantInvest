(function() {

  var risk_score = 0;


  var questions = [{
    question: "What is the amount of money you are willing to invest?",
    choices: ["< $1000", "$1000 - $9000", "$10,000 - $90,000", "$100,000 - $900,000", "> $1,000,000"],
    weights: [1, 2, 3, 5, 7]}
  // }, {
  //   question: "What percentage of your savings does this amount constitute?",
  //   choices: ["1% - 5%", "5% - 10%", "10% - 20%", "20% - 50%", "> 50%"],
  //   weights: [7, 5, 3, 2, 1]
  // }, {
  //   question: "What is your age range?",
  //   choices: ["< 20 years", "20 - 35 years", "36 - 50 years", "51 - 65 years", "> 65 years"],
  //   weights: [7, 5, 3, 2, 1]
  // },{
  //   question: "If your net portfolio value dropped by 2% after the market closed, how would you react?",
  //   choices: ["Sell all portfolio to prevent further losses", "Sell a portion of your portfolio", "Hold your investments and sell nothing, expecting conditions to improve", "Invest in more stocks, tolerating short term losses in hope of long term growth."],
  //   weights: [1, 3, 5, 7]
  // },


  ];

  explanation_text = "<br> This score represents how much you are willing to take risks in your investment. QuantInvest uses this score to generate a suitable investment profile for you. Click continue to see more details and experiment with different profiles.";
  
  var questionCounter = 0; //Tracks question number
  var selections = []; //Array containing user choices
  var quiz = $('#quiz'); //Quiz div object
  
  // Display initial question
  displayNext();
  
  // Click handler for the 'next' button
  $('#next').on('click', function (e) {
    e.preventDefault();
    
    // Suspend click listener during fade animation
    if(quiz.is(':animated')) {        
      return false;
    }

    choose();
    
    // If no user selection, progress is stopped
    if (isNaN(selections[questionCounter])) {
      alert('Please make a selection to continue');
    } else {
      questionCounter++;
      displayNext();
    }
  });
  
  // Click handler for the 'prev' button
  $('#prev').on('click', function (e) {
    e.preventDefault();
    
    if(quiz.is(':animated')) {
      return false;
    }
    choose();
    questionCounter--;
    displayNext();
  });
  
  // Click handler for the 'Start Over' button
  $('#start-over').on('click', function (e) {

    e.preventDefault();
    
    if(quiz.is(':animated')) {
      return false;
    }
    questionCounter = 0;
    selections = [];
    displayNext();
    $('#start-over').hide();

    risk_score = 0;
  });
  
  $('#end').on('click', function(e){
    form = $('<form action="' + CREATE_PROFILE_URL + '" method="POST">' + 
    '<input type="hidden" name="score" value="' + risk_score + '">' +
    '</form>');
    $(document.body).append(form);
    form.submit();


  })
  
  
  // Creates and returns the div that contains the questions and 
  // the answer selections
  function createQuestionElement(index) {
    var qElement = $('<div>', {
      id: 'question'
    });
    
    var header = $('<h2>Question ' + (index + 1) + ':</h2>');
    qElement.append(header);
    
    var question = $('<p>').append(questions[index].question);
    qElement.append(question);
    
    var radioButtons = createRadios(index);
    qElement.append(radioButtons);
    
    return qElement;
  }
  
  // Creates a list of the answer choices as radio inputs
  function createRadios(index) {
    var radioList = $('<div>');
    var item;
    var input = '';
    for (var i = 0; i < questions[index].choices.length; i++) {
      input = '<div class="form-check mb-3">' + 
        '<input type="radio" name="radios" class="form-check-input" value="' + i + '" />' +
        '<label class="form-check-label">'+ questions[index].choices[i] + '</label>'+
      '</div>';

      radioList.append(input);
    }
    return radioList;
  }
  
  // Reads the user selection and pushes the value to an array
  function choose() {
    selections[questionCounter] = +$('input[name="radios"]:checked').val();
    console.log(selections[questionCounter])
  }        
  
  // Displays next requested element
  function displayNext() {
    quiz.fadeOut(function() {
      $('#question').remove();
      
      if(questionCounter < questions.length){

        var nextQuestion = createQuestionElement(questionCounter);
        quiz.append(nextQuestion).fadeIn();
        
        if (!(isNaN(selections[questionCounter]))) {
          $('input[value='+selections[questionCounter]+']').prop('checked', true);
        }
        
        // Controls display of 'prev' button
        if(questionCounter === 1){

          $('#prev').show();

        } else if(questionCounter === 0){
          
          $('#prev').hide();
          $('#end').hide();
          $('#next').show();
        }

      }else {
        var scoreElem = displayScore();
        quiz.append(scoreElem).fadeIn();
        $('#next').hide();
        $('#prev').hide();
        $('#start-over').show();
        $('#end').show();

      }
    });
  }
  
  // Computes score and returns a paragraph element to be displayed
  function displayScore() {

    var score = $('<p>',{id: 'question'});
    
    for (var i = 0; i < selections.length; i++) {
      risk_score += questions[i].weights[selections[i]]
    }
    
    score.append('Your risk analysis score is ' + risk_score + explanation_text);


    //TODO: Add more detailed description of risk class and meaning : priority (1)

    return score;
  }
})();



