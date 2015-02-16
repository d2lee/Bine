bineApp.controller('UserAuthControl', ['$scope', '$http', 'userService',
    function ($scope, $http, userService) {
        // initialize
        $scope.username = "";
        $scope.password = "";

        userService.clear();

        // login check
        $scope.login = function () {
            $http.post('/api-token-auth/', {
                'username': $scope.username,
                'password': $scope.password,
            }).success(function (data) {
                userService.set_token_and_user_info(data);
                location.href = "#/note/"
            }).error(function (data) {
                alert('로그인이 실패했습니다. 사용자 정보를 다시 확인하십시오.');
            });
        }

        $scope.make_birthday = function () {
            var year = $scope.birth_year;
            var month = $scope.birth_month;
            var day = $scope.birth_day;

            if (year.v != null && month.v != null && day.v != null) {
                $scope.birthday = year.name + '-' + month.name + '-' + day.name;
            }
            else {
                $scope.birthday = '';
            }
        }

        $scope.equal_password = function () {
            return $scope.password1 == $scope.password2;
        }

        $scope.register = function () {
            if (!$scope.reg_form.$valid)
                return;

            var url = "/auth/register/";

            $scope.make_birthday();

            data = {
                'username': $scope.username,
                'fullname': $scope.fullname,
                'email': $scope.email,
                'birthday': $scope.birthday,
                'sex': $scope.sex,
                'password': $scope.password1,
            }

            $http.post(url, data).success(function (data) {
                alert('회원 가입이 성공하였습니다.시작 메뉴로 이동합니다.');
                userService.set_token_and_user_info(data);
                location.href = "#/note/";
            });
        }

        $scope.set_sex = function (sex) {
            $scope.sex = sex;
        }

        $scope.date_range = function (min, max, step) {
            // parameters validation for method overloading
            if (max == undefined) {
                max = min;
                min = 0;
            }

            step = Math.abs(step) || 1;
            if (min > max) {
                step = -step;
            }
            // building the array
            var output = [];

            for (var value = min; value != max; value += step) {
                // adding '0' if it's single digit
                if (value < 10) {
                    title = "0" + value;
                }
                else {
                    title = value;
                }
                output.push({'name': title, 'v': value});
            }

            output.push({'name': max, 'v': max});

            // returning the generated array
            return output;
        };

        $scope.init_birthday = function () {
            $scope.year_list = $scope.date_range((new Date()).getFullYear(), 1910);
            $scope.month_list = $scope.date_range(1, 12);
            $scope.day_list = $scope.date_range(1, 31);
        }

        $scope.init_birthday();

    } ]);