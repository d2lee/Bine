bineApp.controller('bookListControl', ['$scope', '$http', 'authService', function ($scope, $http, authService) {

    // check the authentication
    if (!authService.check_auth_and_set_user($scope)) {
        return;
    }

    $scope.load_book_list = function () {
        $http.get('/api/book/').success(function (data) {
            $scope.books = data;
        });
    }

    $scope.load_book_list();
} ]);