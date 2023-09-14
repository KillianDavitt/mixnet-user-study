import * as Automerge from '@automerge/automerge'
var poissonProcess = require('poisson-process');

let pdoc = Automerge.init()
let sdoc = Automerge.clone(pdoc)
let userTokens = 6;

const numQuestions = 14
var typingDelayParam = 700

var numVisible = 2

pdoc = Automerge.change(pdoc, 'Create textboxes', pdoc => {
    pdoc.q=Array(numQuestions).fill(new Automerge.Text(""))
})


sdoc = Automerge.merge(sdoc,pdoc)


function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

// The answers to the questions are populated by the flask template
// so we fetch them from the dom
let answers = [numQuestions-1]
for(var i=0; i<numQuestions; i++){
    answers[i]=document.getElementById(`answer${i}`).getAttribute('answer')
}

const letters = answers.map(s => Array.from(s))

function myDelay(timer) {
    return new Promise(resolve => {
        timer = timer || 2000;
        setTimeout(function () {
            resolve();
        }, timer);
    });
};

const updateValue = async (strings = letters, word = [], id) => {
    // This delay simulates typing delay, not network delay
    let typingDelay = poissonProcess.sample(typingDelayParam)

    // If exhausted current word, select a new word
    if (word.length == 0) {
	var pick = 0;
	do {
	    await myDelay(200)
	    if (strings.length === 0) {
		return
	    }
	    pick = getRandomInt(strings.length)
	    //changed this
	    word = strings[pick]
	    id = letters.indexOf(word)
	} while (sdoc.q[id].toString()!="" || id>=numVisible)
	strings = [...strings.slice(0,pick),...strings.slice(pick+1)]
    }
    
    const input = document.getElementById(`answer${id}`)
    const [letter,...rest] = word

    while (userTokens<1) {
	await myDelay(2000)
	//console.log("reduced")
	typingDelayParam+=30
    }
    setTimeout(() => {
	var tmp;
	// Check if current value is a substring of end value
	if (!(letters[id].join('').trim().includes(sdoc.q[id].toString().trim()))){
	    // Theres a conflict, wait x seconds for the user to fix the box
	    tmp = sdoc.q[id].toString().trim()
	    //setTimeout(() => {
	    // Check if the user is typing...
	//	if(!(tmp==sdoc.q[id].toString().trim())){//(letters[id].join('').trim().includes(sdoc.q[id].toString().trim()))){
		// Conflict fixed, mark this word as finished and move to next
		// This should all the fun with blank word and cause it to pick a new one
		// Then return to stop this word completing...
		    updateValue(strings, '', id)
		    return
	/*	} else {
		    // Conflict still exists, user must have backed off
		    // Delete contents of box and start typing again.
		    let networkDelay = poissonProcess.sample(delayParam)
		    sdoc = Automerge.change(sdoc, 'delete and start again', doc => {
			var l=doc.q[id].length;
			var j=0;
			while(j<i){
			    doc.q[id].deleteAt(0);
			    j++;
			}
		    })
		    setTimeout(() => {
			pdoc = Automerge.merge(pdoc, sdoc)
			sdoc = Automerge.merge(sdoc,pdoc)
			input.value = pdoc.q[id]

		    }, networkDelay)
		    updateValue(strings, letters[id], id)
		    return 
		}
	  */  
	  //  },3000)//
	    return
	}

	updateValue(strings, rest, id)
	let p = Math.random()
	if (p<0.1){
	    userTokens-=2
	} else if(p<0.9){
	    userTokens-=1
	}

	
	sdoc = Automerge.change(sdoc, 'Add letter', doc => {
	    doc.q[id].insertAt(doc.q[id].length, letter)
	})

	// Network delay
	let networkDelay = poissonProcess.sample(delayParam)
	// Merge CRDTs
	setTimeout(() => {
	    pdoc = Automerge.merge(pdoc, sdoc)
	    sdoc = Automerge.merge(sdoc,pdoc)
	    input.value = pdoc.q[id]

	}, networkDelay)

	
    }, typingDelay)
    
}



for (var i=0; i<numQuestions;i++){
    let typeInput = document.getElementById(`answer${i}`)
    
    typeInput.addEventListener( "input" ,
			   (e) => {

			       // Participants has typed, add a token or the script
			       userTokens+=1;
			       if (userTokens>10){
				   typingDelayParam-=5
				   //console.log("increased")
			       }
			       // Add leter to crdt
			       pdoc = Automerge.change(pdoc, 'Add letter', doc => {
				   var num = e.target.getAttribute('num')
				   try{
				       doc.q[num].insertAt(doc.q[num].length, e.data)

				   }
				   catch(err){
				       console.log(typeof(e.data))
				       console.log(err.message)
				       console.log(num)
				       console.log(doc.q[num].length)
				   }
			       })


			       // Delay
			       let delay = poissonProcess.sample(delayParam)
			       // Merge CRDTs
			       setTimeout(() => {
				   sdoc = Automerge.merge(sdoc, pdoc)
				   pdoc = Automerge.merge(pdoc, sdoc)

			       }, delay)
			   })
}


let startInput = document.querySelector("#start")
if (startInput){
startInput.onclick = (ev) => {
  ev.preventDefault()
    updateValue()
}
}
function clearAll(){
    for (var i=0; i<answers.length;i++){
	document.getElementById(`answer${i}`).value='';
    }
}

let clearInput = document.querySelector("#clear")
if (clearInput){
clearInput.onclick = (ev) => {
  ev.preventDefault()
    clearAll()
}
}



document.getElementById("submit_button").addEventListener("click", function (event) {
        event.preventDefault();
    saveAutomergeData()
        document.getElementById("questions_form").submit();
    });

if (delayParam != 0) {
     setTimeout(() => {
	 updateValue()
     },250)
}

function saveAutomergeData(){
    console.log("Saving Automerge data...")
    let binary = Automerge.save(sdoc)
    document.getElementById("automerge_data").value=binary.toString()
    
    return
}

function revealQuestion(classn){
    var elems = document.getElementsByClassName(classn)
    for(var i=0; i<elems.length; i++){ 
	elems[i].style.opacity = '100';
    }
}

async function scanQuestions(){
    while (true) {
    // are the previous questions full
	var done = false
	var elems = document.getElementsByClassName('qinputs');
	for(var i=0; i<numVisible; i++){
	    if(elems[i].value==''){
		
		done=true
		break
	    }
	}
	// if yes make the next 2 visible
	if(done==false){
	    
	    for(var i=numVisible; i<numVisible+2 && i<numQuestions; i++){
		//console.log("revealing: " + elems[i].id)
		revealQuestion(elems[i].parentElement.className)
	    }

	    if(numVisible>=numQuestions){
		document.getElementById('submit_button').style.opacity = '100';
		return
	    } else{
		numVisible+=2
	    }
	}

	// if no, wait 5 seconds
	if(done==true){
	    await myDelay(1000)
	}
    }
}

scanQuestions()
