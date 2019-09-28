function updateStartStopButtons(torrentstate, oldtorrentstate)
{
    var oldstatesuffix = oldtorrentstate.substr(torrentstate.length-6);
    var torrentstatesuffix = torrentstate.substr(torrentstate.length-6);
    if ((torrentstatesuffix == "active") || (torrentstatesuffix == "queued")) {
        if ((oldstatesuffix != "active") && (oldstatesuffix != "queued")) {
            changeButtonState('Start', 'Hide');
            changeButtonState('Start', 'Enable');
            changeButtonState('Stop', 'Show');
        };
    } else if (torrentstatesuffix == "paused") {
        if (oldstatesuffix != "paused") {
            changeButtonState('Stop', 'Hide');
            changeButtonState('Stop', 'Enable');
            changeButtonState('Start', 'Show');
        };
    } else {
        changeButtonState('Stop', 'Hide');
        changeButtonState('Start', 'Hide');
        changeButtonState('Start', 'Enable');
        changeButtonState('Stop', 'Enable');
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
    rerenderAnimatedImage('Copy_Overlay', 'copierstates/'+copyqueuestate, 'gif')
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

