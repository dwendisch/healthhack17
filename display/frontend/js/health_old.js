let ratio = window.devicePixelRatio,
	stage = new PIXI.Container(),
	renderer = PIXI.autoDetectRenderer({
		width: window.innerWidth,
		height: window.innerHeight,
		backgroundColor: 0x01084f,
		resolution: ratio,
		autoResize: true,
		antiAliasing: true
	});

document.body.appendChild(renderer.view);

function drawCircle (x = 0,y = 0, r = circleSize, color = 0xffffff) {

	let circle = new PIXI.Graphics();
	circle.beginFill(color);
	circle.drawCircle(x, y, r);
	circle.endFill();
	circle.visible = false;
	stage.addChild(circle);
	return circle;
}

const stageTime = 1000,
	circleSize = 5,
	circleDensity = 3,
	circlesRange = [...Array(500).keys()],
	stageBounds = {
		left: Math.round(window.innerWidth * 0.1),
		right: Math.round(window.innerWidth * 0.9),
		top: Math.round(window.innerHeight * 0.1),
		bottom: Math.round(window.innerHeight * 0.9),
		width: Math.round(window.innerWidth * 0.8),
		height: Math.round(window.innerHeight * 0.8)
	},
	circlesThroat = circlesRange.map(() => drawCircle(0,0,circleSize, 0xa73c5a)),
	circlesFinger = circlesRange.map(() => drawCircle(0,0,circleSize, 0xff7954));

function feeder(y, circles) {
	let circle = circles.find(circle => !circle.visible);
	circle.enteredStage = Date.now();
	circle.x = stageBounds.right;
	circle.y = (stageBounds.top + stageBounds.height / 2 - y);
	circle.visible = true;
}

function progress(start) {
	return (Date.now() - start) / stageTime;
}

function alpha(prog) {
	return Math.min(1, 4 - prog * 4);
}

function xPos(prog) {
	return stageBounds.left + (stageBounds.width - prog * stageBounds.width);
}

function moveCircles(circle, i) {

	if(!circle.visible) return;

	const prog = progress(circle.enteredStage);

	circle.x = xPos(prog);
	circle.alpha = alpha(prog);

	if(circle.x < stageBounds.left) {
		circle.visible = false;
	}
}

(function render() {
	circlesThroat.forEach(moveCircles);
	circlesFinger.forEach(moveCircles);

	renderer.render(stage);
	requestAnimationFrame(render);
})();

setInterval(() => {
	feeder(Math.sin(Date.now()/1000*2*Math.PI) * 100, circlesThroat);
},60);
setInterval(() => {
	feeder(Math.sin(Date.now()/800*2*Math.PI) * 100, circlesFinger);
},50);