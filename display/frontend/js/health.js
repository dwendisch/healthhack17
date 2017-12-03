let ratio = window.devicePixelRatio,
	stage = new PIXI.Container(),
	renderer = PIXI.autoDetectRenderer({
		width: window.innerWidth,
		height: window.innerHeight,
		backgroundColor: 0xffffff,
		resolution: ratio,
		autoResize: true,
		antiAliasing: true
	});

document.body.appendChild(renderer.view);

function drawCircle (x = 0,y = 0, r = circleSize, color = 0xffffff) {

	let circle = new PIXI.Graphics();
	circle.beginFill(color);
	circle.drawCircle(x, y, r);
	//console.log("circle.drawCircle(x, y, r);", x, y, r)
	circle.endFill();
	circle.enteredStage = 0;
	circle.alpha = 0;
	//circle.visible = false;
	stage.addChild(circle);
	return circle;
}

const stageTime = 5000,
	circleSize = 5,
	circleDensity = 3,
	circlesAmount = 1000,
	circlesRange = [...Array(circlesAmount).keys()],
	stageBounds = {
		left: Math.round(window.innerWidth * 0.1),
		right: Math.round(window.innerWidth * 0.9),
		top: Math.round(window.innerHeight * 0.2),
		bottom: Math.round(window.innerHeight * 0.8),
		width: Math.round(window.innerWidth * 0.8),
		height: Math.round(window.innerHeight * 0.6)
	};
let circlesThroat = circlesRange.map((i) => drawCircle(xPos(i),yMid(),circleSize, 0xff0000)),
	circlesFinger = circlesRange.map((i) => drawCircle(xPos(i),yMid(),circleSize, 0x0000ff));

let startTime = Date.now();
function currentXPos() {
	return stageBounds.left + progress() * stageBounds.width;
}

function xPos(i) {
	return stageBounds.left + (i/circlesAmount) * stageBounds.width;
}

function yMid() {
	return stageBounds.top + stageBounds.height/2;
}

function currentIndex() {
	const now = Date.now();
	if(startTime < now - stageTime) {
		startTime = now;
	}
	return Math.round(progress()*(circlesAmount-1));
}

function feeder(percentage, circles) {

	var index = currentIndex();
	percentage = Math.min(100, Math.max(0, percentage)) / 100;

	var y = stageBounds.top - stageBounds.height*(percentage) ;
	console.log("percentage2", percentage, y/2)
	//console.log("index", index)
	//console.log("index", index)
	circles[index].enteredStage = Date.now();
	//circles[index].x = currentXPos();
	circles[index].y = y/2;
	//circle.visible = true;
}

function progress(start = startTime) {
	return Math.max(0, (Date.now() - start)) / stageTime;
}

function alpha(prog) {
	return Math.min(1, 4 - (prog*4+0.5));
}

function fadeCircle(circle, i) {

	// if(!circle.visible) return;
	// circle.x = xPos(prog);
	// circle.y = yPos();
	circle.alpha = alpha(progress(circle.enteredStage));
}

(function render() {
	circlesThroat.forEach(fadeCircle);
	circlesFinger.forEach(fadeCircle);

	renderer.render(stage);
	requestAnimationFrame(render);
})();

setInterval(() => {
	//feeder(Math.random()>.5 ? 0 : 100, circlesThroat);
	feeder(Math.sin(Date.now()/1000*2*Math.PI) * 50 + 50, circlesThroat);
},22);
setInterval(() => {
	//feeder(Math.random()>.5 ? 0 : 100, circlesFinger);
	feeder(Math.sin(Date.now()/800*2*Math.PI) * 50 + 50, circlesFinger);
},10);