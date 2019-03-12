angular.module("app").factory('Auth0', function(angularAuth0) {
  var accessToken;
  var idToken;
  var picture;

  localLogin = function(authResult) {
    // Set isLoggedIn flag in localStorage
    localStorage.setItem('isLoggedIn', true);
    localStorage.setItem('accessToken', authResult.accessToken);
    // Set the time that the access token will expire at
    expiresAt = (authResult.expiresIn * 1000) + new Date().getTime();
    accessToken = authResult.accessToken;
    idToken = authResult.idToken;
    picture = authResult.idTokenPayload.picture;
  };
  var service = {
    login: function() {
      angularAuth0.authorize();
    },
    logout: function() {
      localStorage.removeItem("isLoggedIn");
      accessToken = null;
      idToken = null;
      picture = null;
      expiresAt = null;
    },
    getIdToken: function() {
      return idToken;
    },
    getAccessToken: function() {
      return accessToken;
    },
    getPicture: function() {
      return picture;
    },
    handleAuthentication: function() {
      angularAuth0.parseHash(function(err, authResult) {
        if (authResult && authResult.accessToken && authResult.idToken) {
          localLogin(authResult);
        } else if (err) {
          console.log(err);
        }
      });
    },
    renewTokens: function() {
      // TODO: this is getting a timeout error, only initial logins are working right now
      angularAuth0.checkSession({},
        function(err, result) {
          if (err) {
            console.log(err);
          } else {
            localLogin(result);
          }
        }
      );
    }
  };

  return service;
});