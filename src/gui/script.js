/*
    JavaScript for site containing interface logic



    TEST LOGIC FOR DYNAMIC EDGES


    // Assume thicknesses is your array of thickness values
    var thicknesses = [...]; // fill this with your values

function updateNetwork() {
    // ... existing code ...

    var links = [];
    var thicknessIndex = 0; // add this line to keep track of the current thickness value

    layers.forEach(function(layer, i) {
        layer.forEach(function(neuron, j) {

            var source = i === 0 ? inputNeurons : layers[i - 1];
            source.forEach(function(srcNeuron) {
                links.push({ source: srcNeuron, target: neuron, weight: thicknesses[thicknessIndex++] });
            });

            var target = i === layers.length - 1 ? outputNeurons : layers[i + 1];
            target.forEach(function(tgtNeuron) {
                links.push({ source: neuron, target: tgtNeuron, weight: thicknesses[thicknessIndex++] });
            });
        });
    });

    // ... existing code ...
}

// When the button is clicked, call updateNetwork
document.getElementById("yourButtonId").addEventListener("click", function() {
    updateNetwork();
});

*/

// Define the dimensions of the SVG
var width = 1100;
var height = 600;
var thicknesses = [0.4];
var numInputNeurons = 4;
var numOutputNeurons = 3;

// Create the SVG
var svg = d3.select("#network_visualization").append("svg")
    .attr("width", width)
    .attr("height", height);

// Create a group for the network
var network = svg.append("g");

// Create a drag behavior
var translate = {x: 0, y: 0};
var drag = d3.drag()
    .on("start", function(event) {
        event.sourceEvent.stopPropagation(); // silence other listeners
    })
    .on("drag", function(event) {
        var currTransform = d3.zoomTransform(network.node());
        currTransform.x += event.dx;
        currTransform.y += event.dy;
        network.attr("transform", currTransform);
    });

// Apply the drag behavior to the SVG
svg.call(drag);

// Create a zoom behavior
var zoom = d3.zoom()
    .scaleExtent([0.1, 10]) // This defines the minimum and maximum zoom scale.
    .translateExtent([[0, 0], [width, height]]) // This restricts panning to within the SVG.
    .on("zoom", function(event) {
        var currTransform = d3.zoomTransform(network.node());
        currTransform.k = event.transform.k;
        network.attr("transform", currTransform);
    });

// Apply the zoom behavior to the zoomGroup
svg.call(zoom);

// Function to repeat an array until it has enough values
function repeatArray(arr, count) {
    console.log("Repeating array...")
    var result = [];
    while (count > 0) {
        result = result.concat(arr);
        count--;
    }
    return result;
}

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
    var inputNeurons = d3.range(numInputNeurons).map(function(d, i) {
        return {x: gap, y: height / 3 * (i + 1)};
    });
    
    // Create the hidden layers
    var layers = d3.range(numLayers).map(function(d, i) {
        return d3.range(numNeurons).map(function(d, j) {
            var y = (height - (numNeurons - 1) * gap) / 2 + j * gap;
            return {x: gap * (i + 2), y: y};
        });
    });

    // Attempt to center hidden layers
    // var maxNeurons = Math.max(numInputNeurons, numOutputNeurons, numNeurons);
    // var layers = d3.range(numLayers).map(function(d, i) {
    //     return d3.range(numNeurons).map(function(d, j) {
    //         // Adjust the y-position based on the maximum number of neurons
    //         var y = (height - (maxNeurons - 1) * gap) / 2 + j * gap;
    //         return {x: gap * (i + 2), y: y};
    //     });
    // });

    // Create the output neurons
    var outputNeurons = d3.range(numOutputNeurons).map(function(d, i) {
        var xPos;
        if (numLayers === 1) {
            xPos = 3 * gap;
        } else {
            xPos = layers[numLayers - 1][0].x + gap; // Use the x position of the last neuron in the last layer
        }
        return {x: xPos, y: height / 3 * (i + 1)};
    });   


    // LINKS //


    // Calculate the number of links between the input layer and the first layer
    var numLinks = 2 * numNeurons; 
    // Calculate the number of links between each pair of layers
    numLinks += (numLayers - 1) * numNeurons * numNeurons; 
    // Calculate the number of links between the last layer and the output layer
    numLinks += 2 * numNeurons;

    console.log("Number of links: " + numLinks);
    console.log("Thickness array size before repeat: " + thicknesses.length)

    // Check to ensure array is big enough
    thicknesses = repeatArray(thicknesses, Math.ceil(numLinks / thicknesses.length));

    // Keep track of the current thickness value
    var thicknessIndex = 0;

    // Create the links
    var links = [];
    layers.forEach(function(layer, i) {
        layer.forEach(function(neuron, j) {

            var source = i === 0 ? inputNeurons : layers[i - 1];
            source.forEach(function(srcNeuron) {
                links.push({ source: srcNeuron, target: neuron, weight: thicknesses[thicknessIndex++] });
            });

            var target = i === layers.length - 1 ? outputNeurons : layers[i + 1];
            target.forEach(function(tgtNeuron) {
                links.push({ source: neuron, target: tgtNeuron, weight: thicknesses[thicknessIndex++] });
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
        .style("stroke", "gray")
        .style("stroke-width", function(d) {
            return d.weight;
        });

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

function getIrisModelOutput(weights, val_acc, loss, accuracy, y_pred) {
    thicknesses = weights;
    console.log(weights.length);
    console.log(weights, val_acc, loss, accuracy, y_pred);
}

// When train button is clicked, run python function passed with the values from sliders
document.getElementById("train").onclick = function() {
    eel.triggerBuildIrisModel(parseInt(layersOutput.innerHTML), parseInt(neuronsOutput.innerHTML))(getIrisModelOutput); // Uses the output from the trigger function to call the getIrisModelOutput function
    updateNetwork();
}