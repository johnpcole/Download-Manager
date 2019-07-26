function updateStartStopButtons(torrentstate)
{
    var torrentstatesuffix = torrentstate.substr(torrentstate.length-6);
    if ((torrentstatesuffix == "active") || (torrentstatesuffix == "queued")) {
        changeButtonState('Start', 'Hide');
        changeButtonState('Stop', 'Show');
    } else if (torrentstatesuffix == "paused"){
        changeButtonState('Stop', 'Hide');
        changeButtonState('Start', 'Show');
    } else {
        changeButtonState('Stop', 'Hide');
        changeButtonState('Start', 'Hide');
    };
};


function updateCopyButton(torrentstate, torrenttype, copyqueuestate)
{
    var torrentstateprefix = torrentstate.substr(0, 7);
    if ((torrentstateprefix == "seeding") && (torrenttype != "unknown")) {
        if ((copyqueuestate == "nothing") || (copyqueuestate == "completed")) {
            changeButtonState('Copy', 'Enable');
        } else {
            changeButtonState('Copy', 'Disable');
        };
    } else {
        changeButtonState('Copy', 'Disable');
    };
    rerenderImage('Copy_Overlay', 'copyoverlay_'+copyqueuestate, 'gif')
};



function updateEditButton()
{
    var areaobjectlist = document.getElementsByClassName('filetilelowerrow');
    var areaindex = areaobjectlist.length;
    if (areaindex > 0) {
        changeButtonState('Edit', 'Enable');
    } else {
        changeButtonState('Edit', 'Disable');
    };
};



function updateDeleteButton(copyqueuestate)
{
    if ((copyqueuestate == "nothing") || (copyqueuestate == "completed")) {
        changeButtonState('Delete', 'Enable');
    } else {
        changeButtonState('Delete', 'Disable');
    };
};


