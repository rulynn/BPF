import Chart from "./chart.js";
import FlameGraph from "./flamegraph.js";

d3.csv('../output/data.csv', function(error, data){

    /* ----------------------------配置参数------------------------  */
    const chart = new Chart();
    const flamegraph = new FlameGraph();

    const config = {
        barPadding: 0.15,
        margins: {top: 80, left: 80, bottom: 50, right: 80},
        textColor: 'black',
        //gridColor: 'gray',
        tickShowGrid: [60, 120, 180],
        //title: '堆叠直方图',
        hoverColor: 'red',
        rectHeight: 25,
        animateDuration: 1000,
        sum:0
    }

    chart.margins(config.margins);


    /* ----------------------------尺度转换------------------------  */
    chart.scaleX = d3.scaleBand()
        .domain(d3.range(data.length))
        .range([0, chart.getBodyWidth()])
        .padding(config.barPadding);

    chart.scaleY = d3.scaleLinear()
        //.domain([0, d3.sum(data.map((d) => d.food))])
        .domain([0, 1])
        .range([chart.getBodyHeight(), 0])

    /* ----------------------------渲染柱形------------------------  */
    chart.renderBars = function(){

        let bars = chart.body().selectAll('.bar')
            .data(data);

        bars.enter()
            .append('rect')
            .attr('class','bar')
            .merge(bars)
            .attr('x', (data) => chart.scaleX(data.name))
            // .attr('y', chart.scaleY(0))
            .attr('width', chart.scaleX.bandwidth())
            // .attr('height', 0)
            .attr('fill', (data,i) => chart._colors(data.id))
            .attr('height', (data) => chart.getBodyHeight() - chart.scaleY(data.sum))
            .attr('y', (data) => chart.scaleY(data.sum));

        bars.exit().remove();
    }

    /* ----------------------------渲染坐标轴------------------------  */
    chart.renderX = function(){
        chart.svg().insert('g','.body')
            .attr('transform', 'translate(' + chart.bodyX() + ',' + (chart.bodyY() + chart.getBodyHeight()) + ')')
            .attr('class', 'xAxis')
            .call(d3.axisBottom(chart.scaleX));
    }

    chart.renderY = function(){
        chart.svg().insert('g','.body')
            .attr('transform', 'translate(' + chart.bodyX() + ',' + chart.bodyY() + ')')
            .attr('class', 'yAxis')
            .call(d3.axisLeft(chart.scaleY));
    }

    chart.renderAxis = function(){
        chart.renderX();
        chart.renderY();
    }

    /* ----------------------------渲染文本标签------------------------  */
    chart.renderText = function(){
        d3.select('.xAxis').append('text')
            .attr('class', 'axisText')
            .attr('x', chart.getBodyWidth())
            .attr('y', 0)
            .attr('fill', config.textColor)
            .attr('dy', 30)
            .text('ID');

        d3.select('.yAxis').append('text')
            .attr('class', 'axisText')
            .attr('x', 0)
            .attr('y', 0)
            .attr('fill', config.textColor)
            .attr('transform', 'rotate(-90)')
            .attr('dy', -40)
            .attr('text-anchor','end')
            .text('比例');
    }

    /* ----------------------------渲染网格线------------------------  */
    chart.renderGrid = function(){
        d3.selectAll('.yAxis .tick')
            .each(function(d, i){
                if (config.tickShowGrid.indexOf(d) > -1){
                    d3.select(this).append('line')
                        .attr('class','grid')
                        .attr('stroke', config.gridColor)
                        .attr('x1', 0)
                        .attr('y1', 0)
                        .attr('x2', chart.getBodyWidth())
                        .attr('y2', 0);
                }
            });
    }

    /* ----------------------------渲染图标题------------------------  */
    chart.renderTitle = function(){
        chart.svg().append('text')
            .classed('title', true)
            .attr('x', chart.width()/2)
            .attr('y', 0)
            .attr('dy', '2em')
            .text(config.title)
            .attr('fill', config.textColor)
            .attr('text-anchor', 'middle')
            .attr('stroke', config.textColor);

    }

    /* ----------------------------绑定鼠标交互事件------------------------  */
    chart.addMouseOn = function(){
        //防抖函数
        function debounce(fn, time){
            let timeId = null;
            return function(){
                const context = this;
                const event = d3.event;
                timeId && clearTimeout(timeId)
                timeId = setTimeout(function(){
                    d3.event = event;
                    fn.apply(context, arguments);
                }, time);
            }
        }

        d3.selectAll('.bar')
            .on('mouseover', function(d){
                const e = d3.event;
                const position = d3.mouse(chart.svg().node());

                d3.select(e.target)
                    .attr('fill', config.hoverColor);

                chart.svg()
                    .append('text')
                    .classed('tip', true)
                    .attr('x', position[0]+5)
                    .attr('y', position[1])
                    .attr('fill', config.textColor)
                    .text(d.name);
            })
            .on('mouseleave', function(d){
                const e = d3.event;

                d3.select(e.target)
                    .attr('fill', chart._colors(d.id));

                d3.select('.tip').remove();
            })
            .on('mousemove', debounce(function(){
                const position = d3.mouse(chart.svg().node());
                d3.select('.tip')
                    .attr('x', position[0]+5)
                    .attr('y', position[1]-5);
            }, 6))
            .on('click', function (d) {
                const e = d3.event;
                const position = d3.mouse(chart.svg().node());

                d3.select(e.target)
                    .attr('fill', 'blue');

                // FlameGraph
                flamegraph.f(d.thread);
            });



    }

    chart.render = function(){

        chart.renderAxis();

        chart.renderText();

        chart.renderGrid();

        chart.renderBars();

        chart.addMouseOn();

        chart.renderTitle();
    }

    chart.renderChart("stack");

});






