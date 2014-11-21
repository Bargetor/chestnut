var ng_app_chestunt_name = "chestnut";

var chestnut_app = angular_app_init(ng_app_chestunt_name);

chestnut_app.controller('WechatInfoController', ['$scope', '$http', function($scope, $http){

    $scope.get_wechat_user_info_by_angular = function(username, password){
        // get_wechat_user_info('bargetor_public@sina.com', 'lanqiao@mj', $scope.get_wechat_user_info_by_angular_callback);

        var request = $http.post('/chestnut/support/wechat/user_info/', {'username' : username, 'password' : hex_md5(password)});

        request.success(function(response, status, headers, config){
            $scope.wechat_info = response;
        });
    };
}]);
