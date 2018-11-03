
var c = document.getElementById("myCanvas");
var ctx = c.getContext("2d");
ctx.fillStyle = 'rgb(0, 0, 0)';

function displayFrame(inputx, inputy, inputname) {
	var centerx = inputx;
	var centery = inputy;
	var dim = 75;
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
}

var room = { p1:{ x:5, y:5 },
		     p2:{ x:300, y:5 },
			 p3:{x:300, y:250},
			 p4:{x:600, y:250},
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
			console.log(prop);
			if (first) {
				p1 = prop;
				pprev = prop; 
				first = false;
			} else {
				console.log("hello");
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

var myObj = { x:150, y:100, name:"desk" }; 
makeFrame(myObj);
