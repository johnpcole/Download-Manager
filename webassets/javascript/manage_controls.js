// Update button visibility

function changeButtonState(buttonid, displayvalue)
{
    var controlobject = document.getElementById(buttonid);
    if (controlobject != null) {
        if (displayvalue == 'Hide') {
            controlobject.style.display = "none";
        } else if (displayvalue == 'Show') {
            controlobject.style.display = "inline";
        } else if (displayvalue == 'Enable') {
            controlobject.disabled = false;
        } else if (displayvalue == 'Disable') {
            controlobject.disabled = true;
        } else {
            alert ("Unknown button state: "+displayvalue)
        };
    } else {
    alert("Cant find button: "+buttonid)
    };
};


// Get Button Enabled/Disabled state

function getButtonState(buttonid)
{
    var controlobject = document.getElementById(buttonid);
    if (controlobject != null) {
        if (controlobject.style.display == 'none') {
            return "Hidden";
        } else if (controlobject.disabled == false) {
            return "Enabled";
        } else if (controlobject.disabled == true) {
            return "Disabled";
        } else {
            alert ("Unknown button state!")
        };
    } else {
    alert("Cant find button: "+buttonid)
    };
};






// Update control visibility

function changeControlState(controlname, displayvalue)
{
    var controlobject = document.getElementsByName(controlname)[0];
    if (controlobject != null) {
        if (displayvalue == 'Hide') {
            controlobject.style.display = "none";
        } else if (displayvalue == 'Show') {
            controlobject.style.display = "inline";
        } else if (displayvalue == 'Enable') {
            controlobject.disabled = false;
        } else if (displayvalue == 'Disable') {
            controlobject.disabled = true;
        } else {
            alert ("Unknown button state: "+displayvalue)
        };
    } else {
        alert("Cant find control: "+controlname)
    };
};


// Get Control Enabled/Disabled state

function getControlState(controlname)
{
    var controlobject = document.getElementsByName(controlname)[0];
    if (controlobject != null) {
        if (controlobject.style.display == 'none') {
            return "Hidden";
        } else if (controlobject.disabled == false) {
            return "Enabled";
        } else if (controlobject.disabled == true) {
            return "Disabled";
        } else {
            alert ("Unknown button state!")
        };
    } else {
        alert("Cant find control: "+controlname)

    };
};



//Get field value

function getFieldValue(fieldname)
{
    var fieldobject=document.getElementsByName(fieldname)[0]
    if (fieldobject != null) {
        return fieldobject.value;
    } else {
        alert("Cant find field: "+fieldname)
    };
};



//Set field value

function setFieldValue(fieldname, fieldvalue)
{
    var fieldobject=document.getElementsByName(fieldname)[0]
    if (fieldobject != null) {
        fieldobject.value = fieldvalue;
    } else {
        alert("Cant find field: "+fieldname)
    };
};



//Set checkbox value

function setCheckboxValue(fieldname, fieldvalue)
{
    var checkbox = document.getElementsByName(fieldname)[0]
    if (checkbox != null) {
        checkbox.checked = fieldvalue;
    } else {
        alert("Cant find checkbox: "+fieldname)
    };
};



//Get checkbox value

function getCheckboxValue(fieldname)
{
    var checkbox = document.getElementsByName(fieldname)[0]
    if (checkbox != null) {
        return checkbox.checked;
    } else {
        alert("Cant find checkbox: "+fieldname)
    };
};


//Repopulates dropdown list

function repopulateDropDownList(fieldname, itemlist)
{
    var combobox = document.getElementsByName(fieldname)[0];
    if (combobox != null) {
        var newoptions = '';
        $.each(itemlist, function(index)
        {
            newoptions = newoptions + '<option value=\"'+itemlist[index]+'\">'+itemlist[index]+'</option>';
        });
        combobox.innerHTML = newoptions;
    } else {
        alert("Cant find dropdownlist: "+fieldname)
    };
};

/*
//Clear dropdown list

function clearDropDownList(fieldname)
{
    var combobox = document.getElementsByName(fieldname)[0];
    while (comboBox.options.length > 0)
    {
        comboBox.remove(0);
    };
};
*/


//Set dropdown value

function setDropDownValue(fieldname, fieldvalue)
{
    var combobox = document.getElementsByName(fieldname)[0];
    if (combobox != null) {
        var itemcount = combobox.options.length;
        for (var i=0; i<itemcount; i++)
        {
            if (combobox.options[i].value == fieldvalue)
            {
                combobox.options[i].selected = true;
                break;
            };
        };
    } else {
        alert("Cant find dropdownlist: "+fieldname)
    };
};

