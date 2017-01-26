angular.module("app").controller('RequiredSignoffsController',
function($scope, $modal, ProductRequiredSignoffs, PermissionsRequiredSignoffs) {
  $scope.loading = true;

  $scope.required_signoffs = {};
  $scope.selected_product = null;

  $scope.$watch("required_signoffs", function() {
    if ($scope.selected_product === null) {
      var products = Object.keys($scope.required_signoffs);
      if (products.length > 0) {
        $scope.selected_product = products[0];
      }
    }
  }, true);
  // Grabbing initial data from the server
  ProductRequiredSignoffs.getRequiredSignoffs()
  .success(function(response) {
    if (response["count"] > 0) {
      response["required_signoffs"].forEach(function(rs) {
        if (! (rs.product in $scope.required_signoffs)) {
          $scope.required_signoffs[rs.product] = {"channels": {}};
        }
    
        if (! (rs.channel in $scope.required_signoffs[rs.product]["channels"])) {
          $scope.required_signoffs[rs.product]["channels"][rs.channel] = {};
        }
    
        $scope.required_signoffs[rs.product]["channels"][rs.channel][rs.role] = {
            "signoffs_required": rs.signoffs_required,
            "data_version": rs.data_version,
        };
      });
    }

    PermissionsRequiredSignoffs.getRequiredSignoffs()
    .success(function(response) {
      if (response["count"] > 0) {
        response["required_signoffs"].forEach(function(rs) {
          if (! (rs.product in $scope.required_signoffs)) {
            $scope.required_signoffs[rs.product] = {"permissions": {}};
          }
          else if (! ("permissions" in $scope.required_signoffs[rs.product])) {
            $scope.required_signoffs[rs.product]["permissions"] = {};
          }
        
          $scope.required_signoffs[rs.product]["permissions"][rs.role] = {
            "signoffs_required": rs.signoffs_required,
            "data_version": rs.data_version,
          };
        });
      }
    })
    // can a response be grabbed here?
    .error(function(response) {
      alert("error! " + response);
    })
    .finally(function() {
    });
  })
  // can a response be grabbed here?
  .error(function(response) {
    alert("error! " + response);
  })
  .finally(function() {
    $scope.loading = false;
  });

  // Setting up dialogs the page uses
  $scope.addNewRequiredSignoff = function() {
    $modal.open({
      templateUrl: "required_signoff_modal.html",
      controller: "NewRequiredSignoffCtrl",
      backdrop: "static",
      resolve: {
        required_signoffs: function() {
          return $scope.required_signoffs;
        },
      }
    });
  };
});
