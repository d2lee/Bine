var bineApp = angular.module('bineApp', ['ngRoute', 'ngCookies', 'ngSanitize',
    'angular-jwt', 'angularFileUpload']);

bineApp.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/login/', {
        templateUrl: '/static/bine/html/login.html',
        controller: 'UserAuthControl'
    }).when('/register/', {
        templateUrl: '/static/bine/html/register.html',
        controller: 'UserAuthControl'
    }).when('/note/', {
        templateUrl: '/static/bine/html/note_list.html',
        controller: 'NoteListControl'
    }).when('/note/new/', {
        templateUrl: '/static/bine/html/note_form.html',
        controller: 'NoteNewControl'
    }).when('/note/:note_id/', {
        templateUrl: '/static/bine/html/note_detail.html',
        controller: 'NoteDetailControl'
    }).when('/book/', {
        templateUrl: '/static/bine/html/book_list.html',
        controller: 'bookListControl'
    }).when('/friend/', {
        templateUrl: '/static/bine/html/friend_confirmed.html',
        controller: 'friendConfirmedListControl'
    }).when('/friend/confirmed/', {
        templateUrl: '/static/bine/html/friend_confirmed.html',
        controller: 'friendConfirmedListControl'
    }).when('/friend/unconfirmed/', {
        templateUrl: '/static/bine/html/friend_unconfirmed.html',
        controller: 'friendUnconfirmedListControl'
    }).when('/friend/search', {
        templateUrl: '/static/bine/html/friend_search.html',
        controller: 'friendSearchControl'
    }).when('/friend/recommend', {
        templateUrl: '/static/bine/html/friend_recommend.html',
        controller: 'friendRecommendControl'
    }).otherwise({
        redirectTo: '/login/'
    });
}]);

bineApp.service('userService', ['$http', '$window', 'jwtHelper',
    function ($http, $window, jwtHelper) {

        this.clear = function () {
            this.set_user(null);
            this.set_token(null);
        }

        this.check_auth_and_set_user = function ($scope) {
            var token = this.get_token();
            var isTokenExpired;

            try {
                isTokenExpired = jwtHelper.isTokenExpired(token);
                if ((token != null) && !isTokenExpired) {
                    $scope.user = this.get_user();
                    return true;
                }
            }
            catch (err) {
            }

            location.href = "#/login/";
            return false;
        }

        this.set_token_and_user_info = function (data) {
            this.set_token(data.token);
            this.set_user(data.user);
        }

        this.set_token = function (token) {
            $window.sessionStorage.token = token;
        }

        this.get_token = function () {
            return $window.sessionStorage.token;
        }

        this.get_user = function () {
            return angular.fromJson($window.sessionStorage.user);
        }

        this.set_user = function (user) {
            $window.sessionStorage.user = angular.toJson(user);
        }
    }]);

bineApp.config(function Config($httpProvider, jwtInterceptorProvider) {
    jwtInterceptorProvider.authPrefix = 'JWT ';
    jwtInterceptorProvider.tokenGetter = ['userService',
        function (userService) {
            return userService.get_token();
        }];

    $httpProvider.interceptors.push('jwtInterceptor');
})

bineApp.filter('truncate', function () {
    return function (content, maxCharacters) {
        if (content == null)
            return "";

        content = "" + content;
        content = content.trim();
        if (content.length <= maxCharacters)
            return content;

        content = content.substring(0, maxCharacters);
        var lastSpace = content.lastIndexOf(" ");
        if (lastSpace > -1)
            content = content.substr(0, lastSpace);

        return content + '...';
    };
});
