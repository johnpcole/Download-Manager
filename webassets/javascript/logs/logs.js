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
        rerenderImage(masterRowName, 'log/expanded', 'png');
    } else {
        rerenderImage(masterRowName, 'log/collapsed', 'png');
    };
    for( var subRow = 0; subRow < 100; subRow++ ) {
        var subRowId = getSubRowId(rowNumber, subRow);
        var areaObject = document.getElementById(subRowId);
        if (areaObject != null) {
            var baseClass = areaObject.className
            var baseClass = baseClass.substring(4, baseClass.length);
            if (currentStatus == 'collapsed_indicator') {
                changeAreaClass(subRowId, "show".concat(baseClass));
            } else {
                changeAreaClass(subRowId, "hide".concat(baseClass));
            };
        };
    };
};



function getSubRowId(mainRow, subRow)
{
    var subRowFractionId = "000".concat(subRow.toString());
    subRowFractionId = subRowFractionId.substring(subRowFractionId.length - 2, 999)
    var subRowId = mainRow.toString()
    subRowId = subRowId.concat(".", subRowFractionId)
    return subRowId;
};