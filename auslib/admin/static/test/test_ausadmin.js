function resetdb() {
    $.ajax(SCRIPT_ROOT + '/reset', {'async': false})
    .error(function() {
        throw "Error resetting database";
    });
}

asyncTest("testAddNewPermission", 2, function() {
    resetdb();
    var ret = $('<div></div');
    var checkElement = function() {
        ok(ret.html().match(/admin/), "new element doesn't have new permission in it");
        start();
    }
    addNewPermission('foo', 'admin', null, ret, checkElement)
    .complete(function(response, text) {
        ok(response.status == 201, "got incorrect response from the server (" + response.status + ") instead of 201");
    });
});
