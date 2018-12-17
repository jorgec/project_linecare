/**
 * Resets a form to its original state based on formFields
 * @param formFields - array of JSON objects of the format:
 *      {
            id: form control id
            value: current value,
            default: default value,
            state: default state
        }
 */
function resetForm(formFields) {
    for (var key in formFields) {
        var control = $(formFields[key].elementId);
        if (formFields[key].state) {
            control.attr(formFields[key].state, formFields[key].state)
        }
        control.val(formFields[key].default);
    }
}

function loadFormData(formFields, response){
    for(fieldItem in formFields){
        var target = $(formFields[fieldItem].elementId);
        var field = formFields[fieldItem].fieldName;
        var fieldValue = null;
        if (field.includes(".")) {
            var parts = field.split(".");
            var partsLen = parts.length;

            if(partsLen == 2){
                fieldValue = response[parts[0]][parts[1]];
            }else if(partsLen == 3){
                fieldValue = response[parts[0]][parts[1]][parts[2]];
            }else if(partsLen == 4){
                fieldValue = response[parts[0]][parts[1]][parts[2]][parts[3]];
            }
        }else{
            fieldValue = response[field];
        }
        target.val(fieldValue);
        console.log(target.val());
    }
}

function postForm(url, postData) {
        var onSuccess =
        arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : [];
        var onFail =
        arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : [];
        var failSilently =
        arguments.length > 4 && arguments[4] !== undefined ? arguments[4] : false;
    
        $.post(url, postData)
        .done(function(response) {
            $.notify(
            {
                message: "Success"
            },
            {
                type: "success"
            }
            );
            for (var i in onSuccess) {
            onSuccess[i]();
            }
            return true;
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
            if (!failSilently) {
            Object.keys(jqXHR.responseJSON).forEach(function(k) {
                $.notify(
                {
                    message: jqXHR.responseJSON[k]
                },
                {
                    type: "danger"
                }
                );
            });
            }
            for (var i in onFail) {
            onFail[i]();
            }
            return false;
        });
}
