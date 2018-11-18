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
        var field = formFields[fieldItem].field_name;
        var field_value = null;
        if (field.includes(".")) {
            var parts = field.split(".")
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
        $("#" + prefix + formFields[fieldItem].id).val(field_value);
    }
}