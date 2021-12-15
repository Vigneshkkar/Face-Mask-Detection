const express = require('express');
const app = express();
const port = 3000;

const { initializeApp, cert } = require('firebase-admin/app');
const { getMessaging } = require('firebase-admin/messaging');

var serviceAccount = require('./face-mask-detection-ea05d-firebase-adminsdk-lnv2l-184eb2072f.json');

const fire = initializeApp({
  credential: cert(serviceAccount),
});

// These registration tokens come from the client FCM SDKs.
const registrationTokens = [
  'dMYdDuEwMFtJ58w_L42fv-:APA91bESoIFbnmG-6bkLN6a0VFqHCMhQ8YPndtAz1snjTpoGnTKjFkrPBr9K6pxck3uJDkZzkHjVXgOTZFITZ9alixSPelkIoiCfTeQkvoa4uXDnl88ssWvbko92Q-MvIzGZVSffaA9z',
];

// Subscribe the devices corresponding to the registration tokens to the
// topic.

app.get('/', (req, res) => {
  console.log(req.query.id);
  res.send('Hello World!');
  getMessaging()
    .subscribeToTopic([req.query.id], 'Alert')
    .then((response) => {
      // See the MessagingTopicManagementResponse reference documentation
      // for the contents of response.
      console.log('Successfully subscribed to topic:', response);
    })
    .catch((error) => {
      console.log('Error subscribing to topic:', error);
    });
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
