
var c = document.getElementById("myCanvas");
var ctx = c.getContext("2d");
ctx.fillStyle = 'rgb(0, 0, 0)';
var rects = [];
var dim = 75;

function displayFrame(inputx, inputy, inputname) {
	var centerx = inputx;
	var centery = inputy;
	var x = centerx - dim/2;
	var y = centery - dim/2;
	var attr_dimx = dim/2;
	var attr_dimy = attr_dimx/3;
	var attrx = x + dim - attr_dimx;
	var attry = y + dim - attr_dimy;
	var name = inputname;
	ctx.rect(x, y, dim, dim);
	ctx.stroke;
	ctx.rect(attrx, attry, attr_dimx, attr_dimy);
	ctx.stroke();
	ctx.textAlign = "center";
	ctx.font = attr_dimy.toString() + "px Arial";
	ctx.fillText(name, attrx + attr_dimx/2, attry + 4*attr_dimy/5);
}

function makeFrame(inputObj) {
	displayFrame(inputObj.x, inputObj.y, inputObj.name);
	rects.push({ x: inputObj.x, y: inputObj.y, d: dim, id:inputObj.id});
}

var room = { p1:{ x:5, y:5 },
		     p2:{ x:300, y:5 },
			 p3:{ x:300, y:250},
			 p4:{ x:600, y:250},
	  		 p5:{ x:600, y:500},
			 p6:{ x:5, y:500}
		   };

function makeRoom(inRoom) {
	var first = true;
	var p1;
	var pprev;
	for (var key in inRoom) {
		ctx.beginPath();
		if (inRoom.hasOwnProperty(key)) {
			var prop = inRoom[key];
			if (first) {
				p1 = prop;
				pprev = prop; 
				first = false;
			} else {
				ctx.moveTo(pprev.x, pprev.y);
				ctx.lineTo(prop.x, prop.y);
				ctx.stroke();
				ctx.moveTo(prop.x, prop.y);
				pprev = prop;
			}
		}
	}
	ctx.lineTo(p1.x, p1.y);
	ctx.stroke();
}
makeRoom(room);

var myObj = { x:100, y:50, name:"desk", id:1 }; 
makeFrame(myObj);

c.onmousemove = function(e) {
	var rect = this.getBoundingClientRect(),
		x = e.clientX - rect.left,
		y = e.clientY - rect.top,
		i = 0, r;

	while (r = rects[i++]) {
		ctx.beginPath();
		ctx.rect(r.x - r.d/2, r.y - r.d/2, r.d, r.d);

		if (ctx.isPointInPath(x, y)) {
			console.log("on rect " + i.toString());
		}
	}
}
