angular.module('app').controller('RevokeSignoffCtrl',
function ($scope, $modalInstance, CSRF) {

  $scope.saving = false;

  $scope.saveChanges = function () {
    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
    });
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});