angular.module('ticketApp', ['ngAnimate', 'ui.bootstrap'])
    .controller('NewTicketController', function($scope) {
      $scope.minDate = new Date();
      $scope.dt = $scope.minDate;
    })
    .controller('ViewTicketController', function($scope, $http) {
      $scope.get_tickets = function() {
        $http.get('/api/tickets/' + $scope.client_id)
          .then(function(response) {
            var sorted = _.sortBy(response.data, function(t) { return t.priority; });
            $scope.tickets = sorted;
          })
      };
    });
