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
function resetForm(formFields, prefix="") {
    for (var key in formFields) {
        var control = $("#" + prefix + formFields[key].id);
        if (formFields[key].state) {
            control.attr(formFields[key].state, formFields[key].state)
        }
        control.val(formFields[key].default);
    }
}

function loadFormData(formFields, response, prefix="edit_"){
    for(fieldItem in formFields){
        var target = $("#" + prefix + formFields[fieldItem].id);
        var target_name = prefix + formFields[fieldItem].id;
        var field = formFields[fieldItem].field_name;
        var field_value = null;
        if (field.includes(".")) {
            var parts = field.split(".");
            var parts_len = parts.length;

            if(parts_len == 2){
                field_value = response[parts[0]][parts[1]];
            }else if(parts_len == 3){
                field_value = response[parts[0]][parts[1]][parts[2]];
            }else if(parts_len == 4){
                field_value = response[parts[0]][parts[1]][parts[2]][parts[3]];
            }
        }else{
            field_value = response[field];
        }
        target.val(field_value);
    }
}

function postForm(url, postData, onSuccess=[], onFail=[], failSilently=false){
    $.post(url, postData)
        .done(function (response) {
            $.notify({
                message: "Success"
            }, {
                type: 'success'
            });
            for(var i in onSuccess){
                onSuccess[i]();
            }
            return true;
        })
        .fail(function (jqXHR, textStatus, errorThrown) {
            if(!failSilently) {
                Object.keys(jqXHR.responseJSON).forEach(function (k) {
                    $.notify({
                        message: jqXHR.responseJSON[k]
                    }, {
                        type: 'danger'
                    });
                });
            }
            for(var i in onFail){
                onFail[i]();
            }
            return false;
        });
}