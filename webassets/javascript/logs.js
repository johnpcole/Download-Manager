//Sets up the page load

$(document).ready(function ()
{
    $('#ajaxloader').hide();
});




function showHideRows(rowNumber)
{
    var masterRowName = "Entry".concat(rowNumber.toString());
    var currentStatus = getImageName(masterRowName);
    if (currentStatus == 'collapsed_indicator') {
        rerenderImage(masterRowName, 'expanded_indicator');
    } else {
        rerenderImage(masterRowName, 'collapsed_indicator');
    };
    for( var subRow = 0; subRow < 100; subRow++ ) {
        var subRowId = getSubRowId(rowNumber, subRow);
        var areaObject = document.getElementById(subRowId);
        if (areaObject != null) {
            var baseClass = areaObject.className
            var baseClass = baseClass.substring(4, currentclass.length);
            if (currentStatus == 'collapsed_indicator') {
                changeAreaClass(areaObject, "show".concat(baseClass));
            } else {
                changeAreaClass(areaObject, "hide".concat(baseClass));
            };
        };
    };
};



function getSubRowId(row, subrow)
{
    var subrowfractionid = "000".concat(subrow.toString());
    subrowfractionid = subrowfractionid.substring(subrowfractionid.length - 2, 999)
    var subrowid = rowNumber.toString()
    subrowid = subrowid.concat(".", subrowfractionid)
    return subrowid;
};