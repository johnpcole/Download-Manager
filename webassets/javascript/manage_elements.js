// Update area visibility

function changeAreasState(areaname, displayvalue)
{
    var areaobjectlist = document.getElementsByClassName(areaname);
    var areaindex;
    for (areaindex = 0; areaindex < areaobjectlist.length; areaindex++) {
        areaobject = areaobjectlist[areaindex]
        if (displayvalue == 'Hide') {
            areaobject.style.display = "none";
        } else {
            areaobject.style.display = "inline-block";
        };
    };
};



// Update area visibility

function changeAreaState(areaname, displayvalue)
{
    var areaobject = document.getElementById(areaname);
    if (areaobject != null) {
        if (displayvalue == 'Hide') {
            areaobject.style.display = "none";
        } else {
            areaobject.style.display = "inline-block";
        };
    } else {
        alert("changeAreaState: "+areaname);
    };
};


// Update area colour

function changeAreaColour(areaname, displayvalue)
{
    var areaobject = document.getElementById(areaname);
    if (areaobject != null) {
        areaobject.style.backgroundColor = displayvalue;
    } else {
        alert("changeAreaColour: "+areaname);
    };
};



// Update area class

function changeAreaClass(areaname, classvalue)
{
    var areaobject = document.getElementById(areaname);
    if (areaobject != null) {
        areaobject.className = classvalue;
    } else {
        alert("changeAreaClass: "+areaname);
    };
};



// Update the displayed text

function rerenderText(fieldname, fieldvalue)
{
    var tileData = document.getElementById(fieldname);
    if (tileData != null) {
        tileData.innerHTML = fieldvalue;
    } else {
        alert("rerenderText: "+fieldname);
    };
};



// Get the displayed text

function getText(fieldname)
{
    var tileData = document.getElementById(fieldname);
    if (tileData != null) {
        return tileData.innerHTML;
    } else {
        alert("getText: "+fieldname);
    };
};



// Update the displayed image

function rerenderImage(fieldname, fieldimage)
{
    var tileData = document.getElementById(fieldname);
    if (tileData != null) {
        tileData.src = "./static/images/"+fieldimage+".png";
    } else {
        alert("rerenderImage: "+ fieldname);
    }
};



// Get displayed image filename

function getImageName(fieldname)
{
    var tileData = document.getElementById(fieldname);
    var outcome = "unknown"
    if (tileData != null) {
        var fullpath = tileData.src;
        var pathsplit = fullpath.split('/');
        var filename = pathsplit[pathsplit.length-1];
        outcome = filename.split('.')[0];
    } else {
        alert("GetImageName: "+ fieldname);
    }
    return outcome
};



// Get Area Hidden/Displayed state

function getAreaState(areaid)
{
    var controlobject = document.getElementById(areaid);
    if (controlobject != null) {
        if (controlobject.style.display == 'none') {
            return "Hidden";
        } else {
            return "Displayed";
        };
    } else {
    alert("Cant find area: "+areaid)
    };
};


