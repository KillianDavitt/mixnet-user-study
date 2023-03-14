import * as Automerge from '@automerge/automerge'
var poissonProcess = require('poisson-process');

let pdoc = Automerge.init()
let sdoc = Automerge.init()


pdoc = Automerge.change(pdoc, 'Add card', pdoc => {
    pdoc.q=Array(8).fill('')
})

sdoc = Automerge.change(sdoc, 'Add card', doc => {
    doc.q=Array(8).fill('')
})


pdoc = Automerge.change(pdoc, 'Mark card as done', pdoc => {
  pdoc.test = 'hi'
})

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

const answers = ["Vienna","London","Paris", "Madrid", "Berlin", "Rome", "Dublin", "Moscow"]

let copyOfAnswers = answers.map(s => Array.from(s))
const copy = copyOfAnswers.map(x => x)

/*
const updateValue = (pick = getRandomInt(letters.length), input = document.getElementById(`answer${pick}`)) => {
    // This delay simulates typing delay, not network delay
    console.log("Started update value")
    let delay = poissonProcess.sample(500)
    let id;
    id = copy.indexOf(letters[pick])
    console.log(id)
    console.log(pick)
    if (letters[pick].length == 0) {
	console.log("in if")
	letters.splice(pick, 1)
	delay+=1000
	if (letters.length === 0) {
	    return
	}
	
	do {
	    pick = getRandomInt(letters.length)
	    id = copy.indexOf(letters[pick])
	    input = document.getElementById(`answer${id}`)
	    if (sdoc.q[id]!=''){
		letters.splice(pick,1)
	    }
	} while (input.value!='')
    }

    const letter = letters[pick].splice(0, 1)
    console.log(letter)
    setTimeout(() => {
	
	sdoc = Automerge.change(sdoc, 'Add letter', doc => {
	    doc.q[id]+= letter
	})

	// Network delay
	let delay = poissonProcess.sample(5000)
	// Merge CRDTs
	setTimeout(() => {
	    pdoc = Automerge.merge(pdoc, sdoc)
	    input.value = pdoc.q[id]
	}, delay)
	
	updateValue(pick, input)
    }, delay)

}*/

const updateValue = (strings = copy, pick = getRandomInt(strings.length), input = document.getElementById(`answer${pick}`)) => {
    // This delay simulates typing delay, not network delay
    let delay = poissonProcess.sample(500)
    let id;
    id = copyOfAnswers.indexOf(strings[pick])
   
    if (strings[pick].length == 0) {

	strings.splice(pick, 1)
	delay+=1000
	if (strings.length === 0) {
	    return
	}
	
	do {
	    pick = getRandomInt(strings.length)
	    id = copyOfAnswers.indexOf(strings[pick])
	    input = document.getElementById(`answer${id}`)
	    if (sdoc.q[id]!=''){
		strings.splice(pick,1)
	    }
	} while (sdoc.q[id]!='')
    }

    const letter = strings[pick].splice(0, 1)
    console.log(letter)
    setTimeout(() => {
	
	sdoc = Automerge.change(sdoc, 'Add letter', doc => {
	    doc.q[id]+= letter
	})

	// Network delay
	let delay = poissonProcess.sample(5000)
	// Merge CRDTs
	setTimeout(() => {
	    pdoc = Automerge.merge(pdoc, sdoc)
	    input.value = pdoc.q[id]
	}, delay)
	let stringsCopy = strings.map(s => Array.from(s))
	updateValue(stringsCopy, pick, input)
    }, delay)

}



document.querySelector('#testbox').value=pdoc.test

const numQuestions = 7;

for (var i=0; i<numQuestions;i++){
    let typeInput = document.getElementById(`answer${i}`)
    console.log(`answer${i}`)
    console.log(pdoc.q[i])
    //typeInput.onkeydown = updateValue()
    typeInput.addEventListener( "keydown" ,
			   (e) => {
			       console.log(e.target)
			       console.log(e.key)
			       // Add leter to crdt
			       pdoc = Automerge.change(pdoc, 'Add letter', doc => {
				   doc.q[i]+=e.key
			       })
			       console.log(pdoc.q[i])
			       // Delay
			       let delay = poissonProcess.sample(1000)
			       // Merge CRDTs
			       setTimeout(() => {
				   sdoc = Automerge.merge(sdoc, pdoc)
			       }, delay)
			   })
}

function updateDoc(newDoc) {
  doc = newDoc
  render(newDoc)
}


let startInput = document.querySelector("#start")
startInput.onclick = (ev) => {
  ev.preventDefault()
    updateValue()
}



function clearAll(){
    for (var i=0; i<answers.length;i++){
	document.getElementById(`answer${i}`).value='';
    }
}

let clearInput = document.querySelector("#clear")
clearInput.onclick = (ev) => {
  ev.preventDefault()
    clearAll()
}

