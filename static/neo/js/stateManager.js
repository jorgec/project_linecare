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

function genericFetch(key) {
    var entity = model[key];

    $.get(entity.dataSrc)
        .done(function (result) {
            // console.log(key, entity.dataSrc, result);

            entity.container.loadTemplate(entity.template, result);

            // onSuccessResult
            if (entity.onSuccessResult.length > 0) {
                $.each(entity.onSuccessResult, function (key, action) {
                    action(result);
                });
            }

            // onSuccess
            if (entity.onSuccess.length > 0) {
                $.each(entity.onSuccess, function (key, action) {
                    action();
                });
            }

            // register bindings
            $.each(entity.actions, function (key, action) {
                if(action.apiConsumer){
                    $(action.parameters.triggerElement).click(function (e) {
                        e.preventDefault();
                        var url = action.parameters.api + "id=" + $(this).attr(action.parameters.id);
                        action.fn(url, action.parameters.onSuccess);
                    })
                }else{
                    $(action.parameters.triggerElement).click(function(e){
                        e.preventDefault();
                        var params = {};
                        var elem = $(this);
                        $.each(action.parameters.fnParams, function(i, param){
                            params[param] = elem.attr(param);
                        });
                        action.fn(params);
                    })
                }
            });
        })
        .fail(function (jqXHR, textStatus, errorThrown) {
            $.notify({
                message: jqXHR.responseJSON
            }, {
                type: 'danger'
            });
        });
}

function genericGetAction(url, onSuccess) {
    $.get(url)
        .done(function (result) {
            $.notify({
                message: result
            }, {
                type: 'success'
            });

            // update states on success
            if (onSuccess.length > 0) {
                $.each(onSuccess, function (key, action) {
                    updateState(model[action]);
                });
            }

        })
        .fail(function (jqXHR, textStatus, errorThrown) {
            $.notify({
                message: jqXHR.responseJSON
            }, {
                type: 'danger'
            });
        });
}