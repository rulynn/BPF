const _width = 800;
const _height = 1000;
var _box = null;
var _svg = null;
function f(tid) {


    if (!_box){
        _box = d3.select('body')
            .append('div')
            .attr('class',"flamegrpah");
    }

    if (!_svg){
        _svg = _box.append('svg')
            .attr('width', _width)
            .attr('height', _height);
    }

    console.log(tid)
    var flameGraph = d3.flamegraph()
        .width(_width)
        .height(_height)
        .cellHeight(18)
        .transitionDuration(750)
        .minFrameSize(5)
        .transitionEase(d3.easeCubic)
        .sort(true)
        .title("")
        .onClick(onClick)
        .differential(false)
        .selfValue(false);

    var file = "../output/stack/" + tid + ".log.json";

    d3.json(file, function (error, data) {
        if (error) return console.warn(error);
        _svg.datum(data)
            .call(flameGraph);
    });

    document.getElementById("form").addEventListener("submit", function (event) {
        event.preventDefault();
        search();
    });

    function search() {
        var term = document.getElementById("term").value;
        flameGraph.search(term);
    }

    function clear() {
        document.getElementById('term').value = '';
        flameGraph.clear();
    }

    function resetZoom() {
        flameGraph.resetZoom();
    }

    function onClick(d) {
        console.info("Clicked on " + d.data.name);
    }
}
