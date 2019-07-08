//Sets up the page load

$(document).ready(function ()
{
    $('#ajaxloader').hide();
});




function showHideRows(rownumber)
{
    for( var subrow = 0; subrow < 1000; subrow++ ) {
        var subrowfractionid = "000";
        subrowfractionid = subrowfractionid.concat(subrow.toString());
        subrowfractionid = subrowfractionid.substring(subrowfractionid.length - 2, 999)
        var subrowid = rownumber.toString()
        subrowid = subrowid.concat(".", subrowfractionid)
        var areaobject = document.getElementById(subrowid);
        if (areaobject != null) {
            var currentclass = areaobject.className
            if (currentclass.substring(0, 6) == 'hidden') {
                areaobject.className = currentclass.substring(6, currentclass.length);
            } else {
                areaobject.className = "hidden".concat(areaobject.className);
            };
        };
    };
};
