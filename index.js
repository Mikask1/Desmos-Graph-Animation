let elt = document.getElementById('calculator')
let calculator = Desmos.GraphingCalculator(elt, zoomFit = true)
let frameEl = document.getElementById("frame")
let defaultState = calculator.getState();


document.getElementById('set-state').addEventListener('click', () => {
    defaultState = calculator.getState();
})

document.getElementById('save-state').addEventListener('click', () => {
    localStorage.setItem("saved", JSON.stringify(calculator.getState()))
})

document.getElementById('get-state').addEventListener('click', () => {
    calculator.setState(JSON.parse(localStorage.getItem("saved")))
})

function saveAs(uri, filename) {
    var link = document.createElement('a');
    if (typeof link.download === 'string') {
        link.href = uri;
        link.download = filename;

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }else{
        window.open(uri);
    }
}

function render(){
    for (let i = 0; i < this.files.length; i++){
        let fr = new FileReader()
        fr.onload = () => {
            let fileIndex = this.files[i].name.match(/(\d+)/)[0]
            console.log(fileIndex)
            frameEl.innerText = "Frame : "+fileIndex
            
            var graphs = fr.result.split("\n")
            expression_states = []
            for (let i = 0; i < graphs.length; i++){
                expression_states.push(JSON.parse(graphs[i]))
            }

            calculator.setState(defaultState)
            
            expression_states.forEach(function(expression_state) {
                calculator.setExpression(expression_state)
            })

            calculator.asyncScreenshot(data => saveAs(data, "frame"+fileIndex+".png"))
        }
        fr.readAsText(this.files[i])
    }
}

document.getElementById('inputfile').addEventListener('change', render)

