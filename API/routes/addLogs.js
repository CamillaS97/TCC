const express = require('express');
const router = express.Router();
const addLogs = require('../services/addLogs');

router.post('/', async function(req, res, next) {
    try {
      res.json(await addLogs.create(req.body));
    } catch (err) {
      console.error(`Error adding logs`, err.message);
      next(err);
    }
  });

module.exports = router;