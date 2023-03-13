import * as Automerge from '@automerge/automerge'
var poissonProcess = require('poisson-process');

let pdoc = Automerge.init()
let sdoc = Automerge.init()


pdoc = Automerge.change(pdoc, 'Add card', pdoc => {
    pdoc.q1=''
    pdoc.q2=''
    pdoc.q3=''
})


pdoc = Automerge.change(pdoc, 'Mark card as done', pdoc => {
  pdoc.test = 'hi'
})

document.querySelector('#testbox').value=pdoc.test

function addItem(text) {
  let newDoc = Automerge.change(doc, doc => {
    if (!doc.items) doc.items = []
    doc.items.push({ text, done: false })
  })
    updateDoc(newDoc)
    console.log(text)
}

let form = document.querySelector("form")
let input = document.querySelector("#new-todo")
form.onsubmit = (ev) => {
  ev.preventDefault()
  addItem(input.value)
  input.value = null
}
const numQuestions = 5;

for (var i=0; i<numQuestions;i++){
    let typeInput = document.querySelector(`answer${i}`)
    typeInput.onkeydown = userTypes()
}

function userTypes(event){
    console.log(event.target)
    // Add leter to crdt
    pdoc = Automerge.change(pdoc, 'Add letter', doc => {
	doc.q[qnum]+=letter
    })

    // Delay
    let delay = poissonProcess.sample(1000)
    // Merge CRDTs
    setTimeout(() => {
	sdoc = Automerge.merge(sdoc, pdoc)
    }, delay)
 
}

/*function render(doc) {
  let list = document.querySelector("#todo-list")
  list.innerHTML = ''
  doc.items && doc.items.forEach((item, index) => {
    let itemEl = document.createElement('li')
    itemEl.innerText = item.text
    itemEl.style = item.done ? 'text-decoration: line-through' : ''
    list.appendChild(itemEl)
  })
}
*/

function updateDoc(newDoc) {
  doc = newDoc
  render(newDoc)
}
//let questionBox = document.querySelector("#answer")

function getRandomInt(max = 4) {
  return Math.floor(Math.random() * max);
}

const strings = ["Vienna","London","Paris", "Madrid", "Berlin", "Rome", "Dublin", "Moscow"]

const letters = strings.map(s => Array.from(s))
const copy = letters.map(x => x)


const updateValue = (pick = getRandomInt(letters.length), input = document.getElementById(`answer${pick}`)) => {
    let delay = poissonProcess.sample(500)

  if (letters[pick].length == 0) {
      letters.splice(pick, 1)
      delay+=1000
    if (letters.length === 0) {
      return
    }
      do {
    pick = getRandomInt(letters.length)
    const id = copy.indexOf(letters[pick])
	  input = document.getElementById(`answer${id}`)
	  if (input.value!=''){
	      letters.splice(pick,1)
	  }
      } while (input.value!='')
  }

  const letter = letters[pick].splice(0, 1)

  setTimeout(() => {
    input.value += letter
    updateValue(pick, input)
  }, delay)

}



let startInput = document.querySelector("#start")
startInput.onclick = (ev) => {
  ev.preventDefault()
    updateValue()
}



function clearAll(){
    for (var i=0; i<strings.length;i++){
	document.getElementById(`answer${i}`).value='';
    }
}

let clearInput = document.querySelector("#clear")
clearInput.onclick = (ev) => {
  ev.preventDefault()
    clearAll()
}



/*
function startUser(){
    const answers = ["Vienna", "London", "Paris", "Madrid", "Berlin", "Rome", "Dublin", "Moscow"]

    let letters = answers.map(s => Array.from(s))
    const copy = letters.map(x => x)

    function getRandomInt(max) {
	return Math.floor(Math.random() * max);
    }
    // Dan Ristea wrote this function
    const typeAnswer = (boxIndex = getRandomInt(letters.length), inputBox = document.getElementById(`answer${boxIndex}`)) => {

	var delay = poissonProcess.sample(500);

	if (letters[boxIndex].length == 0) {
	    letters.splice(boxIndex, 1)
	    if (letters.length === 0) {
		return
	    }
	    boxIndex = getRandomInt(letters.length)
	    const id = copy.indexOf(letters[boxIndex])
	    inputBox = document.getElementById(`answer${id}`)
	
	}

	const letter = letters[boxIndex].splice(0, 1)

    
    setTimeout(() => {
	inputBox.val+=letter;
	typeAnswer(boxIndex,inputBox)
    }, 500);
}

    
   	typeAnswer()
   
}
*/
