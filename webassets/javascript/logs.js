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
            if (areaobject.style.display == 'none') {
                areaobject.style.display = "none";
            } else {
                areaobject.style.display = "";
            };
        };
    };
};
