// var dataset = ["I like dog","I like cat","I like snake"];
//
// var body = d3.select("body");
// var p = body.selectAll("p");
//
// p.data(dataset)
//     .text(function(d, i){
//         return d;
//     });
//
// body.append("p")
//     .text("append p element");


var width = 300;  //画布的宽度
var height = 300;   //画布的高度

// SVG 画布
var svg = d3.select("body")     //选择文档中的body元素
    .append("svg")          //添加一个svg元素
    .attr("width", width)       //设定宽度
    .attr("height", height);    //设定高度

// 数据
var dataset = [ 2.5 , 2.1 , 1.7 , 1.3 , 0.9 ];  // 数据
var rectHeight = 25;   //每个矩形所占的像素高度(包括空白)

// 比例尺
var min = d3.min(dataset);
var max = d3.max(dataset);

var linear = d3.scale.linear()
    .domain([min, max])
    .range([0, 300]);

// 坐标轴
var axis = d3.svg.axis()    // D3 中坐标轴的组件，能够在 SVG 中生成组成坐标轴的元素。
    .scale(linear)      //指定比例尺
    .orient("bottom")   //指定刻度的方向
    .ticks(7);          //指定刻度的数量

svg.append("g")
    .attr("class","axis")
    .attr("transform","translate(20,130)")
    .call(axis);

// 绘图
svg.selectAll("rect")        //选择svg内所有的矩形
    .data(dataset)           //绑定数组
    .enter()                 //指定选择集的enter部分
    .append("rect")   //添加足够数量的矩形元素
    .attr("x",20)
    .attr("y",function(d,i){
        return i * rectHeight;
    })
    .attr("width",function(d){
        return linear(d);       // 利用比例尺
    })
    .attr("height",rectHeight-2)
    .attr("fill","red")
    .on("click",function(d,i){
        d3.select(this)
            .attr("fill","green");
    })
    .on("mouseover",function(d,i){
        d3.select(this)
            .attr("fill","yellow");
    })
    .on("mouseout",function(d,i){
        d3.select(this)
            .transition()
            .duration(500)
            .attr("fill","red");
    });