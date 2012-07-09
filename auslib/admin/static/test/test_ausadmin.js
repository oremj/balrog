test("testScriptRootDefined", function() {
    ok(SCRIPT_ROOT != null, "SCRIPT_ROOT is null.");
});

test("testAddNewPermission", function() {
    var ret = document.createElement('div');
    addNewPermission('foo', 'admin', null, ret)
    .complete(function(response, text) {
        console.log(ret.innerHTML);
    });
});
