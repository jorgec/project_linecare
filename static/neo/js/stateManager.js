function bootUp(model) {
    for (var key in model) {
        if (model[key].onReady) {
            updateState(model[key]);
        }
    }
}

function updateState(entity) {
    entity.fetch();
}


/**
 * requires jQuery
 *
 */
function buildURLwithParams(action) {
    var params = $.param(action.parameters);
    return action.api + params;
}