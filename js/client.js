// Hello World client
// Connects REQ socket to tcp://localhost:5555
// Sends "Hello" to server.

let zmq = require("zeromq");

// socket to talk to server
console.log("Connecting to hello world server…");
let requester = zmq.socket("req");

let x = 0;
requester.on("message", function(reply) {
	console.log("Received reply", x, ": [", reply.toString(), "]");
	x += 1;
	if (x === 10) {
		requester.close();
		process.exit(0);
	}
});

requester.connect("tcp://localhost:5555");

for (let i = 0; i < 10; i++) {
	console.log("Sending request", i, "…");
	requester.send("Hello");
}

process.on("SIGINT", function() {
	requester.close();
});
