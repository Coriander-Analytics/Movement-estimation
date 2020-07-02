const posenet = require('@tensorflow-models/posenet');


const net = posenet.load({
	architecture: 'ResNet50',
	outputStride: 32,
	inputResolution: { width: 257, height: 200 },
	quantBytes: 2
});

console.log("Calling anonymous async function");
(async() => {
	// Load the model spcified above
	console.log("Loading model...");

	// await net;

	console.log("Loaded!");
	console.log(net);

	// Load the image that we want to estimate the pose of
	image = new Image();
	image.src = "https://www.blog.theteamw.com/wp-content/uploads/legacy/2012/05/fx10.jpg"

	// Estimate the pose
	pose = await net.estimateSinglePose(image, {
		flipHorizontal: false
	});

	// Print the pose, which is has a confidence score and array
	// of keypoints
	console.log(pose)
})();



