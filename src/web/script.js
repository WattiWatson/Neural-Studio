/*
    JavaScript for site containing interface logic
*/

// EXAMPLE
// Define the dimensions of the SVG
var width = 1100, height = 600;
let factor = 2.5

// Create the SVG
var svg = d3.select("#network_visualization").append("svg")
    .attr("width", width)
    .attr("height", height);

// Create a group for the network
var network = svg.append("g");

// Create a drag behavior
var translate = {x: 0, y: 0};
var drag = d3.drag()
    .on("drag", function(event) {
        translate.x += event.dx;
        translate.y += event.dy;
        network.attr("transform", "translate(" + translate.x + "," + translate.y + ")");
    });

// Apply the drag behavior to the SVG
svg.call(drag);

// Function to update the network
function updateNetwork() {
    // Clear the network
    network.selectAll("*").remove();

    // Get the number of neurons and layers from the sliders
    var numNeurons = document.getElementById("neurons").value;
    var numLayers = document.getElementById("layers").value;

    // Adjust the gap based on the number of layers
    var gap = width / (2.5 * numLayers + 1);

    // Create the input neurons
    var inputNeurons = d3.range(2).map(function(d, i) {
        return {x: gap, y: height / 3 * (i + 1)};
    });

    // Create the hidden layers
    var layers = d3.range(numLayers).map(function(d, i) {
        return d3.range(numNeurons).map(function(d, j) {
            var y = (height - (numNeurons - 1) * gap) / 2 + j * gap;
            return {x: gap * (i + 2), y: y};
        });
    });

    // Create the output neurons
    var outputNeurons = d3.range(2).map(function(d, i) {
        var xPos;
        if (numLayers === 1) {
            xPos = 3 * gap;
        } else {
            xPos = width - gap;
        }
        return {x: xPos, y: height / 3 * (i + 1)};
    });    

    // Create the links
    var links = [];
    layers.forEach(function(layer, i) {
        layer.forEach(function(neuron, j) {
            // Connect to the previous layer or input neurons
            var source = i === 0 ? inputNeurons : layers[i - 1];
            source.forEach(function(srcNeuron) {
                links.push({source: srcNeuron, target: neuron});
            });

            // Connect to the next layer or output neurons
            var target = i === layers.length - 1 ? outputNeurons : layers[i + 1];
            target.forEach(function(tgtNeuron) {
                links.push({source: neuron, target: tgtNeuron});
            });
        });
    });

    // Create the links between the neurons
    network.selectAll(".link")
        .data(links)
        .enter().append("line")
        .attr("class", "link")
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; })
        .style("stroke", "black");

    // Create the circles for the neurons
    network.selectAll(".neuron")
        .data(inputNeurons.concat(...layers, outputNeurons))
        .enter().append("circle")
        .attr("class", "neuron")
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; })
        .attr("r", 10);
}

// Update the network when the sliders or button are changed
d3.selectAll("#neurons, #layers, #train").on("input", updateNetwork);

// Initial update
updateNetwork();






// Get neuron slider
let neuronsSlider = document.getElementById("neurons");
let neuronsOutput = document.getElementById("neurons_val");
neuronsOutput.innerHTML = neuronsSlider.value;
// Update neuron count when slider is moved
neuronsSlider.oninput = function() {
    neuronsOutput.innerHTML = this.value;
}

// Get hidden layer slider
let layersSlider = document.getElementById("layers");
let layersOutput = document.getElementById("layers_val");
layersOutput.innerHTML = layersSlider.value;
// Update hidden layer count when slider is moved
layersSlider.oninput = function() {
    layersOutput.innerHTML = this.value;
}

// JS functions to be used in Python
eel.expose(get_neurons);
function get_neurons() {
    return parseInt(neuronsOutput.innerHTML)
}
eel.expose(get_layers);
function get_layers() {
    return parseInt(layersOutput.innerHTML)
}

// When train button is clicked, run python function passed with the values from sliders
document.getElementById("train").onclick = function() {
    eel.print_input_vals(parseInt(neuronsOutput.innerHTML), parseInt(layersOutput.innerHTML));
}
