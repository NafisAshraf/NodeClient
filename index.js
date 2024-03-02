const io = require("socket.io-client");

const options = {
  auth: {
    token: "JetsonNanoNodeClientToken",
  },
};
const socket = io("http://localhost:3000", options);

socket.on("connect", () => {
  console.log("Connected to the server");

  const sensorDataInterval = setInterval(async () => {
    const sensorData = await sensorReadData();
    console.log(sensorData);
    socket.emit("sensorData", sensorData);
  }, 1000);

  socket.on("disconnect", () => {
    console.log("Disconnected from the server");
    clearInterval(sensorDataInterval);
  });
});

// Read Data from gpio pins
const sensorReadData = () =>
  new Promise(async (resolve, reject) => {
    // Generate a random number in the range 30 to 50
    const temperature = Math.floor(Math.random() * (50 - 30 + 1) + 30);
    const pressure = Math.floor(Math.random() * (100 - 50 + 1) + 50);

    resolve({ temperature, pressure });
  });
