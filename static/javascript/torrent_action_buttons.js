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


function updateCopyButton(torrentstate)
{
    var torrentstateprefix = torrentstate.substr(0, 7);
    if (torrentstateprefix == "seeding") {
        changeButtonState('Copy', 'Enable');
    } else {
        changeButtonState('Copy', 'Disable');
    };
};



function updateEditButton()
{
    var areaobjectlist = document.getElementsByClassName('file_all');
    var areaindex = areaobjectlist.length;
    if (areaindex > 0) {
        changeButtonState('Edit', 'Enable');
    } else {
        changeButtonState('Edit', 'Disable');
    };
};