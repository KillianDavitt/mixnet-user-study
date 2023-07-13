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
//var data = "MTMzLDExMSw3NCwxMzEsMTY0LDI1MSw5NiwxMjcsMCwxNDIsMiwyLDE2LDEwMiw4Myw1NCwxNCwxMjksMTQzLDc2LDE5NywxNjgsNjcsMTAxLDg1LDk4LDExNiwxNTUsNjcsMTYsMTA0LDI0MiwxMTEsMjA3LDMyLDk1LDc2LDE2MSwxNDcsMTkyLDIwOSwxNjMsMTcxLDQsMTg1LDQ4LDEsMTEwLDEyNywxMDksMTgwLDEzMSwxNTMsMjU1LDE0NCw0MCwyMDQsMjA5LDU0LDExMyw3NSwxMzAsMTczLDc2LDIzMyw3OSwyMjcsMTQ3LDIyNywyMzEsNjIsMTAzLDE4MiwxODAsMSw0LDE0Myw2MSwxMjcsOCwxLDQsMyw1LDE5LDQsMzUsMiw1MywzMCw2NCw0LDY3LDQsODYsMiwxMiwxLDQsMiwxMCwxNywxNiwxOSwyMiwyMSw1LDMzLDQsMzUsMTAsNTIsMiw2Niw2LDg2LDQsODcsMTgsMTI4LDEsMiwxMjcsMSwxOCwwLDEyNiwxLDAsMTcsMSwxMjcsMTEsMTgsMSwxOSwwLDEyNywxNiw2NywxMTQsMTAxLDk3LDExNiwxMDEsMzIsMTE2LDEwMSwxMjAsMTE2LDk4LDExMSwxMjAsMTAxLDExNSwxOCwxMCw2NSwxMDAsMTAwLDMyLDEwOCwxMDEsMTE2LDExNiwxMDEsMTE0LDEyNywwLDE4LDEsMTI3LDAsMTcsMSwxOSw3LDAsMSwyOCwxLDAsMSwxMCwxLDYsMiw1LDcsNywxMSwwLDIsOSwxLDAsMSw1LDAsMCwxLDQsMCwwLDEsNiwwLDAsMSwxMjYsMCwyLDgsMSwxMjYsMTE4LDEyLDQsMSwxMjYsMTEyLDI1LDMsMSwxMjYsMTAwLDE4LDUsMSwxMjcsMSwxMTMsMCwyOCwxMSwxLDE4LDAsMTcsMSwxMjcsOCw0LDEsMTI3LDExNyw2LDEsMSwyOCwxMjcsMiwxMCw0LDE4LDEsMTEsMCwxOCwyMiwzMiw4NCwxMTEsMTA3LDEyMSwxMTEsMzIsNjYsMTE0LDExNywxMTUsNjksMTEwLDEwMywxMDgsMTA1LDExNSwxMDQsMjksMCwxOA=="

var data = "133,111,74,131,209,2,148,1,0,224,1,2,16,91,196,24,19,118,96,71,33,174,185,243,167,195,92,109,207,16,139,71,20,222,142,151,76,105,147,56,94,105,210,211,34,87,1,36,72,167,125,212,253,165,234,106,19,13,89,130,28,113,169,249,235,102,212,172,94,111,46,170,255,140,183,164,4,236,182,8,1,4,3,5,19,4,35,2,53,30,64,4,67,4,86,2,12,1,4,2,6,17,8,19,11,21,5,33,4,35,2,52,2,66,6,86,4,87,3,128,1,2,127,1,3,0,126,1,0,2,1,127,11,3,1,4,0,127,16,67,114,101,97,116,101,32,116,101,120,116,98,111,120,101,115,3,10,65,100,100,32,108,101,116,116,101,114,127,0,3,1,127,0,2,1,4,7,0,1,13,1,0,1,10,1,3,8,0,2,9,1,0,1,2,0,0,1,126,0,2,8,1,125,118,12,1,127,1,113,0,13,11,1,3,0,14,1,1,13,127,2,10,4,3,1,11,0,3,22,32,66,108,14,0,3"
var nums = data.split(',').map(function(item) {
    return parseInt(item, 10);
});

var arr = Uint8Array.from(nums);

var a = Automerge.load(arr)
document.getElementById("submit_button").addEventListener("click", function (event) {
        event.preventDefault();
    saveAutomergeData()
        document.getElementById("questions_form").submit();
    });

updateValue()


function saveAutomergeData(){
    console.log("Saving Automerge data...")
    let binary = Automerge.save(sdoc)
    document.getElementById("automerge_data").value=binary.toString()
    
    return
}
