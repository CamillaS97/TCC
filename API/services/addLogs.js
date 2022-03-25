const db = require('./database');
const config = require('../config');

async function create(logInformation){
    const result = await db.query(
      `INSERT INTO data_logs 
      (temperature, humidity) 
      VALUES ("${logInformation.temperature}", "${logInformation.humidity}");`
    );
  
    let message = 'Error adding logs';
  
    if (result.affectedRows) {
      message = 'Logs uploaded';
    }
  
    return {message};
  }

module.exports = {
   create
}