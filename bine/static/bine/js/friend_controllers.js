bineApp.controller('friendListControl', ['$scope', '$http', 'userService', function ($scope, $http, userService) {

    // check the authentication
    if (!userService.check_auth_and_set_user($scope)) {
        return;
    }

    $scope.load_friend_list = function () {
        $http.get('/friend/').success(function (data) {
            $scope.friends = data;
        });
    }

    $scope.load_friend_list();
}]);