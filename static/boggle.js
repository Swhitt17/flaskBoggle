class BoggleGame{

constructor(boardId, secs = 60){
    this.secs = secs;
    this.showTimer();
    this.score = 0; 
    this.words = new Set();
    this.board = $("#" + boardId);

    this.timer = setInterval(this.tick.bind(this),1000);
    $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
   

}
showWord(word){
    $(".words", this.board).append($("<li>", {text:word}));
}
showScore(){
    $(".score", this.board).text(this.score);
}


showMessage(msg,cls){
    $(".msg", this.board)
    .text(msg)
    .removeClass()
    .addClass(`msg ${cls}`);
}

 async handleSubmit(e){
    e.preventDefault();
    const $word = $(".word", this.board);
     let word = $word.val();
    const res = await axios.post("/check-guess", {guess: word });
    console.log(res);

    console.log(word);

    if(!word) return;

    if (this.words.has(word)) {
      this.showMessage(`${word} has already been found`, "err");
      return;
    }

     resp = await axios.get("/check-guess", {params: {word: word}});
    if (resp.data.result === "not-word"){
        this.showMessage(`${word} is not a valid word`, "err"); 
    } 
    else if (resp.data.result === "not-on-board"){
        this.showMessage(`${word} is not a valid word for this board`, "err"); 
    } 

    else{
        this.showWord(word);
        this.words.add(word);
        this.showMessage(`${word} had been added`, "OK");
    }

    $word.val("").focus();

}
 showTimer(){
    $(".timer", this.board).text(this.timer);
 }

 async tick(){
    this.secs -= 1;
    this.showTimer();
     if (this.secs === 0){
        clearInterval(this.timer);
        await this.scoreGame();
     }
 }



async scoreGame(){
    $(".add-word", this.board).hide();
    resp = await axios.post("/post-score", {score:this.score});
    if (resp.data.brokeRecord){
        this.showMessage(`New Record: ${this.score}`, "ok");
     } 
      else{
        this.showMessage(`Final Score: ${this.score}`, "ok");

        }
    
  }
}
// const boggle = new BoggleGame()


// const bForm = document.querySelector(".add-word");
// const input = document.querySelector(".word");
// const  handleSubmit = async (e) => { 
//      e.preventDefault();
//      const res = await axios.post("/check-guess", {guess: input.value })
   
//     console.log(res);
    
// }
// bForm.addEventListener("submit", handleSubmit)







