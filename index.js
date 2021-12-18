const mqtt = require('mqtt');
const {Pool} = require('pg');
const {MongoClient} = require("mongodb");

const {initializeApp} = require('firebase/app');
const {getDatabase, ref,push, set} = require('firebase/database');

const firebaseConfig = { //poner a datos del firebase
    apiKey: "",
    authDomain: ".firebaseapp.com",
    databaseURL: "",
    storageBucket: ".appspot.com"
};

const app = initializeApp(firebaseConfig);

const uri = "mongodb://localhost:27017/?maxPoolSize=20"; //se debe cambiar la IP cuando ya no es local
const clientMongoDb = new MongoClient(uri);


/*const pool = new Pool({
    host: "localhost",
    user: "postgres",
    password: "root",
    database: "", //nombre bd
    port: 5432
});*/

pool.on('error', (err, client) => {
    console.error('Unexpected error on idle client', err)
    process.exit(-1)
})


let client = mqtt.connect({
    host: "34.225.43.81",
    port: 1883,
    username: "",
    password: ""
});

client.on("connect", function () {
    console.log("conexión MQTT exitosa");

    client.subscribe("proyectoIot/#");
});

client.on("message", function (topic, messageData) {

    let message = messageData.toString();
    console.log("topic: " + topic + " || messageData: " + message);

    grabarConMongoDb(deviceName, deviceType, value);
    grabarConMongoDbTs(deviceName, deviceType, value);

    writeUserDataFB(deviceName, deviceType, value);
});

function writeUserDataFB(deviceName, deviceType, value) {
    let fecha = (new Date()).getTime();
    const databaseFB = getDatabase(app);
    let dbRef = ref(databaseFB, deviceName);
    let dataSave = {
        deviceType: deviceType,
        valor: value,
        fecha: fecha
    };
    push(dbRef,dataSave);
}

function grabarConMongoDb(deviceName, deviceType, value) {
    let mongoDb = clientMongoDb.db("proyectoIot");
    let document = mongoDb.collection("sensordata");

    let dataGuardar = {
        fecha: new Date(),
        deviceName: deviceName,
        deviceType: deviceType,
        valor: value,
        backend: "nodejs"
    }

    clientMongoDb.connect().then(function (result) {
        document.insertOne(dataGuardar, function (err, res) {
            if (err) {
                console.log(err);
            } else {
                console.log("Documento guardado exitosamente, con id: " + res.insertedId);
            }
        });
    }).catch(function (err) {
        console.log(err);
    });
}

function grabarConMongoDbTs(deviceName, deviceType, value) {
    let mongoDb = clientMongoDb.db("proyectoIot");
    let document = mongoDb.collection("sensordatats");

    let fecha = new Date();
    let dataGuardar = {
        fecha: fecha,
        metadata: {deviceName: deviceName, deviceType: deviceType, zonaHoraria: fecha.getTimezoneOffset()},
        valor: value
    }

    clientMongoDb.connect().then(function (result) {
        document.insertOne(dataGuardar, function (err, res) {
            if (err) {
                console.log(err);
            } else {
                console.log("Documento guardado exitosamente, con id: " + res.insertedId);
            }
        });
    }).catch(function (err) {
        console.log(err);
    });
}