/*
    JavaScript for site containing interface logic for CNN
*/

// Define the dimensions of the SVG
var width = 1300;
var height = 800;
var initialThickness = 0.4;
var thicknesses = [];
var numInputNeurons = 4; // Number of input neurons
var numOutputNeurons = 3; // Number of output neurons
const epochs = 100;

// Set the initial zoom level of visual
var initialZoom = 0.5;

// Initial edge color
edgeColor = "gray";

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
zoom.scaleTo(svg, initialZoom);

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
        return {x: gap, y: (height - (numInputNeurons - 1) * gap) / 2 + i * gap, color: "green"};
    });

    // Create the hidden layers
    var layers = d3.range(numLayers).map(function(d, i) {
        return d3.range(numNeurons).map(function(d, j) {
            var y = (height - (numNeurons - 1) * gap) / 2 + j * gap;
            return {x: gap * (i + 2), y: y};
        });
    });

    // Create the output neurons
    var outputNeurons = d3.range(numOutputNeurons).map(function(d, i) {
        var xPos;
        if (numLayers === 1) {
            xPos = 3 * gap;
        } else {
            xPos = layers[numLayers - 1][0].x + gap; // Use the x position of the last neuron in the last layer
        }
        return {x: xPos, y: (height - (numOutputNeurons - 1) * gap) / 2 + i * gap, color: "orange"};
    });

    // LINKS //

    // Calculate the number of links
    numLinks = (4 * numNeurons) + ((numLayers - 1) * (numNeurons * numNeurons)) + (3 * numNeurons);

    console.log("Number of links: " + numLinks);

    // Keep track of the current thickness value
    var thicknessIndex = 0;

    // Create the links
    console.log("Thicknesses length: " + thicknesses.length);
    var links = [];
    outputNeurons.forEach(function(neuron) {
        var source = neuron;
        var targetLayer = layers[layers.length - 1];
        targetLayer.forEach(function(targetNeuron) {
            var currWeight = thicknessIndex < thicknesses.length ? thicknesses[thicknessIndex++] : initialThickness;
            var edgeColor = thicknesses.length > 0 ? (currWeight < 0 ? "red" : "blue") : "gray";
            links.push({ source: source, target: targetNeuron, weight: Math.abs(currWeight), color: edgeColor });
        });
    });

    for (var i = layers.length - 1; i > 0; i--) {
        var layer = layers[i];
        var prevLayer = layers[i - 1];
        layer.forEach(function(neuron) {
            var source = neuron;
            prevLayer.forEach(function(targetNeuron) {
                var currWeight = thicknessIndex < thicknesses.length ? thicknesses[thicknessIndex++] : initialThickness;
                var edgeColor = thicknesses.length > 0 ? (currWeight < 0 ? "red" : "blue") : "gray";
                links.push({ source: source, target: targetNeuron, weight: Math.abs(currWeight), color: edgeColor });
            });
        });
    }

    inputNeurons.forEach(function(neuron) {
        var source = neuron;
        var targetLayer = layers[0];
        targetLayer.forEach(function(targetNeuron) {
            var currWeight = thicknessIndex < thicknesses.length ? thicknesses[thicknessIndex++] : initialThickness;
            var edgeColor = thicknesses.length > 0 ? (currWeight < 0 ? "red" : "blue") : "gray";
            links.push({ source: source, target: targetNeuron, weight: Math.abs(currWeight), color: edgeColor });
        });
    });

    // Create the links between the neurons
    var link = network.selectAll(".link")
    .data(links)
    .enter().append("line")
    .attr("class", "link")
    .attr("x1", function(d) { return d.source.x; })
    .attr("y1", function(d) { return d.source.y; })
    .attr("x2", function(d) { return d.target.x; })
    .attr("y2", function(d) { return d.target.y; })
    .style("stroke", function(d) {
        return d.color;    
    })
    .style("stroke-width", function(d) {
        return d.weight;
    });

    console.log("Links drawn: " + links.length);

    // Create a tooltip
    var tooltip = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

    // Add mouseover and mouseout events to the links
    link.on("mouseover", function(event, d) {
        tooltip.transition()
            .duration(200)
            .style("opacity", .9);
        tooltip.html("Thickness: " + d.weight)
            .style("left", (event.pageX) + "px")
            .style("top", (event.pageY - 28) + "px");
    })
    .on("mouseout", function(d) {
        tooltip.transition()
            .duration(500)
            .style("opacity", 0);
    });

    // Create the circles for the neurons
    network.selectAll(".neuron")
        .data(inputNeurons.concat(...layers, outputNeurons))
        .enter().append("circle")
        .attr("class", "neuron")
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; })
        .attr("r", 10)
        .style("fill", function(d) { return d.color });
}

// Update the network when the sliders or button are changed
d3.selectAll("#neurons, #layers, #train").on("input", updateNetwork);

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

function getIrisModelOutput(weights) {
    thicknesses = [];
    for(let w of weights) {
        thicknesses.push(parseFloat(w));
    }
    updateNetwork();
    // createLossGraph(val_acc, epochs);
}

// When train button is clicked, run python function passed with the values from sliders
document.getElementById("train").onclick = async function() {
    await eel.triggerBuildMNISTModel(parseInt(layersOutput.innerHTML), parseInt(neuronsOutput.innerHTML), epochs)(getIrisModelOutput); // Uses the output from the trigger function to call the getIrisModelOutput function
}

window.addEventListener('resize', function() {
    svg.attr("width", window.innerWidth);
    svg.attr("height", window.innerWidth / aspect);
});

// Initial update
updateNetwork();
