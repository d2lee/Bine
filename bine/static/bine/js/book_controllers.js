bineApp.controller('bookListControl', [ '$scope', '$http', 'userService', function ($scope, $http, userService) {

    // check the authentication
    if (!userService.check_auth_and_set_user($scope)) {
        return;
    }

    $scope.load_book_list = function () {
        $http.get('/book/').success(function (data) {
            $scope.books = data;
        });
    }

    $scope.load_book_list();
} ]);