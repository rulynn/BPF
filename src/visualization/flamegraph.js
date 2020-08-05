export default class FlameGraph {

    constructor(){
        this._width = 600;
        this._height = 400;
        this._margins = {top:30, left:30, right:30, bottom:30};
        this._data = [];
        this._scaleX = null;
        this._scaleY = null;
        this._colors = d3.scaleOrdinal(d3.schemeCategory10);
        this._box = null;
        this._svg = null;
        this._body = null;
        this._padding = {top:10, left:10, right:10, bottom:10};
    }

    f(tid) {
        if (!this._box){
            this._box = d3.select('.box');
        }

        if (!this._svg) {
            this._svg = this._box.append('div')
                .attr('id','flamegraph')
                // .append('flamegraph')
                .attr('width', this._width)
                .attr('height', this._height);
        }

        console.log(tid)
        var flameGraph = d3.flamegraph()
            .width(this._width)
            .width(this._height)
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

        if (tid == null) file = "../output/stacks.json";

        d3.json(file, function (error, data) {
            if (error) return console.warn(error);
            d3.select("#flamegraph")
                .datum(data)
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
}