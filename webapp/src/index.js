import * as Automerge from '@automerge/automerge'
var poissonProcess = require('poisson-process');

let pdoc = Automerge.init()
let sdoc = Automerge.clone(pdoc)
let userTokens = 10;
const numQuestions = 10

pdoc = Automerge.change(pdoc, 'Create textboxes', pdoc => {
    pdoc.q=Array(10).fill(new Automerge.Text(""))
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
    let typingDelay = poissonProcess.sample(500)
   
    if (word.length == 0) {
	
	do {
	    if (strings.length === 0) {
		return
	    }
	    
	    const pick = getRandomInt(strings.length)
	    word = strings[pick]
	    strings = [...strings.slice(0,pick),...strings.slice(pick+1)]
	    id = letters.indexOf(word)
	} while (sdoc.q[id].toString()!="")
    }
    
    const input = document.getElementById(`answer${id}`)
    const [letter,...rest] = word

    while (userTokens<1) {
	await myDelay(1000)
    }
    setTimeout(() => {



	updateValue(strings, rest, id)
	let p = Math.random()
	if (p<0.1){
	    userTokens-=2
	} else if(p<0.6){
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
			       // Add leter to crdt
			       pdoc = Automerge.change(pdoc, 'Add letter', doc => {
				   console.log(doc.q)
				   var num = e.target.getAttribute('num')
				   console.log(num)
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

			       console.log(pdoc)

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
var data = "MTMzLDExMSw3NCwxMzEsMTY0LDI1MSw5NiwxMjcsMCwxNDIsMiwyLDE2LDEwMiw4Myw1NCwxNCwxMjksMTQzLDc2LDE5NywxNjgsNjcsMTAxLDg1LDk4LDExNiwxNTUsNjcsMTYsMTA0LDI0MiwxMTEsMjA3LDMyLDk1LDc2LDE2MSwxNDcsMTkyLDIwOSwxNjMsMTcxLDQsMTg1LDQ4LDEsMTEwLDEyNywxMDksMTgwLDEzMSwxNTMsMjU1LDE0NCw0MCwyMDQsMjA5LDU0LDExMyw3NSwxMzAsMTczLDc2LDIzMyw3OSwyMjcsMTQ3LDIyNywyMzEsNjIsMTAzLDE4MiwxODAsMSw0LDE0Myw2MSwxMjcsOCwxLDQsMyw1LDE5LDQsMzUsMiw1MywzMCw2NCw0LDY3LDQsODYsMiwxMiwxLDQsMiwxMCwxNywxNiwxOSwyMiwyMSw1LDMzLDQsMzUsMTAsNTIsMiw2Niw2LDg2LDQsODcsMTgsMTI4LDEsMiwxMjcsMSwxOCwwLDEyNiwxLDAsMTcsMSwxMjcsMTEsMTgsMSwxOSwwLDEyNywxNiw2NywxMTQsMTAxLDk3LDExNiwxMDEsMzIsMTE2LDEwMSwxMjAsMTE2LDk4LDExMSwxMjAsMTAxLDExNSwxOCwxMCw2NSwxMDAsMTAwLDMyLDEwOCwxMDEsMTE2LDExNiwxMDEsMTE0LDEyNywwLDE4LDEsMTI3LDAsMTcsMSwxOSw3LDAsMSwyOCwxLDAsMSwxMCwxLDYsMiw1LDcsNywxMSwwLDIsOSwxLDAsMSw1LDAsMCwxLDQsMCwwLDEsNiwwLDAsMSwxMjYsMCwyLDgsMSwxMjYsMTE4LDEyLDQsMSwxMjYsMTEyLDI1LDMsMSwxMjYsMTAwLDE4LDUsMSwxMjcsMSwxMTMsMCwyOCwxMSwxLDE4LDAsMTcsMSwxMjcsOCw0LDEsMTI3LDExNyw2LDEsMSwyOCwxMjcsMiwxMCw0LDE4LDEsMTEsMCwxOCwyMiwzMiw4NCwxMTEsMTA3LDEyMSwxMTEsMzIsNjYsMTE0LDExNywxMTUsNjksMTEwLDEwMywxMDgsMTA1LDExNSwxMDQsMjksMCwxOA=="
var d = atob(data)
var a = Automerge.load(d)
document.getElementById("submit_button").addEventListener("click", function (event) {
        event.preventDefault();
    saveAutomergeData()
        document.getElementById("questions_form").submit();
    });

updateValue()


function saveAutomergeData(){
    console.log("Saving Automerge data...")
    let binary = Automerge.save(sdoc)
    let base = btoa(binary)
    document.getElementById("automerge_data").value=base
    
    return
}
