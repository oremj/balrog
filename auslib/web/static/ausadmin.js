function handleError(req, code, error) {
    alert(req);
    alert(code);
    alert(error);
}

function getHTML(path) {
    return $.get(SCRIPT_ROOT + path, {'format': 'html'}
    ).error(handleError
    );
}

function getFullURL(url) {
    return SCRIPT_ROOT + url;
}

function getNewUserPermission(username) {
    return getHTML(getFullURL('/users/' + username + '/permissions/new'));
}

function getUsers(element) {
    getHTML('/users')
    .success(function(data) {
        element.append(data);
    });
}

function getUserPermissions(username, element) {
    getHTML('/users/' + username + '/permissions')
    .success(function(data) {
        element.append(data);
    });
}

function addNewUserPermission(username, permission, element) {
    $.put(SCRIPT_ROOT + '/users/' + username + '/permissions/' + permission), {'format': 'html'})
    .error(handleError
    ).success(function(data) {
        element.append(data);
    });
}

function redirect(page, args) {
    window.location.assign(page + '?' + $.param(args));
}
