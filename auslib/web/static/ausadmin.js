function handleError(req, code, error) {
    alert(req);
    alert(code);
    alert(error);
}

function addNewPermission(username, permission, options, element) {
    url = SCRIPT_ROOT + '/users/' + username + '/permissions' + permission;
    $.ajax(url, {'type': 'put'})
    .error(handleError
    ).success(function(data) {
        $.get(url, {'format': 'html'})
        .error(handleError
        ).success(function(data) {
            element.append(data);
        });
    });
}

function redirect(page, args) {
    window.location.assign(page + '?' + $.param(args));
}
