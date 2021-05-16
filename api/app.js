const express = require('express')
const fileUpload = require('express-fileupload')
const shortid = require('shortid')
const jackrabbit = require('jackrabbit')
require('dotenv').config()

const app = express()
app.use(fileUpload())

const rabbit = jackrabbit(process.env.AMQP_URL);
const exchange = rabbit.default();

app.post('/upload', (req, res) => {
  let file = req.files.image;
  if(!file) {
    res.status(400).json({
      success: false,
      message: 'File not found'
    })
  }
  file = file['data'].toString('base64')

  const id = shortid.generate()
  exchange.publish({ msg: {
    file: file,
    id
  } }, { key: 'worker' });

  res.status(200).json({
    success: true,
    id
  })
})

app.listen(5000, () => {
  console.log('Running on port 5000')
})
