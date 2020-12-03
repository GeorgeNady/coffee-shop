/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://localhost:5000', // the running FLASK api server url
  auth0: {
    url: 'https://fsnd200.us.auth0.com', // the auth0 domain prefix
    audience: 'coffee_shop', // the audience set for the auth0 app
    clientId: 'VoNLIrLajritb9qRoAdudVCPhflGMF1d', // the client id generated for the auth0 app
    callbackURL: 'https://127.0.0.1:5000/login-result', // the base url of the running ionic application. 
  }
};
