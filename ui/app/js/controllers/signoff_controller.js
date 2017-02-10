angular.module('app').controller('SignoffCtrl',
function ($scope, $modalInstance, CSRF, Permissions, object_name, service, current_user, user_roles, sc_id, pk, data, details) {
  $scope.saving = false;
  $scope.errors = {};
  $scope.object_name = object_name;
  $scope.sc_id = sc_id;
  $scope.pk = pk;
  $scope.data = data;
  $scope.details = details;
  $scope.current_user = current_user;
  $scope.signoff_role = null;
  $scope.user_roles = user_roles;

  $scope.saveChanges = function () {
    console.log($scope.signoff_role);
    if ($scope.signoff_role === null) {
      $scope.errors["exception"] = "No Role selected!";
      return;
    }
    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
      var data = {"role": $scope.signoff_role, "csrf_token": csrf_token};
      service.signoffOnScheduledChange($scope.sc_id, data)
      .success(function(response) {
        $scope.saving = false;
        // update list of signoffs that have been made
        $scope.details["signoffs"][$scope.current_user] = $scope.signoff_role;
        $modalInstance.close();
      })
      .error(function(response) {
        $scope.saving = false;
        if (typeof response === "object") {
          $scope.errors = response;
          sweetAlert(
            "Form submission error",
            "See fields highlighted in red.",
            "error"
          );
        }
        else {
          sweetAlert(
            "Unknown error:",
            response
          );
        }
      });
    });
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});