export default class FlameGraph {


    f(position) {
        console.log(position)
        //画布大小
        var width = 500, height = 500;

        // 在body里添加一个SVG画布
        var svg = d3.select("body")
            .append("svg")
            .attr("width", width)
            .attr("height", height);

        var circle = svg.append("circle")
            .attr("cx", 100)
            .attr("cy", 100)
            .attr("r", 45)
            .style("fill", "green");
    }
}