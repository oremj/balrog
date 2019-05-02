angular.module('app').controller('ReleaseDataCtrl',
function($scope, $http, $modalInstance, Releases, Rules, release, diff, previous_version = null) {
  $scope.release = release;
  $scope.diff = diff;
  $scope.previous_version = previous_version;

  if (release.timestamp) {
    if (diff) {
      if (previous_version) {
      }
      else {
      }
      $scope.release.diff = "this is a diff";
    } else {
      Releases.getData(release.data_url)
      .then(function(response) {
        $scope.release.data = response.data;
      });
    }

  } else {
    Releases.getRelease(release.name)
    .then(function(response) {
      $scope.release.data = response.data;
    });
  }

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
