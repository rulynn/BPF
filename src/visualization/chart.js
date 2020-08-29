export default class Chart {
    constructor(){
        this._width = 600;
        this._height = 400;
        this._margins = {top:30, left:30, right:30, bottom:30};
        this._data = [];
        this._scaleX = null;
        this._scaleY = null;

        var color = [];

        color[0] = "#4e79a7";
        color[1] = "#f28e2c";
        color[2] = "#edc949";
        color[3] = "#8c9d6a";
        color[4] = "#bab0ab";
        color[5] = "#9c755f";
        color[6] = "#6c4d6e";
        color[7] = "#a88bbe";
        color[8] = "#eed1c1";


        color[9] = "#e08e9d";
        color[10] = "#76b7b2";
        color[11] = "#bab0c4";
        color[12] = "#c2d0ba";
        color[13] = "#deb7be";
        color[14] = "#3c6b82";

        // color[0] = "#4e79a7";
        // color[1] = "#9cbed6";
        //
        // color[3] = "#76b7b2";
        // color[4] = "#59a14f";
        // color[5] = "#edc949";
        // color[6] = "#af7aa1";
        // color[7] = "#ff9da7";
        // color[8] = "#9c755f";
        // color[9] = "#bab0ab";
        // color[10] = "#f28e2c";
        // color[12] = "#deb7be";
        // color[13] = "#c2d0ba";
        // color[14] = "#8c9d6a";
        // color[15] = "#eed1c1";
        // color[16] = "#cf8c6e";
        // color[17] = "#97b4ae";
        // color[18] = "#c5ac9d";
        // color[19] = "#3c6b82";
        this._colors = d3.scaleOrdinal(color);
        this._box = null;
        this._svg = null;
        this._body = null;
        this._padding = {top:10, left:10, right:10, bottom:10};
    }

    width(w){
        if (arguments.length === 0) return this._width;
        this._width = w;
        return this;
    }

    height(h){
        if (arguments.length === 0) return this._height;
        this._height = h;
        return this;
    }

    margins(m){
        if (arguments.length === 0) return this._margins;
        this._margins = m;
        return this;
    }

    data(d){
        if (arguments.length === 0) return this._data;
        this._data = d;
        return this;
    }

    scaleX(x){
        if (arguments.length === 0) return this._scaleX;
        this._scaleX = x;
        return this;
    }

    scaleY(y){
        if (arguments.length === 0) return this._scaleY;
        this._scaleY = y;
        return this;
    }

    svg(s){
        if (arguments.length === 0) return this._svg;
        this._svg = s;
        return this;
    }

    body(b){
        if (arguments.length === 0) return this._body;
        this._body = b;
        return this;
    }

    box(b){
        if (arguments.length === 0) return this._box;
        this._box = b;
        return this;
    }

    getBodyWidth(){
        let width = this._width - this._margins.left - this._margins.right;
        return width > 0 ? width : 0;
    }

    getBodyHeight(){
        let height = this._height - this._margins.top - this._margins.bottom;
        return height > 0 ? height : 0;
    }

    padding(p){
        if (arguments.length === 0) return this._padding;
        this._padding = p;
        return this;
    }

    defineBodyClip(){

        this._svg.append('defs')
                 .append('clipPath')
                 .attr('id', 'clip')
                 .append('rect')
                 .attr('width', this.getBodyWidth() + this._padding.left + this._padding.right)
                 .attr('height', this.getBodyHeight() + this._padding.top  + this._padding.bottom)
                 .attr('x', -this._padding.left)
                 .attr('y', -this._padding.top);
    }

    render(){
        return this;
    }

    bodyX(){
        return this._margins.left;

    }

    bodyY(){
        return this._margins.top;
    }

    renderBody(){
        if (!this._body){
            this._body = this._svg.append('g')
                            .attr('class', 'body')
                            .attr('transform', 'translate(' + this.bodyX() + ',' + this.bodyY() + ')')
                            .attr('clip-path', "url(#clip)");
        }

        this.render();
    }

    renderChart(name){
        if (!this._box){
            this._box = d3.select('body')
                            .append('div')
                            .attr('class',name);
        }

        if (!this._svg){
            this._svg = this._box.append('svg')
                            .attr('width', this._width)
                            .attr('height', this._height);
        }

        this.defineBodyClip();

        this.renderBody();
    }

}

