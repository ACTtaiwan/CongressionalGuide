'use strict';

const application_root = __dirname,
  express = require('express'),
  bodyParser = require('body-parser'),
  path = require("path");

// Constants
const PORT = 8080;

// App
const app = express();

app.use(express.static(path.join(application_root, "public")));

// app.get('/', function (req, res) {
//   res.send('Hello world!\n');
// });


app.listen(PORT);
console.log('Running on http://localhost:' + PORT);
