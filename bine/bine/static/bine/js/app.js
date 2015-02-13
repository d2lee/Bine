var bineApp = angular.module('bineApp', [
                             'ngRoute',
                             'ngSanitize',
                             'angularFileUpload',
                             'bineControllers'
                             ]);

var bineControllers = angular.module('bineControllers', []);

bineApp.config(['$routeProvider',
                function($routeProvider) {
                  $routeProvider.
                    when('/login/', {
                      templateUrl: '/static/bine/html/login.html',
                      controller: 'UserAuthControl'
                    }).
                    when('/register/', {
                        templateUrl: '/static/bine/html/register.html',
                        controller: 'UserAuthControl'
                      }).
                  	when('/note/', {
                      templateUrl: '/static/bine/html/note_list.html',
                      controller: 'NoteListControl'
                    }).
                    when('/note/new/', {
                        templateUrl: '/static/bine/html/note_form.html',
                        controller: 'NoteNewControl'
                      }).
                    when('/note/:note_id/', {
                      templateUrl: '/static/bine/html/note_detail.html',
                      controller: 'NoteDetailControl'
                    }).
                    when('/book/', {
                        templateUrl: '/static/bine/html/book_list.html',
                        controller: 'bookListControl'
	                }).
	                otherwise({
                      redirectTo: '/login/'
                    });
                }]);

bineApp.config(['$httpProvider', function($httpProvider) {
	    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
	    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	}
]);

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


