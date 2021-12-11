
let elt = document.getElementById('calculator')
let calculator = Desmos.GraphingCalculator(elt, zoomFit = true)

let defaultState = calculator.getState();

document.getElementById('set-state').addEventListener('click', () => {
    defaultState = calculator.getState();
})

document.getElementById('reset').addEventListener('click', () => {
    calculator.setState(defaultState)
})

function plotGraph(){
    let fr = new FileReader()
    fr.onload = () => {
        var graphs = fr.result.split("\n")
        
        console.log(graphs)
        expression_states = []
        for (let i = 0; i < graphs.length; i++){
            expression_states.push(JSON.parse(graphs[i]))
        }

        expression_states.forEach(function(expression_state) {
            calculator.setExpression(expression_state)
        })
        
    }
    fr.readAsText(this.files[0])
}

document.getElementById('inputfile').addEventListener('change', plotGraph)

//{'id': 'graph1', 'latex': 'x', 'color': '#000000', 'lineWidth': 1.0}, {'id': 'graph2', 'latex': 'x^2' , 'color': '#000000', 'lineWidth': 1.0}, {'id': 'graph3', 'latex': 'x^3' , 'color': '#000000', 'lineWidth': 1.0}